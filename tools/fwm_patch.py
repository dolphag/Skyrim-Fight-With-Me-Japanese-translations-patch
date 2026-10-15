# -*- coding: utf-8 -*-
"""Fight With Me 0.1.0 (FightWithMe.dll) 日本語化パッチ生成。

使い方: python3 fwm_patch.py <原版FightWithMe.dll> <出力DLL> <レポートJSON>

方針 (WWM向けtools/build_patch.pyと同系統):
  1. 画面表示用の英語文字列を .jpn セクション(新設)の日本語文字列へ付け替える
       - lea reg,[rip+disp] の参照先を付け替え
       - 直後/直前の長さ即値(std::string_view / fmt書式)も同時に更新
       - ポインタ表(.rdata)のスロットと、隣接する長さ(string_view)を更新
       - コンパイラがその場で展開した std::string の組み立て領域は、
         std::string(const char*,size_t) 生成関数の呼び出しに置換 (レジスタ生存を検証)
  2. Label/LabelWidth は文字列を1バイトずつ描画するためUTF-8が壊れる。
       非ASCIIを含む場合のみ Text/TextSize へ振り分けるスタブを .text 末尾の空きに置く。
"""
import sys, os, json, struct, collections
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import *
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fwm_trans1 import T1
from fwm_trans2 import T2
from fwm_trans3 import T3
from fwm_trans4 import T4
import fwm_cfg as C

SRC, OUT, REP = sys.argv[1:4]
T = {**T1, **T2, **T3, **T4}

# ---- 表示可能な漢字の検査 ----------------------------------------------------------------
# SKSE Menu Framework 3 (ImGui) は GetGlyphRangesJapanese の漢字2999字しか描画できず、範囲外は「?」になる。
# 訳文に範囲外の漢字があればビルドを止める。許可字表は tools/jp_kanji.txt (1行に全字、ImGui 1.91.9 の範囲)。
_kj = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jp_kanji.txt'), encoding='utf-8').read().strip()
_ok = set(_kj)
_bad = {}
for _en, _ja in T.items():
    for _ch in _ja:
        if '\u4e00' <= _ch <= '\u9fff' and _ch not in _ok: _bad.setdefault(_ch, []).append(_en[:40])
for _ja in [r_[5] for r_ in C.IMM_REGIONS] + [r_[2] for r_ in C.SITE_STR]:
    for _ch in _ja:
        if '\u4e00' <= _ch <= '\u9fff' and _ch not in _ok: _bad.setdefault(_ch, []).append(_ja)
if _bad:
    raise SystemExit('描画できない漢字(「?」になる): ' + ', '.join('%s=%s' % (k_, v_[:2]) for k_, v_ in _bad.items()))
raw = open(SRC, 'rb').read()
data = bytearray(raw)
pe = pefile.PE(SRC)
IB = pe.OPTIONAL_HEADER.ImageBase
FA = pe.OPTIONAL_HEADER.FileAlignment
SA = pe.OPTIONAL_HEADER.SectionAlignment
secs = pe.sections
last = secs[-1]
assert len(raw) == last.PointerToRawData + last.SizeOfRawData, 'overlay/signature present'
S = {s.Name.rstrip(b'\0').decode(): s for s in secs}
tx, rd, dt, pd = S['.text'], S['.rdata'], S['.data'], S['.pdata']
def al(v, a): return (v + a - 1) // a * a
new_va = al(last.VirtualAddress + last.Misc_VirtualSize, SA)
new_raw = last.PointerToRawData + last.SizeOfRawData
def sec_of(va):
    for s in secs:
        if s.VirtualAddress <= va < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData): return s
def off(va):
    s = sec_of(va); return s.PointerToRawData + va - s.VirtualAddress
def u32(o): return struct.unpack_from('<I', data, o)[0]

pool = bytearray(); cache = {}
def add(b):
    if b in cache: return cache[b]
    o = len(pool); pool.extend(b); cache[b] = o; return o
def jva(o): return new_va + o

changes = []     # (file_offset, length, label)
log = []         # 人が読むレポート
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True

# ---- .rdata の文字列表 ---------------------------------------------------
rdraw = bytes(raw[rd.PointerToRawData:rd.PointerToRawData + rd.SizeOfRawData])
strs = {}; i = 0
while i < len(rdraw):
    j = rdraw.find(b'\0', i)
    if j < 0: break
    if j > i: strs[rd.VirtualAddress + i] = rdraw[i:j]
    i = j + 1
rev = collections.defaultdict(list)
for va, b in strs.items(): rev[b].append(va)

# ---- 関数(.pdata)と全命令 ----------------------------------------------
pdraw = raw[pd.PointerToRawData:pd.PointerToRawData + pd.Misc_VirtualSize]
funcs = sorted((b, e) for b, e, u in (struct.unpack_from('<III', pdraw, k) for k in range(0, len(pdraw) - 11, 12))
               if tx.VirtualAddress <= b < tx.VirtualAddress + tx.Misc_VirtualSize and e > b)
fins = {}   # func -> (insn list, addr->index)
def decode(f):
    if f not in fins:
        code = raw[off(f[0]):off(f[0]) + f[1] - f[0]]
        ins = list(md.disasm(code, IB + f[0]))
        fins[f] = (ins, {x.address - IB: k for k, x in enumerate(ins)})
    return fins[f]
import bisect
fbeg = [f[0] for f in funcs]
def func_of(a):
    k = bisect.bisect_right(fbeg, a) - 1
    if k >= 0 and funcs[k][0] <= a < funcs[k][1]: return funcs[k]
def ripref(x):
    for op in x.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return x.address + x.size + op.mem.disp - IB
rd_lo, rd_hi = rd.VirtualAddress, rd.VirtualAddress + rd.Misc_VirtualSize

# rdata を指す全参照 (target -> [(addr, insn)])
refs = collections.defaultdict(list)
for f in funcs:
    for x in decode(f)[0]:
        t = ripref(x)
        if t is not None and rd_lo <= t < rd_hi: refs[t].append((x.address - IB, x, f))

# ---- 再配置 ---------------------------------------------------------------
reloc = set()
for blk in pe.DIRECTORY_ENTRY_BASERELOC:
    for e in blk.entries:
        if e.type: reloc.add(e.rva)

# ---- 長さ即値の検出 -------------------------------------------------------
REG32 = {X86_REG_EAX, X86_REG_ECX, X86_REG_EDX, X86_REG_R8D, X86_REG_R9D, X86_REG_R10D, X86_REG_R11D,
         X86_REG_EBX, X86_REG_ESI, X86_REG_EDI, X86_REG_R12D, X86_REG_R13D, X86_REG_R14D, X86_REG_R15D}   # 0.1.5: 退避レジスタ経由の長さもある(後続の使用を要確認)
