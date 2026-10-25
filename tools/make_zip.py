# -*- coding: utf-8 -*-
"""テスト版 zip と、Nexus 配布用 zip を作る(Python の zipfile 使用。パス区切りと改行を揃える)。
使い方(リポジトリのルートから):
  python3 -I tools/make_zip.py test    out/test<N>.dll <N> --memo memo.txt            -> out/FWM_Paths_test<N>.zip
  python3 -I tools/make_zip.py release fwm   out/test<N>.dll --version 0.3.0-2 --notices <THIRD-PARTY-NOTICES.md>
  python3 -I tools/make_zip.py release paths out/test<N>.dll --version 0.1.0-1 --notices <THIRD-PARTY-NOTICES.md>
release は release/README_{Japanese,English}.{fwm,paths}.txt を雛形に使い、{ORIG_SHA}/{OUT_SHA} を埋める。
README の 1 行目に --version が含まれていなければ失敗する(Nexus の版と README の版の食い違いを防ぐ)。
元DLLの SHA-256 は tools/fwm_patch.py の ORIG_SHA256 から読む。--notices は原作(fatalCMD/fight-with-me)の THIRD-PARTY-NOTICES.md。"""
import argparse, hashlib, os, re, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = {'fwm': 'Fight With Me - Japanese Translations Patch', 'paths': 'Paths - Japanese Translations Patch'}

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def orig_sha():
    m = re.search(r"ORIG_SHA256\s*=\s*'([0-9a-f]{64})'", open(os.path.join(ROOT, 'tools', 'fwm_patch.py'), encoding='utf-8').read())
    if not m: raise SystemExit('tools/fwm_patch.py に ORIG_SHA256 が見つかりません')
    return m.group(1)

def put(z, arcname, data):
    zi = zipfile.ZipInfo(arcname, (2026, 1, 1, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16
    z.writestr(zi, data)

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='mode', required=True)
    t = sub.add_parser('test'); t.add_argument('dll'); t.add_argument('n'); t.add_argument('--memo', required=True); t.add_argument('--out', default='out')
    r = sub.add_parser('release'); r.add_argument('page', choices=['fwm', 'paths']); r.add_argument('dll'); r.add_argument('--version', required=True); r.add_argument('--notices', required=True); r.add_argument('--out', default='out')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    dll = open(a.dll, 'rb').read()
    if a.mode == 'test':
        memo = open(a.memo, encoding='utf-8').read().replace('\r\n', '\n')
        path = os.path.join(a.out, 'FWM_Paths_test%s.zip' % a.n)
        with zipfile.ZipFile(path, 'w') as z:
            put(z, 'SKSE/Plugins/FightWithMe.dll', dll)
            put(z, 'テスト用メモ.txt', memo.encode('utf-8'))
        print(path); return
    o, n = orig_sha(), hashlib.sha256(dll).hexdigest()
    path = os.path.join(a.out, '%s %s.zip' % (NAMES[a.page], a.version))
    entries = [('SKSE/Plugins/FightWithMe.dll', dll)]
    for lang in ('Japanese', 'English'):
        s = open(os.path.join(ROOT, 'release', 'README_%s.%s.txt' % (lang, a.page)), encoding='utf-8').read()
        s = s.replace('{ORIG_SHA}', o).replace('{OUT_SHA}', n)
        left = re.findall(r'\{[A-Z_]+\}', s)
        if left: raise SystemExit('未解決のプレースホルダ: %s' % left)
        first = s.split('\n', 1)[0]
        if a.version not in first: raise SystemExit('README(%s)の1行目に版 %s がありません(雛形を直してください): %s' % (lang, a.version, first))
        entries.append(('README_%s.txt' % lang, s.replace('\r\n', '\n').encode('utf-8')))
    entries.append(('THIRD-PARTY-NOTICES_FightWithMe.md', open(a.notices, 'rb').read()))
    with zipfile.ZipFile(path, 'w') as z:    # すべての検査が済んでから書く(失敗時に中途半端な zip を残さない)
        for name, data in entries: put(z, name, data)
    print(path, 'SHA-256 of DLL:', n)

if __name__ == '__main__':
    main()
