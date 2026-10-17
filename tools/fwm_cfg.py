# -*- coding: utf-8 -*-
# Fight With Me 0.3.0 パッチ設定 (DLLアドレスは FightWithMe.dll 0.3.0 専用)

# 翻訳しないキー（表にはあるが、このDLLでは別用途と衝突するなど）
SKIP_KEYS = set()

# (キー, 参照アドレス) を個別に除外 (ImGuiのID・tween名など表示文字列ではない用途)
SKIP_SITES = {
    ('you', 0x94a59),    # 成長経路(バッファ不足時の再確保)側。ふだんは通らず、長さ欄が英語のままなので触らない
}

# 画面に出ない/対象外としてあえて訳さないキー（DLL内に存在しても無視）
NOT_TRANSLATED = {
    'No arrows': 'インライン展開(movsd)の箇所のみで、安全な置換方式が無いため原文のまま',
}

# Label/LabelWidth の1バイトずつ描画する不具合を回避するスタブ
LABEL = 0x1236e0        # Label(draw,pos,color,size,string_view*,tracking)
LABELWIDTH = 0x123490   # LabelWidth(size,string_view*,tracking) -> float
TEXT = 0x123cc0         # Text(draw,pos,color,size,string_view*)
TEXTSIZE = 0x123e00     # TextSize(size,string_view*) -> ImVec2 (rax)
ALLOC = 0x1f070        # operator new 相当(長文 std::string の確保)。0.1.5: 0x1c970
STRCTOR = 0x1f0e0      # std::string(const char*, size_t) コンストラクタ

# 近傍探索で見つからない長さ即値を手動指定: (キー, lea アドレス, 長さ即値(mov qword [m],imm32) のアドレス)
# 0.2.0: 役職が選べない理由 (Why()) の文言が無くなったため空
MANUAL_LEN = []

# 文字列長が imm8/disp8/imm32 のまま命令に埋め込まれている箇所(インライン展開された std::string::append)。
# 新しい長さが127以下なら命令長を変えずにバイトだけ書き換えられる。(キー, 命令アドレス, 種別)
EXTRA_LEN = [
    ('you', 0x949e0, 'byte'), ('you', 0x949f3, 'imm32'), ('you', 0x94a10, 'byte'),   # 容量比較 cmp rdi,3 / size欄 / NUL位置
    ('AUTO', 0x10b3fd, 'imm32'),        # スキル欄の「自動」: ポインタを退避レジスタで持ち回り、長さだけ後で書く
    ('LEVEL', 0x106066, 'imm32'),       # 従者パネルの「レベル」: ポインタは rbx、長さはその場の mov
    ('Move', 0xe5b73, 'imm32'),         # 上空視点の操作ヒント: 構造体の長さ欄が分岐の前でまとめて書かれる
    ('RIGHT HAND', 0x1019c1, 'imm32'),  # mov r13d, 10
    ('LEFT HAND', 0x108733, 'byte'),    # add rdx, 9 (右 = +1 で計算)
    ('TEACH', 0x1034ac, 'imm32'),       # mov esi, 5
    (' (Adept from level 25)', 0x11d904, 'imm32'),   # r13d = 最小容量(長さ)
    ('left hand', 0x1540c9, 'byte'), ('left hand', 0x154306, 'byte'), ('right hand', 0x154706, 'byte'),   # add reg, 9 / add rbx, 10 (right = left + 1)
    ('Nothing else for this hand.', 0x103e87, 'imm32'),   # string_view をもう一度組み立てる側の長さ
    ('AUTO BATTLE', 0xe8f0e, 'imm32'),  # string_view を2つ並べて組み立てる2つ目
    ('they wait to be attacked', 0xe96c2, 'imm32'),   # cmove で選ぶ側の長さ (mov eax,24)
    ('Carries no melee weapon.', 0x12ce0a, 'imm32'), ('Carries no melee weapon.', 0x12ceb4, 'imm32'),
    ('Carries no bow or crossbow.', 0x12cdfc, 'imm32'),
    ('Knows no attack spell and carries no staff.', 0x12cdee, 'imm32'),
]