def imm32_form(x, L):
    """この命令が『長さLを32bit即値(命令末尾4バイト)で持つ mov』なら True"""
    if x.mnemonic != 'mov' or len(x.operands) != 2: return False
    d, s = x.operands
    if s.type != X86_OP_IMM or s.imm != L: return False
    if len(x.bytes) < 5 or int.from_bytes(x.bytes[-4:], 'little') != L: return False
    if d.type == X86_OP_MEM and d.size == 8 and d.mem.base != X86_REG_RIP: return True    # mov qword [m], imm32
    if d.type == X86_OP_REG and d.reg in REG32: return True                                # mov r32, imm32
    return False
def find_len(f, k, L):
    """lea(索引k)に対応する長さ即値を探す: 近傍の前方→後方。次のrdata参照leaの手前まで。"""
    ins, idx = decode(f)
    best = None
    for j in range(k + 1, min(len(ins), k + 9)):
        x = ins[j]
        if x.mnemonic in ('call', 'ret', 'jmp'): break
        t = ripref(x)
        if x.mnemonic == 'lea' and t is not None and rd_lo <= t < rd_hi and t in strs: break
        if imm32_form(x, L): best = (j - k, x); break
    if best is None and ins[k].op_str.startswith('rdx,'):      # std::string::append/assign(this, rdx=ptr, r8=len): 長さは先に設定される
        for j in range(k - 1, max(-1, k - 4), -1):
            x = ins[j]
            if x.mnemonic in ('call', 'ret', 'jmp'): break
            if imm32_form(x, L) and x.operands[0].type == X86_OP_REG and x.operands[0].reg == X86_REG_R8D:
                best = (j - k, x); break
    return best

# ---- 翻訳対象の VA を決める -----------------------------------------------
targets = []   # (en, ja, va)
for en, ja in T.items():
    if en in C.SKIP_KEYS: continue
    vas = rev.get(en.encode('utf-8'))
    if not vas:
        raise SystemExit('rdataに無いキー: %r' % en[:60])
    for va in vas: targets.append((en, ja, va))

claimed = {}          # 長さ即値アドレス -> lea アドレス
sites = []            # dict
slotsl = []
inline_sites = []
for en, ja, va in targets:
    L = len(en.encode()); JL = len(ja.encode('utf-8'))
    for a, x, f in refs.get(va, []):
        if (en, a) in C.SKIP_SITES: log.append(('skip-site', en, hex(a))); continue
        if x.mnemonic == 'lea' and x.size == 7 and x.disp_offset == 3:
            ins, idx = decode(f); k = idx[a]
            hit = find_len(f, k, L)
            rec = dict(kind='lea', en=en, ja=ja, va=va, addr=a, len_at=None)
            if hit:
                d, lx = hit; la = lx.address - IB
                assert la not in claimed, ('長さ即値の二重取り', hex(la), hex(a), hex(claimed[la]))
                claimed[la] = a; rec['len_at'] = la; rec['len_d'] = d
                if lx.operands[0].type == X86_OP_REG and lx.operands[0].reg in (X86_REG_EBX, X86_REG_ESI, X86_REG_EDI, X86_REG_R12D, X86_REG_R13D, X86_REG_R14D, X86_REG_R15D):
                    log.append(('calleesaved-len', hex(la), hex(a), en[:40]))
            elif '{' in en:
                raise SystemExit('書式文字列なのに長さ即値が無い: %r @%x' % (en[:40], a))
            sites.append(rec)
        else:
            inline_sites.append(dict(en=en, ja=ja, va=va, addr=a, mn=x.mnemonic))

# 特定の参照箇所だけを訳す文字列(同じ文字列が他の用途でも共有されているもの)
for en, a_, ja in C.SITE_STR:
    L_ = len(en.encode('utf-8'))
    vas_ = [v for v in rev.get(en.encode('utf-8'), []) if any(r_[0] == a_ for r_ in refs.get(v, []))]
    assert len(vas_) == 1, ('SITE_STRの参照が見つからない', en, hex(a_))
    va_ = vas_[0]; r_ = next(r_ for r_ in refs[va_] if r_[0] == a_); x_, f_ = r_[1], r_[2]
    assert x_.mnemonic == 'lea' and x_.size == 7 and x_.disp_offset == 3
    hit_ = find_len(f_, decode(f_)[1][a_], L_)
    assert hit_, ('SITE_STRの長さ即値が無い', en, hex(a_))
    la_ = hit_[1].address - IB
    assert la_ not in claimed, ('長さ即値の二重取り', hex(la_))
    claimed[la_] = a_
    sites.append(dict(kind='lea', en=en, ja=ja, va=va_, addr=a_, len_at=la_, len_d=hit_[0]))
    log.append(('site-str', en, hex(a_), hex(la_), ja))

# ---- ポインタ表スロット -----------------------------------------------------
want = {IB + va: (en, ja, va) for en, ja, va in targets}
slot_recs = []
for s in (rd, dt):
    base = s.PointerToRawData
    for o in range(0, s.SizeOfRawData - 7, 8):
        v = struct.unpack_from('<Q', raw, base + o)[0]
        if v in want:
            en, ja, va = want[v]
            rva = s.VirtualAddress + o
            assert rva in reloc, ('スロットに再配置が無い', hex(rva), en)
            nxt = struct.unpack_from('<Q', raw, base + o + 8)[0] if o + 16 <= s.SizeOfRawData else None
            slot_recs.append(dict(en=en, ja=ja, va=va, slot=rva, file=base + o, has_len=(nxt == len(en.encode()))))

print('lea sites:', len(sites), ' slots:', len(slot_recs), ' inline-candidates:', len(inline_sites))
json.dump([dict(en=r['en'], addr=hex(r['addr']), len_at=(hex(r['len_at']) if r.get('len_at') else None)) for r in sites], open(REP + '.sites', 'w'), ensure_ascii=False, indent=0)
json.dump(dict(inline=[{**i, 'addr': hex(i['addr'])} for i in inline_sites]), open(REP + '.pre', 'w'), ensure_ascii=False, indent=1)

# ---- 手動指定の長さ即値 ----------------------------------------------------
for en, la, lenaddr in C.MANUAL_LEN:
    r = next(s for s in sites if s['en'] == en and s['addr'] == la)
    assert r['len_at'] is None, ('手動指定が自動検出と二重', en)
    assert lenaddr not in claimed
    claimed[lenaddr] = la; r['len_at'] = lenaddr; r['len_d'] = 'manual'

# ---- lea 付け替え + 長さ即値 -------------------------------------------------
def patch_len_imm32(la, L, JL, label):
    o = off(la)
    ins = next(md.disasm(raw[o:o + 15], IB + la))
    assert imm32_form(ins, L), (hex(la), ins.op_str)
    fo = o + ins.size - 4
    assert u32(fo) == L
    data[fo:fo + 4] = struct.pack('<I', JL); changes.append((fo, 4, label + '@%x' % la))

