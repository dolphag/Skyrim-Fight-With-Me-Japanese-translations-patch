#!/usr/bin/env python3
"""FWM 0.5.0 / Paths 1.0 以降用: 公式の翻訳ファイル機構向けに *_JAPANESE.txt を作る。

原 MOD の翻訳テンプレート(英語<TAB>英語)を原作の zip から読み、translations_en_ja.csv の訳を当てはめる。
DLL には触れない(0.3.0 までの DLL パッチ方式とは別物)。

  python3 -I tools/lang_build.py --fwm <FWM の zip> --paths <Paths の zip> --out out/ja [--no-wrap]

出力(--out の下):
  SKSE/Plugins/FightWithMe/Translations/FightWithMe_JAPANESE.txt       FWM 本体と、Paths 同梱の FightWithMe_ENGLISH.txt の鍵の和集合
  SKSE/Plugins/FightWithMe/Translations/FightWithMePaths_JAPANESE.txt  Paths のツリーの文言

検査(1 つでも失敗すると非 0 で終了):
  - テンプレートの全項目に訳がある(英語のままにする項目は CSV で ja を en と同じにする)
  - 書式欄 {} {:.0f} {0} などの種類と順序が英語と一致する(番号付きは対応が一致する)
  - 漢字が tools/jp_kanji.txt の範囲内
  - CSV に、テンプレートに無い項目(古い版の残り)が無い(--allow-stale で警告に格下げ)
"""
import argparse
import csv
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TPL_DIR = 'SKSE/Plugins/FightWithMe/Translations/'
MAXSEG = 18  # 折り返し用スペースを入れる 1 区間の最大幅(全角 1 文字 = 1、{..} = 2)

FIELD = re.compile(r'\{([0-9]*)((?::[^{}]*)?)\}')
CJK = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')


def unesc(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s) and s[i + 1] in 'nt\\':
            out.append({'n': '\n', 't': '\t', '\\': '\\'}[s[i + 1]])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return ''.join(out)


def esc(s):
    return s.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t')


def read_template(data):
    """テンプレートの(鍵, 節の見出し)を順に返す。鍵は \\n などを戻した文字列。"""
    out, sec = [], ''
    for line in data.decode('utf-8-sig').split('\n'):
        line = line.rstrip('\r')
        if line.startswith('# ') and ('/' in line):
            sec = line
        if not line or line.startswith('#'):
            continue
        out.append(unesc(line.partition('\t')[0]))
    return out


def fields(s):
    """[(番号 or None, 書式)] を出現順に返す。"""
    return [(int(m.group(1)) if m.group(1) else None, m.group(2)) for m in FIELD.finditer(s)]


def field_problem(en, ja):
    fe, fj = fields(en), fields(ja)
    if any(i is not None for i, _ in fe):
        return 'English has numbered fields'  # 英語側が番号付きなら人が見る
    specs = [s for _, s in fe]
    if all(i is None for i, _ in fj):
        return None if [s for _, s in fj] == specs else f'fields {specs} != {[s for _, s in fj]}'
    if any(i is None for i, _ in fj):
        return 'automatic and numbered fields mixed'
    # 番号付き: 各番号が英語の何番目に当たるか。使わない番号があってはならない。
    used = {}
    for i, s in fj:
        if i >= len(specs):
            return f'index {i} out of range'
        if specs[i] != s:
            return f'field {i}: {specs[i]!r} != {s!r}'
        used[i] = True
    return None if len(used) == len(specs) else 'a field is missing'


def load_kanji():
    return set(open(os.path.join(HERE, 'jp_kanji.txt'), encoding='utf-8').read().strip())


def load_csv(path):
    tbl = {}
    for r in csv.reader(open(path, encoding='utf-8-sig', newline='')):
        if r and r[0] != 'en':
            tbl[r[0]] = r[1]
    return tbl


# --- 折り返し用スペース --------------------------------------------------------
# ImGui の折り返しは ASCII スペースでしか起きない。日本語の長文は文節の切れ目にスペースを入れる(janome)。
_tok = None
_UNIT = re.compile(r'\{[^}]*\}|.', re.S)


def _tokenizer():
    global _tok
    if _tok is None:
        try:
            from janome.tokenizer import Tokenizer
        except ImportError:
            sys.exit('janome が必要です: pip install -r requirements-dev.txt')
        _tok = Tokenizer()
    return _tok


