# -*- coding: utf-8 -*-
# Fight With Me 0.1.5 パッチ設定 (DLLアドレスは FightWithMe.dll 0.1.5 専用)

# 翻訳しないキー（表にはあるが、このDLLでは別用途と衝突するなど）
SKIP_KEYS = set()

# (キー, 参照アドレス) を個別に除外 (ImGuiのID・tween名など表示文字列ではない用途)
SKIP_SITES = {
    ('enemy', 0xb7d4b),   # tween名 "enemy" (表示ではない)
    ('War cry', 0x8d52c), # INIのフォーム名(ログ表示用)。スキル名の方だけ訳す
}

# 画面に出ない/対象外としてあえて訳さないキー（DLL内に存在しても無視）
NOT_TRANSLATED = {
    'No arrows': 'インライン展開(movsd)の箇所のみで、安全な置換方式が無いため原文のまま',
}

# Label/LabelWidth の1バイトずつ描画する不具合を回避するスタブ
LABEL = 0xbcd80        # Label(draw,pos,color,size,string_view*,tracking)
LABELWIDTH = 0xbcb30   # LabelWidth(size,string_view*,tracking) -> float
TEXT = 0xbd360         # Text(draw,pos,color,size,string_view*)
TEXTSIZE = 0xbd4a0     # TextSize(size,string_view*) -> ImVec2 (rax)
ALLOC = 0x1c970        # operator new 相当(長文 std::string の確保)。0.1.0: 0x1be90
STRCTOR = 0x1c9e0      # std::string(const char*, size_t) コンストラクタ

# 近傍探索で見つからない長さ即値を手動指定: (キー, lea アドレス, 長さ即値(mov qword [m],imm32) のアドレス)
# 0xbfe20 の関数は、4つの Why() 文字列のポインタを先にレジスタへ載せ、長さは switch の各分岐で設定する
MANUAL_LEN = [
    ('Knows no spell that heals others.',           0xbff76, 0xbffb8),
    ('Knows no attack spell and carries no staff.', 0xbff7d, 0xbffc6),
    ('Carries no bow or crossbow.',                 0xbff8b, 0xbffd4),
    ('Carries no melee weapon.',                    0xbff84, 0xbffe2),
]

# 文字列長が imm8/disp8/imm32 のまま命令に埋め込まれている箇所(インライン展開された std::string::append)。
# 新しい長さが127以下なら命令長を変えずにバイトだけ書き換えられる。(キー, 命令アドレス, 種別)
EXTRA_LEN = [
    # 'Potions' の見出し: std::string のサイズ欄(imm32)と、終端NULの書き込み位置(disp8)に長さが埋め込まれている (訳は15バイトで SSO に収まる)
    ('Potions', 0xae3cb, 'imm32'),   # mov qword [rbp+0x118], 7
    ('Potions', 0xae3eb, 'byte'),    # mov byte [rbx+7], r13b
]

# 長文(16バイト超)のstd::stringがヒープ確保+コピーで展開されている領域: サイトアドレス -> (領域開始, 領域終了, 基準レジスタ, 変位)
HEAP_REGIONS = {
    # 'Press a key...' (SSO): 末尾2バイトのゼロ詰めが先頭にあり、自動検出の形と違うため手動指定
    0x96283: (0x9626e, 0x962a7, 'rsp', 0x40),
}
# 領域置換後に、破壊される揮発レジスタを元の値に戻す命令 (サイトの領域開始アドレス -> 機械語, 想定する元命令)
POSTFIX = {}

PARAGRAPH = 0xbcee0    # Paragraph(draw,pos,color,size,string_view*,width)

# 日本語の文字だけ拡大する倍率(題字は除く)。日本語は同じpxでも英字より小さく見えるため。
FONT_SCALE = 1.2
# 題字を描く Label/LabelWidth 呼び出し(YOUR PARTY / BATTLE PLAN)。拡大しない。
TITLE_CALLS = {0x9ff69, 0xa0120}

# DrawTip(ツールチップ)は ImGui の CalcTextSize で枠を測るため、文字だけ拡大すると枠からはみ出す。
# そこで DrawTip 内の size(15.0*s) と width(300.0*s) の係数を同じ倍率で拡大する(命令アドレス, 元の係数)。
TIP_CONSTS = [(0xa131f, 15.0), (0xa1328, 300.0)]

# rdata に文字列が無い (命令の即値から組み立てられる) 表示文字列: (原文, 領域開始, 領域終了(排他), 基準レジスタ, 変位, 訳)
IMM_REGIONS = [
    ('none',     0xae550, 0xae578, 'rbp', 0x1e0, 'なし'),   # ポーション欄のツールチップ「Potions: none」
    ('everyone', 0x7a11b, 0x7a14a, 'rbp', 0x90,  '全員'),   # 「Taunted, but everyone shrugged it off.」
]