n_lea = 0
for r in sites:
    a = r['addr']; en, ja = r['en'], r['ja']; JL = len(ja.encode('utf-8'))
    o = off(a); ins = next(md.disasm(raw[o:o + 15], IB + a))
    assert ins.mnemonic == 'lea' and ins.size == 7 and ins.disp_offset == 3
    tgt = a + 7 + [op for op in ins.operands if op.type == X86_OP_MEM][0].mem.disp
    assert tgt == r['va'] and strs[tgt] == en.encode('utf-8'), (hex(a), en)
    po = add(ja.encode('utf-8') + b'\0')
    disp = jva(po) - (a + 7)
    assert -2**31 <= disp < 2**31
    data[o + 3:o + 7] = struct.pack('<i', disp); changes.append((o + 3, 4, 'lea@%x' % a)); n_lea += 1
    if r.get('len_at'): patch_len_imm32(r['len_at'], len(en.encode()), JL, 'len')

assert len(T['right hand'].encode()) == len(T['left hand'].encode()) + 1, '右手/左手の長さ関係'
for en, a, kind in C.EXTRA_LEN:
    ja = T[en]; L = len(en.encode()); JL = len(ja.encode('utf-8'))
    if kind == 'imm32':
        patch_len_imm32(a, L, JL, 'xlen')
    else:
        assert JL <= 127, ('8bit即値に収まらない', en, JL)
        o = off(a); ins = next(md.disasm(raw[o:o + 15], IB + a))
        pos = [i for i in range(ins.size) if raw[o + i] == L]
        assert len(pos) >= 1, (hex(a), ins.op_str)
        p = pos[-1] if ins.mnemonic in ('cmp', 'add') else pos[0]
        assert ins.mnemonic in ('cmp', 'lea', 'mov', 'add')
        data[o + p] = JL; changes.append((o + p, 1, 'xlen8@%x' % a))

# ---- ポインタ表スロット --------------------------------------------------------
n_slot = 0
for s in slot_recs:
    po = add(s['ja'].encode('utf-8') + b'\0')
    struct.pack_into('<Q', data, s['file'], IB + jva(po)); changes.append((s['file'], 8, 'slot@%x' % s['slot']))
    if s['has_len']:
        struct.pack_into('<Q', data, s['file'] + 8, len(s['ja'].encode('utf-8'))); changes.append((s['file'] + 8, 8, 'slotlen@%x' % s['slot']))
    n_slot += 1

# ---- インライン展開された std::string の組み立てを生成関数の呼び出しへ置換 --------
tx_slack_start = al(tx.Misc_VirtualSize, 16)                 # スタブ置き場(.text末尾の空き)
tx_end = tx.SizeOfRawData
stub_off = tx_slack_start                                    # .text 内オフセット
assert all(b == 0 for b in raw[tx.PointerToRawData + tx.Misc_VirtualSize:tx.PointerToRawData + tx_end]), '.text末尾が空きでない'
stub_buf = bytearray()
def stub_va(): return tx.VirtualAddress + stub_off + len(stub_buf)

