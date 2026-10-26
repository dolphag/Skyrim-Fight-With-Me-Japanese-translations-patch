# -*- coding: utf-8 -*-
"""テスト版 zip と、Nexus 配布用 zip を作る(FWM 0.5.0 / Paths 1.0 以降: 翻訳テキストのみ。DLL は含まない)。
先に tools/lang_build.py で <dir>/SKSE/Plugins/FightWithMe/Translations/*_JAPANESE.txt を作っておく。

使い方(リポジトリのルートから):
  python3 -I tools/make_zip.py test    out/ja <N> --memo memo.txt            -> out/FWM_Paths_ja_test<N>.zip
  python3 -I tools/make_zip.py release fwm   out/ja --version 0.5.0-1
  python3 -I tools/make_zip.py release paths out/ja --version 1.0.0-1

zip の中身:
  fwm   : FightWithMe_JAPANESE.txt                              + README_Japanese.txt / README_English.txt
  paths : FightWithMe_JAPANESE.txt + FightWithMePaths_JAPANESE.txt + README_Japanese.txt / README_English.txt
  test  : 上の paths と同じ + テスト用メモ.txt(README なし)
release は release/README_{Japanese,English}.{fwm,paths}.txt を雛形に使い、{SHA_FWM_JA} / {SHA_PATHS_JA}(訳文ファイルの SHA-256)を埋める。
README の 1 行目に --version が含まれていなければ失敗する(Nexus の版と README の版の食い違いを防ぐ)。"""
import argparse, hashlib, os, re, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = 'SKSE/Plugins/FightWithMe/Translations/'
FILES = {'fwm': ['FightWithMe_JAPANESE.txt'], 'paths': ['FightWithMe_JAPANESE.txt', 'FightWithMePaths_JAPANESE.txt']}
NAMES = {'fwm': 'Fight With Me - Japanese Translations Patch', 'paths': 'Path of the Companions - Japanese Translations Patch'}


def sha(b): return hashlib.sha256(b).hexdigest()


def put(z, arcname, data):
    zi = zipfile.ZipInfo(arcname, (2026, 1, 1, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16
    z.writestr(zi, data)


def load(d, names):
    out = []
    for n in names:
        p = os.path.join(d, TPL, n)
        if not os.path.isfile(p): raise SystemExit('見つかりません: %s(先に tools/lang_build.py を実行)' % p)
        out.append((TPL + n, open(p, 'rb').read()))
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='mode', required=True)
    t = sub.add_parser('test'); t.add_argument('dir'); t.add_argument('n'); t.add_argument('--memo', required=True); t.add_argument('--out', default='out')
    r = sub.add_parser('release'); r.add_argument('page', choices=['fwm', 'paths']); r.add_argument('dir'); r.add_argument('--version', required=True); r.add_argument('--out', default='out')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.mode == 'test':
        memo = open(a.memo, encoding='utf-8').read().replace('\r\n', '\n')
        path = os.path.join(a.out, 'FWM_Paths_ja_test%s.zip' % a.n)
        entries = load(a.dir, FILES['paths']) + [('テスト用メモ.txt', memo.encode('utf-8'))]
        with zipfile.ZipFile(path, 'w') as z:
            for name, data in entries: put(z, name, data)
        print(path)
        for name, data in entries: print('  ', name, len(data), sha(data)[:12])
        return
    files = load(a.dir, FILES['paths'])
    shas = {'{SHA_FWM_JA}': sha(files[0][1]), '{SHA_PATHS_JA}': sha(files[1][1])}
    entries = load(a.dir, FILES[a.page])
    path = os.path.join(a.out, '%s %s.zip' % (NAMES[a.page], a.version))
    for lang in ('Japanese', 'English'):
        s = open(os.path.join(ROOT, 'release', 'README_%s.%s.txt' % (lang, a.page)), encoding='utf-8').read()
        for k, v in shas.items(): s = s.replace(k, v)
        left = re.findall(r'\{[A-Z_]+\}', s)
        if left: raise SystemExit('未解決のプレースホルダ: %s' % left)
        first = s.split('\n', 1)[0]
        if a.version not in first: raise SystemExit('README(%s)の1行目に版 %s がありません(雛形を直してください): %s' % (lang, a.version, first))
        entries.append(('README_%s.txt' % lang, s.replace('\r\n', '\n').encode('utf-8')))
    with zipfile.ZipFile(path, 'w') as z:    # すべての検査が済んでから書く(失敗時に中途半端な zip を残さない)
        for name, data in entries: put(z, name, data)
    print(path)
    for name, data in entries: print('  ', name, len(data), sha(data)[:12])


if __name__ == '__main__':
    main()
