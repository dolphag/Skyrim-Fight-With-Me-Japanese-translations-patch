# -*- coding: utf-8 -*-
"""日本語対応フォントの zip 用ファイルを作る(FWM 0.5.0 / Paths 1.0 のテーマ UI 用)。

原作のテーマ UI(SMF 経由)は Lora-SemiBold / Spectral-SemiBold / BarlowSemiCondensed-SemiBold を使う。
同梱の TTF はラテン文字のみで、日本語は「?」になる。同じ名前の日本語対応フォントを置くと表示される(2026-10-26 実機確認)。
このスクリプトは、ユーザーが用意した OFL のフォントを、内部の名前を付け替えて 3 つの名前で書き出す(既定は全グリフ。--subset で絞る)。

  python3 -I tools/make_font_pack.py --font NotoSansJP-Medium.ttf --license OFL.txt --out out/font

--license には、そのフォントの OFL 全文のファイルを渡す(同梱必須)。--subset のときの字形は tools/jp_kanji.txt + かな + ASCII + 記号。
内部の名前(family)は、元の名前を引き継がないよう付け替える(OFL の Reserved Font Name 対策)。
"""
import argparse, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = ['Lora-SemiBold', 'Spectral-SemiBold', 'BarlowSemiCondensed-SemiBold']
FAMILY = 'FWM Japanese UI'


def chars():
    kanji = open(os.path.join(HERE, 'jp_kanji.txt'), encoding='utf-8').read().strip()
    kana = ''.join(chr(c) for c in list(range(0x3041, 0x3097)) + list(range(0x30A1, 0x30FB)) + [0x30FC, 0x30FD, 0x30FE])
    punct = '、。，．・：；？！゛゜´｀¨＾￣＿ヽヾゝゞ〃仝々〆〇ー―‐／＼～∥｜…‥‘’“”（）〔〕［］｛｝〈〉《》「」『』【】＋－±×÷＝≠＜＞≦≧∞∴♂♀°′″℃￥＄￠￡％＃＆＊＠§☆★○●◎◇◆□■△▲▽▼※〒→←↑↓〓'
    ascii_ = ''.join(chr(c) for c in range(0x20, 0x7F))
    wide = ''.join(chr(c) for c in list(range(0xFF10, 0xFF1A)) + list(range(0xFF21, 0xFF3B)) + list(range(0xFF41, 0xFF5B)))
    return sorted(set(kanji + kana + punct + ascii_ + wide + ' 　'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--font', required=True)
    ap.add_argument('--license', required=True, help='そのフォントの OFL 全文')
    ap.add_argument('--out', required=True)
    ap.add_argument('--subset', action='store_true', help='使う文字だけに絞る(小さいが、ゲーム由来の珍しい漢字が出ない。既定は全グリフを残す=実機で確認した状態)')
    a = ap.parse_args()
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
    except ImportError:
        sys.exit('fonttools が必要です: pip install fonttools')
    os.makedirs(a.out, exist_ok=True)
    opt = subset.Options(); opt.layout_features = ['*']; opt.name_IDs = ['*']; opt.notdef_outline = True; opt.glyph_names = False; opt.hinting = False
    f = TTFont(a.font, fontNumber=0, recalcTimestamp=False)  # 更新日時を現在時刻にしない(同じ入力から同じバイト列を作る)
    if a.subset:
        sub = subset.Subsetter(opt); sub.populate(text=''.join(chars())); sub.subset(f)
    for rec in list(f['name'].names):
        if rec.nameID in (1, 4, 16):   f['name'].setName(FAMILY, rec.nameID, rec.platformID, rec.platEncID, rec.langID)
        elif rec.nameID == 6:          f['name'].setName(FAMILY.replace(' ', '') + '-Regular', 6, rec.platformID, rec.platEncID, rec.langID)
        elif rec.nameID in (2, 17):    f['name'].setName('Regular', rec.nameID, rec.platformID, rec.platEncID, rec.langID)
    tmp = os.path.join(a.out, '_one.ttf'); f.save(tmp)
    data = open(tmp, 'rb').read(); os.remove(tmp)
    for n in NAMES:
        with open(os.path.join(a.out, n + '.ttf'), 'wb') as o: o.write(data)
    with open(os.path.join(a.out, 'FONT-LICENSE.txt'), 'wb') as o: o.write(open(a.license, 'rb').read())
    print(f'{len(data)/1e6:.2f} MB x {len(NAMES)} -> {a.out} (glyph chars requested: {len(chars())})')


if __name__ == '__main__':
    main()