REGS = ['rax', 'rcx', 'rdx', 'rbx', 'rsp', 'rbp', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']
def enc_lea_rcx(base, disp):
    b = REGS.index(base); rex = 0x48 | (1 if b >= 8 else 0)
    d8 = -128 <= disp <= 127
    code = bytes([rex, 0x8d, (0x40 if d8 else 0x80) | (1 << 3) | (b & 7)])
    if (b & 7) == 4: code += b'\x24'                          # SIB (rsp/r12)
    return code + (struct.pack('<b', disp) if d8 else struct.pack('<i', disp))

def _modrm_mem(reg, base, disp):
    b = REGS.index(base); d8 = -128 <= disp <= 127
    out = bytes([(0x40 if d8 else 0x80) | ((reg & 7) << 3) | (b & 7)])
    if (b & 7) == 4: out += b'\x24'
    return out + (struct.pack('<b', disp) if d8 else struct.pack('<i', disp))
def enc_movabs(reg, imm):
    r = REGS.index(reg)
    return bytes([0x48 | (1 if r >= 8 else 0), 0xb8 + (r & 7)]) + struct.pack('<Q', imm)
def enc_mov_mem_reg(base, disp, reg):
    r, b = REGS.index(reg), REGS.index(base)
    return bytes([0x48 | (4 if r >= 8 else 0) | (1 if b >= 8 else 0), 0x89]) + _modrm_mem(r, base, disp)
def enc_mov_mem_imm32(base, disp, imm):
    b = REGS.index(base)
    return bytes([0x48 | (1 if b >= 8 else 0), 0xc7]) + _modrm_mem(0, base, disp) + struct.pack('<i', imm)
FAM = {}
for n, fam_ in {'rax': ['rax', 'eax', 'ax', 'al', 'ah'], 'rcx': ['rcx', 'ecx', 'cx', 'cl', 'ch'], 'rdx': ['rdx', 'edx', 'dx', 'dl', 'dh'],
                'r8': ['r8', 'r8d', 'r8w', 'r8b'], 'r9': ['r9', 'r9d', 'r9w', 'r9b'], 'r10': ['r10', 'r10d', 'r10w', 'r10b'], 'r11': ['r11', 'r11d', 'r11w', 'r11b']}.items():
    for q in fam_: FAM[q] = n
for i_ in range(6): FAM['xmm%d' % i_] = 'xmm%d' % i_
FAM['eflags'] = 'flags'
def rw(x):
    r, w = x.regs_access()
    f = lambda s: {FAM.get(md.reg_name(q)) for q in s} - {None}
    return f(r), f(w)
CALLEE = {q for r_ in ('bx','si','di') for q in ('r'+r_,'e'+r_,r_,r_[0]+'l' if r_=='bx' else r_+'l')} | {q for n_ in range(12,16) for q in ('r%d'%n_,'r%dd'%n_,'r%dw'%n_,'r%db'%n_)}
CLOB = {'rax', 'rcx', 'rdx', 'r8', 'r9', 'r10', 'r11', 'xmm0', 'xmm1', 'xmm2', 'xmm3', 'xmm4', 'xmm5', 'flags'}
def live_out(f, re_, regs):
    ins, idx = decode(f); res = {}
    for R in regs:
        seen = set(); stack = [idx[re_]]; steps = 0
        while stack and steps < 4000:
            i = stack.pop()
            if i in seen or i >= len(ins): continue
            seen.add(i); steps += 1
            x = ins[i]; r, w = rw(x)
            if x.mnemonic in ('xor', 'xorps', 'pxor') and len(x.operands) == 2 and x.operands[0].type == X86_OP_REG and x.operands[1].type == X86_OP_REG and x.operands[0].reg == x.operands[1].reg:
                r = set()
            if R in r:
                res[R] = hex(x.address - IB) + ' ' + x.mnemonic + ' ' + x.op_str; break
            if R in w: continue
            if x.mnemonic == 'call': continue        # 呼び出しで揮発レジスタは破壊される (引数読み出しは保守的に無視しない→下で別扱い)
            if x.mnemonic in ('ret',): continue
            if x.mnemonic == 'jmp':
                if x.operands[0].type == X86_OP_IMM:
                    t = x.operands[0].imm - IB
                    if t in idx: stack.append(idx[t])
                    else: res[R] = 'jump out of function'; 
                continue
            if x.mnemonic.startswith('j') and x.operands[0].type == X86_OP_IMM:
                t = x.operands[0].imm - IB
                if t in idx: stack.append(idx[t])
            stack.append(i + 1)
    return res

def branch_targets(f):
    ins, idx = decode(f); T_ = set()
    for x in ins:
        if (x.mnemonic == 'jmp' or x.mnemonic.startswith('j')) and x.operands and x.operands[0].type == X86_OP_IMM:
            T_.add(x.operands[0].imm - IB)
    return T_

INL = []   # 結果
def sso_region(site):
    en, ja, va, a = site['en'], site['ja'], site['va'], site['addr']
    L = len(en.encode()); f = func_of(a); ins, idx = decode(f); k = idx[a]; bt = branch_targets(f)
    assert L <= 15, ('SSO以外', en)
    # 先頭ロード直後のストアから格納先ウィンドウを決める
    dest = None
    for j in range(k + 1, k + 4):
        x = ins[j]
        if x.operands and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.base not in (0, X86_REG_RIP) and x.mnemonic in ('mov', 'movsd', 'movups', 'movdqu'):
            dest = (md.reg_name(x.operands[0].mem.base), x.operands[0].mem.disp); break
    assert dest, ('格納先不明', en, hex(a))
    base, d0 = dest
    def in_win(x):
        if not x.operands or x.operands[0].type != X86_OP_MEM: return False
        m = x.operands[0].mem
        return md.reg_name(m.base) == base and m.index == 0 and d0 <= m.disp < d0 + 0x20
    def is_strload(x):
        t = ripref(x)
        return t is not None and va <= t <= va + L and x.mnemonic in ('mov', 'movzx', 'movsd')
    # 後方へ
    rs_i = k; j = k - 1
    while j >= 0 and ins[j].address - IB not in bt:
        x = ins[j]
        if in_win(x) and x.mnemonic in ('movups', 'movdqu', 'mov'):
            rs_i = j
        elif x.mnemonic == 'movdqa' and ripref(x) is not None: pass
        elif x.mnemonic == 'xorps' and x.operands[0].reg == x.operands[1].reg: pass
        else: break
        j -= 1
    # 前方へ
    re_i = k; j = k
    while j < len(ins) and ins[j].address - IB not in (bt - {ins[k].address - IB} if j == k else bt):
        x = ins[j]
        if in_win(x) or is_strload(x): re_i = j
        elif j > k and x.mnemonic in ('lea', 'mov', 'jmp', 'or', 'movabs') or j > k: break
        j += 1
    # 領域内訳チェック
    rs = ins[rs_i].address - IB; re_ = ins[re_i + 1].address - IB
    assert not any(rs < t < re_ for t in bt), ('領域内へ分岐', en, hex(rs))
    wrote_xmm = set(); vec_xmm = {}
    for x in ins[rs_i:re_i + 1]:
        if in_win(x) or is_strload(x): continue
        if x.mnemonic == 'movdqa' and ripref(x) is not None:
            t = ripref(x); q = struct.unpack_from('<QQ', raw, off(t))
            vec_xmm[md.reg_name(x.operands[0].reg)] = q; continue
        if x.mnemonic == 'xorps': continue
        raise AssertionError(('領域内に想定外の命令', en, hex(x.address - IB), x.op_str))
    # NUL終端と size/cap の確認
    stores = [x for x in ins[rs_i:re_i + 1] if in_win(x)]
    assert any(x.operands[0].mem.disp == d0 + L and x.operands[0].size == 1 for x in stores), ('NUL終端ストアが無い', en)
    return dict(en=en, ja=ja, rs=rs, re=re_, base=base, d0=d0, vec=vec_xmm, f=f, L=L)


def heap_detect(site):
    """16バイト超の定数 std::string がその場で展開された領域を自動検出する(0.1.5向け)。
    形: (std::string の先頭16バイトのゼロ詰め) / mov ecx,N / call ALLOC / mov [base+d],rax (確保したポインタ) /
        size・cap の設定 / 文字列のコピー / mov byte [ptr+L],(0 か 0 を持つレジスタ)
    領域 = ゼロ詰めの先頭 〜 終端NULの書き込み。基準(base,d)は確保ポインタの格納先 = std::string オブジェクト。
    戻り値: (領域開始, 領域終了(排他), 基準レジスタ名, 変位) または None"""
    en, a = site['en'], site['addr']
    L = len(en.encode()); f = func_of(a); ins, idx = decode(f); k = idx[a]; bt = branch_targets(f)
    call_i = None
    for j in range(k - 1, max(-1, k - 14), -1):
        x = ins[j]
        if x.mnemonic == 'call' and x.operands[0].type == X86_OP_IMM and x.operands[0].imm - IB == C.ALLOC:
            call_i = j; break
    if call_i is None: return None
    st = None
    for j in range(call_i + 1, min(k, call_i + 5)):
        x = ins[j]
        if x.mnemonic == 'mov' and x.operands[0].type == X86_OP_MEM and x.operands[1].type == X86_OP_REG and x.operands[1].reg == X86_REG_RAX \
           and x.operands[0].mem.base not in (0, X86_REG_RIP) and x.operands[0].size == 8:
            st = x; break
    if st is None: return None
    base_reg = st.operands[0].mem.base; base = md.reg_name(base_reg); d0 = st.operands[0].mem.disp
    rs_i = None; j = call_i - 1
    while j >= 0 and call_i - j <= 12:
        x = ins[j]
        if x.mnemonic == 'mov' and x.operands[0].type == X86_OP_REG and x.operands[1].type == X86_OP_IMM and md.reg_name(x.operands[0].reg) == 'ecx': pass
        elif x.mnemonic in ('movups', 'mov') and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.base == base_reg and d0 <= x.operands[0].mem.disp < d0 + 0x10:
            rs_i = j       # 先頭16バイトへのゼロ詰めストア
        elif x.mnemonic == 'mov' and x.operands[0].type == X86_OP_MEM: pass
        elif x.mnemonic in ('xorps', 'xor'): pass
        else: break
        if ins[j].address - IB in bt: break
        j -= 1
    if rs_i is None:        # 先頭のゼロ詰めが無い形: mov ecx,N の直前から
        x = ins[call_i - 1]
        if x.mnemonic == 'mov' and x.operands[0].type == X86_OP_REG and md.reg_name(x.operands[0].reg) == 'ecx' and x.operands[1].type == X86_OP_IMM:
            rs_i = call_i - 1
    if rs_i is None: return None
    for t in range(rs_i + 1, call_i + 1):
        if ins[t].address - IB in bt: return None
    for j in range(k, min(len(ins) - 1, k + 22)):
        x = ins[j]
        if x.mnemonic == 'mov' and x.operands[0].type == X86_OP_MEM and x.operands[0].size == 1 and x.operands[0].mem.disp == L \
           and x.operands[0].mem.base not in (0, X86_REG_RIP, X86_REG_RSP, X86_REG_RBP):
            if x.operands[1].type == X86_OP_IMM and x.operands[1].imm != 0: return None
            return (ins[rs_i].address - IB, ins[j + 1].address - IB, base, d0)
    return None

# 対象サイトを領域単位にまとめる
regions = {}
for s in inline_sites:
    if s['en'] in C.NOT_TRANSLATED: continue
    if s['en'] in getattr(C, 'HEAP_REGIONS_KEYS', ()): continue
    regions.setdefault((s['en'], s['va']), []).append(s)
REG_LIST = []
for (en, va), ss in regions.items():
    for s in ss:
        if s['mn'] not in ('mov', 'movsd', 'movups', 'movaps', 'movzx'): raise SystemExit('未知の参照形態 %s %r' % (s['mn'], en))
        L = len(en.encode())
        if L <= 15:
            try: REG_LIST.append(sso_region(s))
            except AssertionError as e_: print('  INLINE NG', hex(s['addr']), e_.args)
        else:
            REG_LIST.append(dict(en=en, ja=s['ja'], heap=True, addr=s['addr']))
print('inline regions:', len(inline_sites))
# ---- 領域の確定 -----------------------------------------------------------------
UNRESOLVED = []
regions = {}
for s in inline_sites:
    if s['en'] in C.NOT_TRANSLATED: continue
    regions.setdefault((s['en'], s['va']), []).append(s)
REG_LIST = []
for (en, va), ss in regions.items():
    for s in ss:
        L = len(en.encode())
        if s['addr'] not in C.HEAP_REGIONS and L > 15:
            hr = heap_detect(s)
            if hr: C.HEAP_REGIONS[s['addr']] = hr
        if s['addr'] in C.HEAP_REGIONS:
            rs, re_, base, d0 = C.HEAP_REGIONS[s['addr']]
            f = func_of(rs); ins, idx = decode(f); bt = branch_targets(f)
            assert not any(rs < t < re_ for t in bt), ('領域内へ分岐', hex(rs))
            vec = {}
            for x in ins[idx[rs]:idx[re_]]:
                ok = x.mnemonic in ('movups', 'movaps', 'movdqu', 'movdqa', 'movzx', 'mov', 'xorps', 'movsd', 'xor', 'movss', 'movq', 'movd', 'lea') or (x.mnemonic == 'call' and x.op_str == '0x%x' % (IB + C.ALLOC))
                assert ok, ('ヒープ領域内に想定外の命令', hex(x.address - IB), x.mnemonic, x.op_str)
                if x.mnemonic == 'movdqa' and ripref(x) is not None:
                    vec[md.reg_name(x.operands[0].reg)] = struct.unpack_from('<QQ', raw, off(ripref(x)))
            REG_LIST.append(dict(en=en, ja=s['ja'], rs=rs, re=re_, base=base, d0=d0, vec=vec, f=f, L=L, heap=True))
        else:
            try:
                assert s['mn'] in ('mov', 'movsd', 'movups', 'movaps', 'movzx'), (s['mn'], en)
                assert L <= 15, ('SSO以外でHEAP_REGIONS未指定', en, hex(s['addr']))
                g = sso_region(s); g['heap'] = False; REG_LIST.append(g)
            except AssertionError as e_:
                UNRESOLVED.append((hex(s['addr']), en, e_.args))

# rdata に文字列が無く、命令の即値(4文字や8文字)から組み立てられる短い std::string (SSO)
for en_, rs_, re__, base_, d0_, ja_ in C.IMM_REGIONS:
    f_ = func_of(rs_); ins_, idx_ = decode(f_); bt_ = branch_targets(f_); vec_ = {}
    assert not any(rs_ < t < re__ for t in bt_), ('領域内へ分岐', hex(rs_))
    for x in ins_[idx_[rs_]:idx_[re__]]:
        if x.mnemonic == 'movdqa' and ripref(x) is not None:
            vec_[md.reg_name(x.operands[0].reg)] = struct.unpack_from('<QQ', raw, off(ripref(x)))
    REG_LIST.append(dict(en=en_, ja=ja_, rs=rs_, re=re__, base=base_, d0=d0_, vec=vec_, f=f_, L=len(en_.encode()), heap=False))
for en_, rs_, re__, base_, d0_ in C.EXTRA_HEAP:
    f_ = func_of(rs_); ins_, idx_ = decode(f_); bt_ = branch_targets(f_)
    assert not any(rs_ < t < re__ for t in bt_), ('領域内へ分岐', hex(rs_))
    assert ins_[idx_[rs_]].mnemonic == 'mov' and ins_[idx_[rs_]].op_str == 'ecx, %s' % hex(al(len(en_.encode()) + 1, 16)), ('領域の先頭が mov ecx,サイズ でない', hex(rs_))
    assert any(x.mnemonic == 'call' and x.operands[0].imm - IB == C.ALLOC for x in ins_[idx_[rs_]:idx_[re__]]), 'ALLOC 呼び出しが領域に無い'
    assert any(x.mnemonic == 'mov' and x.operands[0].type == X86_OP_MEM and x.operands[0].size == 1 and x.operands[0].mem.disp == len(en_.encode()) for x in ins_[idx_[rs_]:idx_[re__]]), 'NUL終端が領域に無い'
    assert not any(x.mnemonic in ('ret', 'jmp') or x.mnemonic.startswith('j') for x in ins_[idx_[rs_]:idx_[re__]]), '領域内に分岐'
    REG_LIST.append(dict(en=en_, ja=T[en_], rs=rs_, re=re__, base=base_, d0=d0_, vec={}, f=f_, L=len(en_.encode()), heap=True))
if UNRESOLVED:
    for u in UNRESOLVED: print('  UNRESOLVED', u)
    raise SystemExit('未解決のインライン領域: %d' % len(UNRESOLVED))
def postfix_list(rs):
    """POSTFIX[rs] は (機械語, 想定する元命令, 元アドレス) 1件、またはそのリスト(0.2.0: rcx/rdx/r8 を順に戻す箇所がある)"""
    v = C.POSTFIX[rs]
    return [v] if isinstance(v, tuple) else list(v)
def postfix_regs(rs):
    out = set()
    for pb, text, src in postfix_list(rs):
        o_ = off(src); x_ = next(md.disasm(raw[o_:o_ + 15], IB + src))
        _, w_ = rw(x_); out |= w_
    return out
# ---- 領域置換コードの生成 -----------------------------------------------------------
n_reg = 0
for g in REG_LIST:
    en, ja, rs, re_, base, d0 = g['en'], g['ja'], g['rs'], g['re'], g['base'], g['d0']
    jb = ja.encode('utf-8'); po = add(jb + b'\0')
    lo = live_out(g['f'], re_, sorted(CLOB))
    unrestorable = []
    ptr_regs = []     # 領域内で ALLOC の戻り値(rax)を写している退避レジスタ(後続が std::string のデータポインタとして使う)
    if g.get('heap'):
        _i, _x = decode(g['f'])
        for x in _i[_x[rs]:_x[re_]]:
            if x.mnemonic == 'mov' and len(x.operands) == 2 and x.operands[0].type == X86_OP_REG and x.operands[1].type == X86_OP_REG \
               and x.operands[1].reg == X86_REG_RAX and md.reg_name(x.operands[0].reg) in ('r12', 'r13', 'r14', 'r15', 'rbx', 'rsi', 'rdi'):
                ptr_regs.append(md.reg_name(x.operands[0].reg))
    code = enc_lea_rcx(base, d0)
    code += b'\x48\x8d\x15' + struct.pack('<i', jva(po) - (rs + len(code) + 7))
    code += b'\x41\xb8' + struct.pack('<I', len(jb))
    code += b'\xe8' + struct.pack('<i', C.STRCTOR - (rs + len(code) + 5))
    # 領域内で書かれ、領域後に読まれるレジスタの復元
    for R, why in sorted(lo.items()):
        if R in g['vec'] and R.startswith('xmm'):
            q = g['vec'][R]
            assert q[0] == g['L'] and q[1] >= 15 and (g.get('heap') or q[1] == 15), ('size/cap定数が想定外', R, q)
            n = int(R[3:]); assert n < 8
            code += bytes([0x0f, 0x10, 0x40 | (n << 3) | 1 if False else 0]) if False else b''
            # movups xmmN,[rcx+0x10]  (rcx は領域置換直後は壊れているので dest から再計算)
            code += enc_lea_rcx(base, d0 + 0x10) + bytes([0x0f, 0x10, (n << 3) | 1])
            log.append(('restore', R, hex(rs)))
        elif rs in C.POSTFIX and R in postfix_regs(rs):
            pass
        elif R == 'rax' and g.get('heap') and ptr_regs:
            pass          # 下で rax = 新しい std::string のデータポインタ に直す
        else:
            unrestorable.append((R, why))
    if unrestorable:
        # 0.2.0: 呼び出しで壊れる xmm 等が領域の後でも生きている → 呼び出しを使わず、15バイト以下の訳文をその場で直接書き込む
        if len(jb) > 15:
            raise SystemExit('領域後に生きているレジスタ %s (%s) を復元できない: %r @%x' % (unrestorable[0][0], unrestorable[0][1], en, rs))
        print('  direct:', en, hex(rs), unrestorable)
        scratch = next((r_ for r_ in ('rax', 'rcx', 'rdx', 'r8', 'r9', 'r10', 'r11') if r_ not in lo), None)
        assert scratch, ('作業レジスタが無い', en)
        code = b''
        pad = jb + b'\0' * (16 - len(jb))
        # 領域の直前が「xorps xmm0,xmm0; movups [base+d0],xmm0」(先頭16バイトのゼロ詰め)なら、0 の qword は書かなくてよい
        _i, _x = decode(g['f']); k0 = _x[rs]; zero_pre = False
        if k0 >= 2:
            p1, p2 = _i[k0 - 1], _i[k0 - 2]
            if p1.mnemonic == 'movups' and p1.operands[0].type == X86_OP_MEM and md.reg_name(p1.operands[0].mem.base) == base and p1.operands[0].mem.disp == d0 \
               and p1.operands[1].type == X86_OP_REG and p1.operands[1].reg == X86_REG_XMM0 and p2.mnemonic == 'xorps' and p2.operands[0].reg == p2.operands[1].reg == X86_REG_XMM0:
                zero_pre = True
        for k_ in (0, 8):
            q_ = struct.unpack_from('<Q', pad, k_)[0]
            if q_ == 0 and zero_pre: continue
            code += enc_movabs(scratch, q_) + enc_mov_mem_reg(base, d0 + k_, scratch)
        code += enc_mov_mem_imm32(base, d0 + 0x10, len(jb)) + enc_mov_mem_imm32(base, d0 + 0x18, 15)
        for R, why in sorted(lo.items()):       # 領域内の movdqa で作った size/cap 定数のレジスタは読み直す
            if R in g['vec'] and R.startswith('xmm'):
                code += bytes([0x0f, 0x10]) + _modrm_mem(int(R[3:]), base, d0 + 0x10)
        log.append(('direct', en, hex(rs), scratch, 'live-out=' + ','.join(sorted(lo))))
    elif rs in C.POSTFIX:
        for pb, text, src in postfix_list(rs):
            o_ = off(src); x_ = next(md.disasm(raw[o_:o_ + 15], IB + src))
            assert x_.mnemonic + ' ' + x_.op_str == text and bytes(x_.bytes) == pb, ('POSTFIX元命令が一致しない', hex(src))
            code += pb
    if ptr_regs and not unrestorable:
        # std::string のデータポインタ: 訳文が16バイト以上ならヒープ上([オブジェクト]の先頭8バイト)、以下ならオブジェクト自身
        op_ = 0x8b if len(jb) > 15 else 0x8d
        for R_ in (['rax'] if 'rax' in lo else []) + ptr_regs:
            r_ = REGS.index(R_); b_ = REGS.index(base)
            code += bytes([0x48 | (4 if r_ >= 8 else 0) | (1 if b_ >= 8 else 0), op_]) + _modrm_mem(r_, base, d0)
        log.append(('ptrregs', en, hex(rs), ','.join(ptr_regs), 'rax' if 'rax' in lo else '-'))
    # 領域内で退避レジスタ(rbx/rsi/rdi/r12-r15)へ書かれた値(xor r,r / mov r,imm)は領域後も使われうるので、そのまま書き直す
    ins_, idx_ = decode(g['f'])
    for x in ins_[idx_[rs]:idx_[re_]]:
        if x.mnemonic not in ('xor', 'mov') or any(op.type == X86_OP_MEM for op in x.operands): continue
        _, w_ = x.regs_access()
        if {md.reg_name(q) for q in w_} & CALLEE:
            if ptr_regs and x.mnemonic == 'mov' and x.operands[1].type == X86_OP_REG and md.reg_name(x.operands[0].reg) in ptr_regs: continue
            assert x.mnemonic == 'xor' and x.operands[0].reg == x.operands[1].reg or x.operands[1].type == X86_OP_IMM, ('退避レジスタ書き込みが単純でない', hex(x.address - IB))
            code += bytes(x.bytes); log.append(('reemit', hex(x.address - IB), x.mnemonic + ' ' + x.op_str))
    size = re_ - rs
    assert len(code) <= size, ('置換コードが領域に収まらない', en, len(code), size)
    code += b'\x90' * (size - len(code))
    fo = off(rs); data[fo:fo + size] = code; changes.append((fo, size, 'inline@%x' % rs)); n_reg += 1
    log.append(('inline', en, hex(rs), hex(re_), base, hex(d0) if d0 >= 0 else '-' + hex(-d0), 'live-out=' + ','.join(sorted(lo))))
print('inline replaced:', n_reg)

# ---- ツールチップ(DrawTip)の拡大: 係数 15.0 / 300.0 を FONT_SCALE 倍した定数へ付け替える ----------
for a_, v_ in C.TIP_CONSTS:
    o_ = off(a_); x_ = next(md.disasm(raw[o_:o_ + 15], IB + a_))
    assert x_.mnemonic == 'mulss' and x_.size == 9 and x_.disp_offset == 5, (hex(a_), x_.op_str)
    t_ = a_ + 9 + [op for op in x_.operands if op.type == X86_OP_MEM][0].mem.disp
    assert struct.unpack_from('<f', raw, off(t_))[0] == v_, ('DrawTip係数が想定と違う', hex(a_))
    assert sec_of(a_) is tx and func_of(a_) is not None
    po_ = add(struct.pack('<f', v_ * C.TIP_SCALE))
    data[o_ + 5:o_ + 9] = struct.pack('<i', jva(po_) - (a_ + 9)); changes.append((o_ + 5, 4, 'tip@%x' % a_))
    log.append(('tip', hex(a_), v_, round(v_ * C.TIP_SCALE, 3)))

# ---- 文字拡大で重なる箇所の間隔(mulss xmm,[rip+定数]) ---------------------------------------
for a_, v_, nv_ in C.SPACING_CONSTS:
    o_ = off(a_); x_ = next(md.disasm(raw[o_:o_ + 15], IB + a_))
    assert x_.mnemonic == 'mulss' and x_.size == 9 and x_.disp_offset == 5, (hex(a_), x_.op_str)
    t_ = a_ + 9 + [op for op in x_.operands if op.type == X86_OP_MEM][0].mem.disp
    assert struct.unpack_from('<f', raw, off(t_))[0] == v_, ('間隔の係数が想定と違う', hex(a_))
    assert sec_of(a_) is tx and func_of(a_) is not None
    po_ = add(struct.pack('<f', nv_))
    data[o_ + 5:o_ + 9] = struct.pack('<i', jva(po_) - (a_ + 9)); changes.append((o_ + 5, 4, 'space@%x' % a_))
    log.append(('space', hex(a_), v_, nv_))

# ---- Label / LabelWidth / Text / TextSize / Paragraph スタブ ---------------------------------
# 非ASCIIを含む文字列のときだけ Text / TextSize へ振り分け(Label/LabelWidth)、
# 日本語のときだけ文字サイズを C.FONT_SCALE 倍する(題字を除く)。ASCIIのみなら原関数へそのまま飛ぶ。
# スタブは新設の .jpn セクション(読み取り+実行)の末尾に置く。
def rel32(src_end, dst): return struct.pack('<i', dst - src_end)
while len(pool) % 16: pool.append(0)
stub_base = new_va + len(pool)
sb = bytearray()                                    # スタブ領域(.jpn内オフセット = len(pool) + len(sb))
def sva(): return stub_base + len(sb)
# 共通ヘルパ: r9=ptr, r10=len -> CF=1 なら非ASCIIを含む。破壊: r9, r10, flags
helper_va = sva()
sb += b'\x4d\x85\xd2'                               # test r10, r10
sb += b'\x74\x0e'                                   # jz  -> clc; ret
sb += b'\x41\x80\x39\x80'                           # cmp byte ptr [r9], 0x80
sb += b'\x73\x0a'                                   # jae -> stc; ret
sb += b'\x49\xff\xc1\x49\xff\xca'                   # inc r9; dec r10
sb += b'\xeb\xed'                                   # jmp top
sb += b'\xf8\xc3'                                   # clc; ret
sb += b'\xf9\xc3'                                   # stc; ret
# 注: jz は 'clc;ret'(+0x0c相当)へ、jae は 'stc;ret' へ飛ぶ。位置を検証する
assert len(sb) == 23 and sb[19:23] == b'\xf8\xc3\xf9\xc3'
while len(sb) % 4: sb.append(0xcc)
factor_va = sva(); sb += struct.pack('<f', C.FONT_SCALE)
while len(sb) % 16: sb.append(0xcc)
LOAD_STACK5 = b'\x48\x8b\x44\x24\x28' b'\x4c\x8b\x08' b'\x4c\x8b\x50\x08'   # mov rax,[rsp+28h]; mov r9,[rax]; mov r10,[rax+8]
LOAD_RDX = b'\x4c\x8b\x0a' b'\x4c\x8b\x52\x08'                              # mov r9,[rdx]; mov r10,[rdx+8]
def mulss_xmm(n):          # mulss xmmN, [rip+factor]  (N=0 or 3)
    modrm = {0: 0x05, 3: 0x1d}[n]
    c = bytes([0xf3, 0x0f, 0x59, modrm]); return c + rel32(sva_now + len(c) + 4, factor_va)
def make_stub(load, ascii_to, non, scale_xmm=None):
    """non: ('jmp', 目的アドレス) または ('ts',)  = TextSize を呼んで幅(x)を xmm0 に返す"""
    global sva_now
    start = sva(); code = bytearray(load)
    code += b'\xe8' + rel32(start + len(code) + 5, helper_va)    # call helper
    jc_at = len(code); code += b'\x72\x00'                       # jc nonascii
    code += b'\xe9' + rel32(start + len(code) + 5, ascii_to)      # jmp ascii target
    code[jc_at + 1] = len(code) - (jc_at + 2)
    if scale_xmm is not None:
        sva_now = start + len(code); code += mulss_xmm(scale_xmm)
    if non[0] == 'jmp':
        code += b'\xe9' + rel32(start + len(code) + 5, non[1])
    else:
        code += b'\x48\x83\xec\x28'                                       # sub rsp,28h
        code += b'\xe8' + rel32(start + len(code) + 5, C.TEXTSIZE_VA)     # call TextSize (xmm0=size, rdx=string_view*)
        code += b'\x66\x0f\x6e\xc0'                                       # movd xmm0, eax
        code += b'\x48\x83\xc4\x28\xc3'                                   # add rsp,28h; ret
    sb.extend(code)
    while len(sb) % 16: sb.append(0xcc)
    return start
sva_now = 0
IBR = lambda a: new_va  # placeholder (未使用)
C.TEXTSIZE_VA = C.TEXTSIZE
def T_(a): return a
st_label_plain = make_stub(LOAD_STACK5, T_(C.LABEL), ('jmp', T_(C.TEXT)))
st_label_s = make_stub(LOAD_STACK5, T_(C.LABEL), ('jmp', T_(C.TEXT)), 3)
st_lw_plain = make_stub(LOAD_RDX, T_(C.LABELWIDTH), ('ts',))
st_lw_s = make_stub(LOAD_RDX, T_(C.LABELWIDTH), ('ts',), 0)
st_text_s = make_stub(LOAD_STACK5, T_(C.TEXT), ('jmp', T_(C.TEXT)), 3)
st_para_s = 0
st_ts_s = make_stub(LOAD_RDX, T_(C.TEXTSIZE), ('jmp', T_(C.TEXTSIZE)), 0)
# 世界座標ラベル(TextOnWorld)の y を size*係数 だけ上へずらす中継スタブ: rdx=pos(x低32bit,y高32bit), xmm3=size。rsp は変えず jmp で原関数へ。
world_stubs = {}
for call_a, lift in C.WORLD_LABEL_LIFT:
    while len(sb) % 16: sb.append(0xcc)
    k_va = sva(); sb += struct.pack('<f', lift)
    while len(sb) % 16: sb.append(0xcc)
    st = sva()
    sb += b'\x48\x89\xd0'                       # mov rax, rdx
    sb += b'\x48\xc1\xe8\x20'                   # shr rax, 32      (y のビット列)
    sb += b'\x66\x0f\x6e\xe0'                   # movd xmm4, eax
    sb += b'\x0f\x28\xeb'                       # movaps xmm5, xmm3
    sb += b'\xf3\x0f\x59\x2d' + rel32(sva() + 8, k_va)   # mulss xmm5, [rip+k]
    sb += b'\xf3\x0f\x5c\xe5'                   # subss xmm4, xmm5
    sb += b'\x66\x0f\x7e\xe0'                   # movd eax, xmm4
    sb += b'\x48\xc1\xe0\x20'                   # shl rax, 32
    sb += b'\x89\xd2'                           # mov edx, edx     (上位を0に)
    sb += b'\x48\x09\xc2'                       # or rdx, rax
    sb += b'\xe9' + rel32(sva() + 5, C.TEXTONWORLD)   # jmp TextOnWorld
    world_stubs[call_a] = st
pool.extend(sb)

# 題字(YOUR PARTY / BATTLE PLAN)を描く Label/LabelWidth 呼び出しは拡大しない。題字を持つ関数であることを確認する。
title_fn = {func_of(a_) for a_ in C.TITLE_CALLS}
assert len(title_fn) == 1, '題字呼び出しが複数の関数にまたがる'
tf = next(iter(title_fn))
title_leas = {a for k in ('YOUR PARTY', 'BATTLE PLAN') for v in rev[k.encode()] for a, x, f in refs.get(v, []) if f == tf}
assert len(title_leas) == 2, ('題字の参照が見つからない', title_leas)

def retarget_calls(target, plain, scaled, label):
    n = 0
    for f in funcs:
        for x in decode(f)[0]:
            if x.mnemonic == 'call' and x.operands[0].type == X86_OP_IMM and x.operands[0].imm - IB == target:
                a_ = x.address - IB
                dst = plain if (a_ in C.TITLE_CALLS and plain) else scaled
                o = off(a_)
                assert raw[o] == 0xe8
                data[o + 1:o + 5] = rel32(a_ + 5, dst); changes.append((o + 1, 4, label + '@%x' % a_)); n += 1
    return n
n_cl = retarget_calls(C.LABEL, st_label_plain, st_label_s, 'callLabel')
n_cw = retarget_calls(C.LABELWIDTH, st_lw_plain, st_lw_s, 'callLabelWidth')
n_ct = retarget_calls(C.TEXT, None, st_text_s, 'callText')
n_cs = retarget_calls(C.TEXTSIZE, None, st_ts_s, 'callTextSize')
for call_a, st in world_stubs.items():
    o = off(call_a); assert raw[o] == 0xe8, hex(call_a)
    tgt_ = call_a + 5 + struct.unpack_from('<i', raw, o + 1)[0]
    assert tgt_ == C.TEXTONWORLD, ('TextOnWorld呼び出しでない', hex(call_a), hex(tgt_))
    data[o + 1:o + 5] = rel32(call_a + 5, st); changes.append((o + 1, 4, 'callWorldLabel@%x' % call_a))
n_cp = 0   # Paragraph は DrawTip からのみ呼ばれ、DrawTip の係数側で拡大済み
print('calls retargeted: Label %d LabelWidth %d Text %d TextSize %d Paragraph %d' % (n_cl, n_cw, n_ct, n_cs, n_cp))
stub_label_va, stub_lw_va = st_label_plain, st_lw_plain

# ---- .jpn セクション追加 --------------------------------------------------------------
while len(pool) % 16: pool.append(0)
pool_raw = al(len(pool), FA)
elf = pe.DOS_HEADER.e_lfanew
nsec_o = elf + 6
nsec = struct.unpack_from('<H', data, nsec_o)[0]
soh = struct.unpack_from('<H', data, elf + 20)[0]
tbl = elf + 24 + soh
hdr_end = tbl + nsec * 40
assert hdr_end + 40 <= min(s.PointerToRawData for s in secs), 'セクションヘッダの空きが無い'
assert all(b == 0 for b in data[hdr_end:hdr_end + 40])
hdr = b'.jpn\0\0\0\0' + struct.pack('<IIIIIIHHI', len(pool), new_va, pool_raw, new_raw, 0, 0, 0, 0, 0x60000060)
data[hdr_end:hdr_end + 40] = hdr; changes.append((hdr_end, 40, 'section-header'))
struct.pack_into('<H', data, nsec_o, nsec + 1); changes.append((nsec_o, 2, 'NumberOfSections'))
soi = elf + 24 + 56
struct.pack_into('<I', data, soi, al(new_va + len(pool), SA)); changes.append((soi, 4, 'SizeOfImage'))
struct.pack_into('<I', data, elf + 24 + 64, 0); changes.append((elf + 24 + 64, 4, 'CheckSum'))
assert len(data) == new_raw
data.extend(pool + b'\0' * (pool_raw - len(pool)))
open(OUT, 'wb').write(data)
print('出力:', OUT, len(data), 'bytes; .jpn VA=0x%x size=0x%x; stubs at 0x%x/0x%x' % (new_va, len(pool), stub_label_va, stub_lw_va))
json.dump(dict(src=SRC, jpn_va=new_va, jpn_size=len(pool), stub_label=stub_label_va, stub_labelwidth=stub_lw_va, font_scale=C.FONT_SCALE,
               stubs=dict(label_plain=st_label_plain, label_s=st_label_s, lw_plain=st_lw_plain, lw_s=st_lw_s, text_s=st_text_s, para_s=st_para_s, ts_s=st_ts_s),
               n_lea=n_lea, n_slot=n_slot, n_region=n_reg, n_label_calls=n_cl, n_labelwidth_calls=n_cw,
               changes=[(hex(a), n, l) for a, n, l in changes], log=[list(map(str, x)) for x in log]),
          open(REP, 'w'), ensure_ascii=False, indent=1)
