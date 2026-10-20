# -*- coding: utf-8 -*-
"""Paths の英日対照表(PATHS_TABLE.md)を作る。
使い方: python3 -I tools/paths_table.py <Fight With Me の include/FWM/Paths.h> > PATHS_TABLE.md
Paths.h からノードの構造(種別・段・最大ランク)を読み、日本語名は fwm_names6.py、効果は paths_effects_ja.py から引く。"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fwm_names6 import NAMES
from fwm_trans6 import T6
from paths_effects_ja import EFFECTS

src = open(sys.argv[1], encoding='utf-8').read()
body = src[src.index('inline constexpr std::array<Path, kRoles> paths{'):]
body = body[:body.index('[[nodiscard]] constexpr const Path& PathOf')]
ROLES = [('Fighter', 'ファイター', 'Path of the Blade'), ('Tank', 'タンク', 'Path of the Shield'), ('Healer', 'ヒーラー', 'Path of the Mender'),
         ('Bruiser', 'ブルーザー', 'Path of the Hammer'), ('Archer', 'アーチャー', 'Path of the Arrow'), ('Mage', 'メイジ', 'Path of the Storm')]
LEAD = {'Path of the Blade': 'Steel and nerve: take their weapons, turn their blows, cut through crowds.',
        'Path of the Shield': 'Hold the line: draw every eye, stand between you and harm, steel the party.',
        'Path of the Mender': 'Keep everyone standing: heals, quickened magicka, wards and slow renewal.',
        'Path of the Hammer': 'Break them: roars that stagger, fury, shattered guards and a shaking earth.',
        'Path of the Arrow': 'Death from range: volleys, a steady eye, pinning shots and a rain of arrows.',
        'Path of the Storm': 'Spell pressure: surging magicka, wards, elemental bursts, and at its height, Magnus.'}
parts = re.split(r'// (?:Fighter|Tank|Healer|Bruiser|Archer|Mage): the \w+', body)[1:]
assert len(parts) == 6, len(parts)
call = re.compile(r'detail::([ABTCE])\(([^)]*)\)')
def args(s): return [a.strip().strip('"') for a in re.split(r',\s*(?=(?:[^"]*"[^"]*")*[^"]*$)', s)]
UNLOCK = {0: '最初から', 1: '5ポイント使用で', 2: '10ポイント使用で'}
out = []
w = out.append
w('# Paths 日本語化 対照表 / Paths Japanese name table\n')
w('Paths (Follower Ability Skilltree) 0.1.0 のツリー6本・全88ノード(防護とスペルワードがヒーラーとメイジで共通のため、名前は86種)の、英語名・日本語名・効果の対照表です。')
w('日本語名は日本語化パッチ(FWM 0.3.0-2 以降)の表示と同じです。効果は要約で、数値は「ランクI / II / III」の値です(距離はゲーム内単位)。\n')
w('**ご意見・ご要望をお待ちしています**(名前の言い換え案、効果の説明の不足・誤りなど)。GitHub の Issues、または Nexus Mods のコメントでお知らせください。\n')
w('## 用語\n')
w('| English | 日本語 | 備考 |\n|---|---|---|')
for e, j, n in [('Path (the tree of a role)', 'ツリー', '役割ごとに1本。「スキルツリー」とは呼ばない(バニラのスキル/パークと紛らわしいため)'),
                ('Ability', 'アビリティ', '戦闘に2つ持ち込む能動スキル。バニラの「スキル」(片手武器など)と区別するため'),
                ('Branch', '分岐', 'アビリティを強化する。元のアビリティのランクを超えられない'),
                ('Trait', '特性', '常時有効'),
                ('Perk / perk points', 'パーク / パークポイント', 'バニラのパークの仕組みに合わせたため、同じ語'),
                ('Capstone', '最上位', '最終段階。他のすべてのノードを習熟すると解放'),
                ('Rank / Mastered', 'ランク / 習熟', ''),
                ('Role', '役割', 'ファイター / タンク / ヒーラー / ブルーザー / アーチャー / メイジ')]:
    w('| %s | %s | %s |' % (e, j, n))
w('\n## 解放のしくみ\n')
w('- 第1段階(最初から開いている): 各ツリーの先頭2つのアビリティ(全従者が最初からランクI)と、その分岐、特性1つ。')
w('- 第2段階: そのツリーに **5ポイント** 使うと開く。第3段階(最終段階): **10ポイント** 使うと開く。')
w('- ランクは1段階につき1ポイント(最大ランクが1の分岐は1ポイント)。最上位(マグナス)だけは、他のすべてのノードを全ランク習熟してから、最初のランクが5ポイント、以降は各3ポイント。\n')
w('## 命名メモ\n')
w('- **やり込め**(Unnerve)、**解きほぐし**(Unravel)、**結集する雄叫び**(Rallying Roar)など、日本語で定着した訳語がある語は、それに合わせています。「咆」「哮」はゲームのフォントに無いため、「雄叫び」にしています。')
w('- **炎の外套**(Flame Mantle)は分岐名、**フレイム・クローク**は同名のゲーム内効果名です。')
w('- ウォークライ(War cry)、挑発(Taunt)、回復(Heal)など、Fight With Me 本体と共通のアビリティ名は、本体側の訳に統一しています。')
w('- 役割名(ファイター/タンク/ヒーラー/ブルーザー/アーチャー/メイジ)は Fight With Me 本体の表記です。ツリー名は「〜の道」で、「槌の道」(Path of the Hammer)は暫定です。\n')
total = 0
for (role_en, role_ja, title_en), part in zip(ROLES, parts):
    title_ja = T6[title_en].replace(' ', '')
    lead_ja = T6[LEAD[title_en]].replace(' ', '')
    w('## %s (%s) / %s(%s)\n' % (title_ja, title_en, role_ja, role_en))
    w(lead_ja + '\n')
    w('| 種別 | English | 日本語 | 解放 | 効果 | 再使用 |\n|---|---|---|---|---|---|')
    for kind, a in call.findall(part):
        if kind == 'E': continue
        a = args(a)
        if kind == 'A': tier = int(a[2]); name = a[3]; most = 3; label = 'アビリティ(初期)' if tier == 0 else 'アビリティ'; unlock = '最初から' if tier == 0 else UNLOCK[tier]
        elif kind == 'B': tier = int(a[2]); most = int(a[3]); name = a[4]; label = '分岐' + ('(ランク1のみ)' if most == 1 else ''); unlock = UNLOCK[tier]
        elif kind == 'T': tier = int(a[1]); name = a[2]; label = '特性'; unlock = UNLOCK[tier]
        elif kind == 'C': name = a[4]; label = 'アビリティ(最上位)'; unlock = '他の全ノードを習熟(コスト 5/3/3)'
        ja = NAMES[name]; eff, cd = EFFECTS[name]
        w('| %s | %s | **%s** | %s | %s | %s |' % (label, name, ja, unlock, eff, cd or '―'))
        total += 1
    w('')
assert total == 88, total
w('---\n')
w('英語名は Fight With Me / Paths の表示文字列です(各作者に帰属)。日本語名・効果の要約は日本語化パッチの作者による訳で、GPL-3.0-or-later です。')
print('\n'.join(out))
