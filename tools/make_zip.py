# -*- coding: utf-8 -*-
"""テスト版 zip と、Nexus 配布用 zip(翻訳パッチ・日本語フォント)を作る。Fight With Me 用。DLL は含まない。
先に tools/lang_build.py で <dir>/SKSE/Plugins/FightWithMe/Translations/FightWithMe_JAPANESE.txt を作っておく。

使い方(リポジトリのルートから):
  python3 -I tools/make_zip.py test    out/ja <N> --memo memo.txt [--font-dir out/font]   -> out/FWM_ja_test<N>.zip
  python3 -I tools/make_zip.py release out/ja --font-dir out/font --version 0.5.0-1

zip の中身:
  release : SKSE/Plugins/Fonts/*.ttf + FONT-LICENSE.txt + FightWithMe_JAPANESE.txt + README_Japanese.txt / README_English.txt
release は release/README_{Japanese,English}.txt を雛形に使う。日本語フォントは同じ zip に入れる(Nexus で 2 ファイルに分けると、同じページ名の MOD として入れるときに「一つにまとめる/置き換える」のダイアログが出て混乱するため)。
{SHA_JA} は訳文ファイルの SHA-256 で埋まる。README の 1 行目に --version が含まれていなければ失敗する
(Nexus の版と README の版の食い違いを防ぐ)。"""
import argparse, hashlib, os, re, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = 'SKSE/Plugins/FightWithMe/Translations/'
OUT_FILE = 'FightWithMe_JAPANESE.txt'
NAME = 'Fight With Me'
PREFIX = 'FWM'
FONT_FILES = ['Lora-SemiBold.ttf', 'Spectral-SemiBold.ttf', 'BarlowSemiCondensed-SemiBold.ttf']


def sha(b): return hashlib.sha256(b).hexdigest()


def put(z, arcname, data):
    zi = zipfile.ZipInfo(arcname, (2026, 1, 1, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16
    z.writestr(zi, data)


def load_text(d):
    p = os.path.join(d, TPL, OUT_FILE)
    if not os.path.isfile(p): raise SystemExit('見つかりません: %s(先に tools/lang_build.py を実行)' % p)
    return [(TPL + OUT_FILE, open(p, 'rb').read())]


def load_fonts(d):
    out = []
    for n in FONT_FILES:
        p = os.path.join(d, n)
        if not os.path.isfile(p): raise SystemExit('見つかりません: %s(先に tools/make_font_pack.py を実行)' % p)
        out.append(('SKSE/Plugins/Fonts/' + n, open(p, 'rb').read()))
    p = os.path.join(d, 'FONT-LICENSE.txt')
    if not os.path.isfile(p): raise SystemExit('FONT-LICENSE.txt がありません(OFL の全文を同梱する必要があります)')
    out.append(('FONT-LICENSE.txt', open(p, 'rb').read()))
    return out


def readmes(stem, version, subs):
    out = []
    for lang in ('Japanese', 'English'):
        s = open(os.path.join(ROOT, 'release', 'README_%s%s.txt' % (stem, lang)), encoding='utf-8').read()
        for k, v in subs.items(): s = s.replace(k, v)
        left = re.findall(r'\{[A-Z_]+\}', s)
        if left: raise SystemExit('未解決のプレースホルダ: %s' % left)
        first = s.split('\n', 1)[0]
        if version not in first: raise SystemExit('README(%s)の1行目に版 %s がありません(雛形を直してください): %s' % (lang, version, first))
        out.append(('README_%s.txt' % lang, s.replace('\r\n', '\n').encode('utf-8')))
    return out


def write(path, entries):
    with zipfile.ZipFile(path, 'w') as z:    # すべての検査が済んでから書く(失敗時に中途半端な zip を残さない)
        for name, data in entries: put(z, name, data)
    print(path)
    for name, data in entries: print('  ', name, len(data), sha(data)[:12])


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='mode', required=True)
    t = sub.add_parser('test'); t.add_argument('dir'); t.add_argument('n'); t.add_argument('--memo', required=True); t.add_argument('--out', default='out')
    t.add_argument('--font-dir', help='tools/make_font_pack.py の出力。あれば SKSE/Plugins/Fonts/ に入れる')
    r = sub.add_parser('release'); r.add_argument('dir'); r.add_argument('--font-dir', required=True, help='tools/make_font_pack.py の出力(日本語フォント。同梱する)'); r.add_argument('--version', required=True); r.add_argument('--out', default='out')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.mode == 'test':
        memo = open(a.memo, encoding='utf-8').read().replace('\r\n', '\n')
        entries = load_text(a.dir) + (load_fonts(a.font_dir) if a.font_dir else []) + [('テスト用メモ.txt', memo.encode('utf-8'))]
        write(os.path.join(a.out, '%s_ja_test%s.zip' % (PREFIX, a.n)), entries)
    else:
        text = load_text(a.dir)
        entries = text + load_fonts(a.font_dir) + readmes('', a.version, {'{SHA_JA}': sha(text[0][1])})
        write(os.path.join(a.out, '%s - Japanese Translations Patch %s.zip' % (NAME, a.version)), entries)


if __name__ == '__main__':
    main()