# 長文(16バイト超)のstd::stringがヒープ確保+コピーで展開されている領域、または自動検出に掛からない短文の領域:
# サイトアドレス -> (領域開始, 領域終了, 基準レジスタ, 変位)
HEAP_REGIONS = {
    0xd7993: (0xd797e, 0xd79b7, 'rsp', 0x40),   # 'Press a key...' (SSO): 末尾2バイトのゼロ詰めが先頭にあり、自動検出の形と違う
    0xb6696: (0xb6681, 0xb66be, 'rsp', 0x40),   # 'Rejuvenated' (NUL・size/cap が rbp 基準で書かれ、自動検出に掛からない)
    0xb6971: (0xb695c, 0xb698d, 'rsp', 0x40),   # 'Guarding you'
    0xb6b27: (0xb6b12, 0xb6b4e, 'rsp', 0x40),   # 'Out of magicka'
    0xc1bec: (0xc1bd6, 0xc1c27, 'rbp', 0x17),   # 'The fight is over.' (確保の後で文字列を読む形)
    0x150cbb: (0x150ca2, 0x150cfa, 'rsp', 0x20), # 'The fight is over.'
}
# 領域の後で rdx(=文字列オブジェクト) / r8(=0) / rcx が読まれる箇所: 領域内にあった元命令を、置換コードの後ろにそのまま書き直す
POSTFIX = {
    0xc1bd6: [(bytes.fromhex('488d5517'), 'lea rdx, [rbp + 0x17]', 0xc1bf7), (bytes.fromhex('4533c0'), 'xor r8d, r8d', 0xc1c03),
              (bytes.fromhex('488d8bb3feffff'), 'lea rcx, [rbx - 0x14d]', 0xc1c1c)],
    0x150ca2: [(bytes.fromhex('488d542420'), 'lea rdx, [rsp + 0x20]', 0x150cc7), (bytes.fromhex('4533c0'), 'xor r8d, r8d', 0x150cd5),
               (bytes.fromhex('488d8bb3feffff'), 'lea rcx, [rbx - 0x14d]', 0x150cef)],
}

PARAGRAPH = 0x123840    # Paragraph(draw,pos,color,size,string_view*,width)

# 日本語の文字だけ拡大する倍率(題字は除く)。日本語は同じpxでも英字より小さく見えるため。
FONT_SCALE = 1.4
# DrawTip(ツールチップ)の拡大倍率。ツールチップは元から大きめ(15px)なので画面本体より控えめにする。
TIP_SCALE = 1.2
# 題字を描く Label/LabelWidth 呼び出し(YOUR PARTY / BATTLE PLAN)。拡大しない。
TITLE_CALLS = {0xe32ef, 0xe3510}

# DrawTip(ツールチップ)は ImGui の CalcTextSize で枠を測るため、文字だけ拡大すると枠からはみ出す。
# そこで DrawTip 内の size(15.0*s) と width(300.0*s) の係数を同じ倍率で拡大する(命令アドレス, 元の係数)。
TIP_CONSTS = [(0xe4b64, 15.0), (0xe4b6d, 300.0)]

# 文字を拡大すると隣の部品と重なる箇所の間隔(命令アドレス, 元の係数, 新しい係数)。mulss xmm,[rip+定数] の定数を付け替える。
# 0xbb44c: 「耐性」見出しの下から属性ひし形の中心までの距離(34.0*s)。見出しが大きくなると、ひし形(半径19*s)の上端と重なるため広げる。
SPACING_CONSTS = [(0x1066ed, 34.0, 42.0)]

# 書式文字列を組み立てる断片のうち、同じ文字列が他でも使われるため、特定の参照箇所だけ訳すもの: (原文, lea アドレス, 訳)
# 0xd9eee: ポーション調合通知の末尾に付ける「.」
SITE_STR = []