def _cands(units):
    masked = ''.join('〇' if u[0] == '{' else u for u in units)
    ok, pos = set(), 0
    for t in _tokenizer().tokenize(masked):
        pos += len(t.surface)
        if t.part_of_speech.startswith('助詞'):
            ok.add(pos)
    for i, u in enumerate(units):
        if u == '（':
            ok.add(i)
    res = []
    for i in ok:
        if i <= 0 or i >= len(units):
            continue
        a, b = units[i - 1], units[i]
        if a.isascii() and b.isascii():
            continue
        if b in '。、）」』・：:,.!?%％' or a in '（「『':
            continue
        res.append(i)
    return res


def _w(units):
    return sum(2 if u[0] == '{' else 1 for u in units)


def _split_units(units):
    if _w(units) <= MAXSEG:
        return [units]
    c = _cands(units)
    if not c:
        return [units]
    tot = _w(units)
    i = min(c, key=lambda i: abs(_w(units[:i]) - tot / 2))
    return _split_units(units[:i]) + _split_units(units[i:])


def wrapfix_line(v):
    if len(v) < MAXSEG + 1 or not CJK.search(v):
        return v
    v = re.sub(r'([、。：])(?=[^\s])', r'\1 ', v)  # 句読点・コロンの後ろ
    out = []
    for seg in v.split(' '):
        out += [''.join(x) for x in _split_units(_UNIT.findall(seg))]
    return ' '.join(out)


def wrapfix(v):
    return '\n'.join(wrapfix_line(l) for l in v.split('\n'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--fwm', required=True, help='Fight With Me の zip(FightWithMe_ENGLISH.txt を含む)')
    ap.add_argument('--paths', required=True, help='Path of the Companions の zip')
    ap.add_argument('--csv', default=os.path.join(ROOT, 'translations_en_ja.csv'))
    ap.add_argument('--out', required=True)
    ap.add_argument('--no-wrap', action='store_true', help='折り返し用スペースを入れない')
    ap.add_argument('--allow-stale', action='store_true')
    a = ap.parse_args()

    def member(zpath, name):
        with zipfile.ZipFile(zpath) as z:
            return z.read(TPL_DIR + name)

    fwm = read_template(member(a.fwm, 'FightWithMe_ENGLISH.txt'))
    pfw = read_template(member(a.paths, 'FightWithMe_ENGLISH.txt'))
    pp = read_template(member(a.paths, 'FightWithMePaths_ENGLISH.txt'))
    keys_fwm = list(dict.fromkeys(fwm + pfw))
    keys_pp = list(dict.fromkeys(pp))
    allkeys = list(dict.fromkeys(keys_fwm + keys_pp))

    tbl = load_csv(a.csv)
    kanji = load_kanji()
    bad = []
    for k in allkeys:
        if k not in tbl:
            bad.append(f'未訳: {k!r}')
            continue
        v = tbl[k]
        p = field_problem(k, v)
        if p:
            bad.append(f'書式: {p}\n    en: {k!r}\n    ja: {v!r}')
        out = sorted({c for c in CJK.findall(v) if c not in kanji})
        if out:
            bad.append(f'漢字が範囲外 {"".join(out)}: {v!r}')
        if v == '':
            bad.append(f'訳が空(英語のままにするなら en と同じ値にする): {k!r}')
    stale = [k for k in tbl if k not in set(allkeys)]
    for k in stale:
        (print if a.allow_stale else bad.append)(f'テンプレートに無い項目: {k!r}')
    if bad:
        print('\n'.join(bad))
        sys.exit(f'{len(bad)} 件の問題があります')

    def render(keys, title):
        head = [
            '# English<TAB>Translation. 日本語訳 / Japanese translation.',
            f'# {title}',
            '# 原 MOD: Fight With Me / Path of the Companions, by hashhbbrown (GitHub: fatalCMD).',
            '# 左側の英語は原 MOD のものです。右側が日本語訳です。',
            '# SKSEMenuFramework.ini の [Fonts] で EnableJapanese などを有効にしてください(README 参照)。',
            '',
        ]
        lines = []
        for k in keys:
            v = tbl[k]
            if not a.no_wrap and v != k:
                v = wrapfix(v)
            lines.append(f'{esc(k)}\t{esc(v)}')
        return '\ufeff' + '\n'.join(head + lines) + '\n'

    d = os.path.join(a.out, TPL_DIR)
    os.makedirs(d, exist_ok=True)
    files = {
        'FightWithMe_JAPANESE.txt': render(keys_fwm, 'Fight With Me (Paths 同梱分を含む)'),
        'FightWithMePaths_JAPANESE.txt': render(keys_pp, 'Path of the Companions: ツリー・アビリティ・特性'),
    }
    for name, text in files.items():
        with open(os.path.join(d, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        print(f'{name}: {text.count(chr(10)) - 6} 行')
    print(f'項目 {len(allkeys)}(FWM {len(keys_fwm)} / Paths {len(keys_pp)})')


if __name__ == '__main__':
    main()