# rdata に文字列が無い (命令の即値から組み立てられる) 表示文字列: (原文, 領域開始, 領域終了(排他), 基準レジスタ, 変位, 訳)
IMM_REGIONS = []

# rdata への参照が rip 相対ではなく「lea rax,[rip-自身]; lea rax,[rax+RVA]」(イメージベース経由)で作られるため、自動検出に掛からない長文 std::string:
# (原文, 領域開始, 領域終了(排他), 基準レジスタ, 変位)。領域 = mov ecx,サイズ(ALLOC引数) から 終端NULの書き込みまで。
EXTRA_HEAP = [
    # 上空視点タブのツールチップ「The whole fight from above: …」 (std::string は [rbp-0x90] = [rsp+0x70])
    ("The whole fight from above: blue rings for the party, red for enemies, white for you. Indoors the ceiling is cut away above everyone's heads. Click an enemy to send someone after them.",
     0xea3ab, 0xea458, 'rbp', -0x90),
]

# 上空視点で自キャラの頭上に出す「あなた」(原文 YOU) のラベルを、輪と重ならないよう上へずらす。
# TextOnWorld(draw, pos(packed xy), color, size, string_view*, alpha) の呼び出し箇所ごとに、y から size*係数 を引く中継スタブへ向ける。
# (呼び出しアドレス, 係数)。係数は「文字サイズ(14*s)の何倍上へ」。輪の半径が約24px(s=1)なので 3.0 (=42px)。
TEXTONWORLD = 0x123a00
WORLD_LABEL_LIFT = [(0xeaf9e, 3.0)]

# 内容(日本語か英字か)に関係なく常に文字を拡大する Text / TextSize の呼び出し: {呼び出しアドレス: 倍率}。測定(TextSize)と描画(Text)は必ず対で同じ倍率にする。
NUM_SCALE = 1.25   # 数値だけの表示(英字扱いで拡大されず小さく見える)を「もう少し大きく」する倍率
FORCE_SCALE = {
    0x10342d: FONT_SCALE, 0x10347f: FONT_SCALE,   # 魔法選択の一覧の各行(魔法名)
    0x1063c5: NUM_SCALE, 0x106405: NUM_SCALE,     # 従者パネルの3本のバー下の数値
}
# 日本語のとき拡大する Paragraph(折り返し描画)の呼び出し: 0xb8f6f = バトルプラン画面「メイジは…」の説明、0xbe270 = 手の選択ポップアップの同じ説明
PARA_SCALE_CALLS = {0x10416c, 0x10955c}   # バトルプラン画面の説明 / 手の選択ポップアップの説明

# 0.3.0 で本体から削除された(または文言が変わり別キーで訳し直した)表示文字列。表にあってもDLLに無いので無視する。
GONE_KEYS = {
    "{} heals {}: +{:.0f} health.", "Healed {}: +{:.0f} health each.",
    "Stay at your side, weapons out, and fight there: whatever comes near you, and whoever is on them.",
    "A Healer holds any heal, and other spells up to {}",
    "Potions", "magicka", "stamina", "OFF", "{} ", "  \u00b7  brewing",
    "Role strength, role guessing and standing down back to their defaults. Companions' orders are not touched.",
    "Volley! {} looses five arrows at {}.", "Volley: five arrows at {}.", "Could not cast on you.",
    "Abilities and potions", "Drink potions in a fight", "Brew potions at rest", "Mix them by hand",
    "Their health when they reach for a healing potion.", "Drink a healing potion below",
    "{} drinks {}.", "{} brewed {}{}",
}

# 長文で、冒頭だけで特定できる削除・文言変更済みの表示文字列 (前方一致)
GONE_PREFIX = (
    "With me (what To me! gives everyone): they keep this close to you and fight there,",
    "They drink their own in a fight", "Potions: {}{}", "Standing about out of a fight",
    "The spells you can give a healer's hands on their sheet: every heal",
    "What each ability looks like in the world: a red glow", "Companions drink their own potions",
    "They look over the mix in their hands",
)
