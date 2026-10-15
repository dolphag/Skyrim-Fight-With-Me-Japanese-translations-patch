# -*- coding: utf-8 -*-
# Fight With Me 0.2.0 パッチ設定 (DLLアドレスは FightWithMe.dll 0.2.0 専用)

# 翻訳しないキー（表にはあるが、このDLLでは別用途と衝突するなど）
SKIP_KEYS = set()

# (キー, 参照アドレス) を個別に除外 (ImGuiのID・tween名など表示文字列ではない用途)
SKIP_SITES = {
    ('you', 0x7dc70),     # 成長経路の自動検出の誤検出 (rax は生のヒープバッファで std::string ではない)
    ('enemy', 0xcc121),   # tween名 "enemy" (表示ではない)
    ('War cry', 0x991cb), # INIのフォーム名(ログ表示用)。スキル名の方だけ訳す
}

# 画面に出ない/対象外としてあえて訳さないキー（DLL内に存在しても無視）
NOT_TRANSLATED = {
    'No arrows': 'インライン展開(movsd)の箇所のみで、安全な置換方式が無いため原文のまま',
}

# Label/LabelWidth の1バイトずつ描画する不具合を回避するスタブ
LABEL = 0xd1c50        # Label(draw,pos,color,size,string_view*,tracking)
LABELWIDTH = 0xd1a00   # LabelWidth(size,string_view*,tracking) -> float
TEXT = 0xd2230         # Text(draw,pos,color,size,string_view*)
TEXTSIZE = 0xd2370     # TextSize(size,string_view*) -> ImVec2 (rax)
ALLOC = 0x1d540        # operator new 相当(長文 std::string の確保)。0.1.5: 0x1c970
STRCTOR = 0x1d5b0      # std::string(const char*, size_t) コンストラクタ

# 近傍探索で見つからない長さ即値を手動指定: (キー, lea アドレス, 長さ即値(mov qword [m],imm32) のアドレス)
# 0.2.0: 役職が選べない理由 (Why()) の文言が無くなったため空
MANUAL_LEN = []

# 文字列長が imm8/disp8/imm32 のまま命令に埋め込まれている箇所(インライン展開された std::string::append)。
# 新しい長さが127以下なら命令長を変えずにバイトだけ書き換えられる。(キー, 命令アドレス, 種別)
EXTRA_LEN = [
    # 'Potions' の見出し: std::string のサイズ欄(imm32)と、終端NULの書き込み位置(disp8)に長さが埋め込まれている (訳は15バイトで SSO に収まる)
    ('Potions', 0xc13ac, 'imm32'),   # mov qword [rbp+0x88], 7
    ('Potions', 0xc13cc, 'byte'),    # mov byte [rbx+7], r12b
    # ポインタを退避レジスタに持ち回り、2回目以降の使用では lea が無く長さ即値だけが残る箇所 (0.1.5-2 で発見)
    ('AUTO',  0xc048b, 'imm32'),     # スキル欄の「自動」: 1回目(TextSize)は lea 直後で自動検出、2回目(Text)は rsi を使い回す
    ('Move',  0xaf5f2, 'imm32'),     # 上空視点の操作ヒント「LS 移動」: 構造体の長さ欄が分岐の前でまとめて書かれ、lea の近くに無い (0.1.5-4)
    ('LEVEL', 0xbad8e, 'imm32'),
    ('you', 0x7dc08, 'imm32'), ('you', 0x7dc26, 'byte'),   # 成長経路: 長さ即値が lea から離れている
    ('RIGHT HAND', 0xb6872, 'imm32'),
    ('TEACH', 0xb8335, 'imm32'),
    (' (Adept from level 25)', 0xcee24, 'imm32'),            # r13d = 最小容量(長さ)
    ('left hand', 0xeb256, 'byte'), ('left hand', 0xeb571, 'byte'),   # add reg, 9 (right = +1 で計算)     # 従者パネルの「レベル」: ポインタは rbx、長さはその場の mov
]

# 長文(16バイト超)のstd::stringがヒープ確保+コピーで展開されている領域、または自動検出に掛からない短文の領域:
# サイトアドレス -> (領域開始, 領域終了, 基準レジスタ, 変位)
HEAP_REGIONS = {
    0xa2f83: (0xa2f6e, 0xa2fa7, 'rsp', 0x40),   # 'Press a key...' (SSO): 末尾2バイトのゼロ詰めが先頭にあり、自動検出の形と違う
    0x8808d: (0x88078, 0x880a8, 'rsp', 0x30),   # 'Braced' (xmm2 が領域後も生きている → 呼び出しを使わず直接書き込む)
    0x881cf: (0x881ba, 0x881f7, 'rsp', 0x30),   # 'Rejuvenated' (NUL・size/cap が rbp 基準で書かれ、自動検出に掛からない)
    0x882e3: (0x882ce, 0x882ff, 'rsp', 0x30),   # 'Guarding you'
    0x88492: (0x8847d, 0x884b9, 'rsp', 0x30),   # 'Out of magicka'
    0x91f9b: (0x91f82, 0x91fda, 'rsp', 0x30),   # 'The fight is over.' (確保の後で文字列を読む形)
    0xe944b: (0xe9432, 0xe948a, 'rsp', 0x20),   # 'The fight is over.'
}
# 領域の後で rdx(=文字列オブジェクト) / r8(=0) / rcx が読まれる箇所: 領域内にあった元命令を、置換コードの後ろにそのまま書き直す
POSTFIX = {
    0x91f82: [(bytes.fromhex('488d542430'), 'lea rdx, [rsp + 0x30]', 0x91fa7), (bytes.fromhex('4533c0'), 'xor r8d, r8d', 0x91fb5),
              (bytes.fromhex('488d8bcbfeffff'), 'lea rcx, [rbx - 0x135]', 0x91fcf)],
    0xe9432: [(bytes.fromhex('488d542420'), 'lea rdx, [rsp + 0x20]', 0xe9457), (bytes.fromhex('4533c0'), 'xor r8d, r8d', 0xe9465),
              (bytes.fromhex('488d8bcbfeffff'), 'lea rcx, [rbx - 0x135]', 0xe947f)],
}

PARAGRAPH = 0xd1db0    # Paragraph(draw,pos,color,size,string_view*,width)

# 日本語の文字だけ拡大する倍率(題字は除く)。日本語は同じpxでも英字より小さく見えるため。
FONT_SCALE = 1.4
# DrawTip(ツールチップ)の拡大倍率。ツールチップは元から大きめ(15px)なので画面本体より控えめにする。
TIP_SCALE = 1.2
# 題字を描く Label/LabelWidth 呼び出し(YOUR PARTY / BATTLE PLAN)。拡大しない。
TITLE_CALLS = {0xad87c, 0xada36}

# DrawTip(ツールチップ)は ImGui の CalcTextSize で枠を測るため、文字だけ拡大すると枠からはみ出す。
# そこで DrawTip 内の size(15.0*s) と width(300.0*s) の係数を同じ倍率で拡大する(命令アドレス, 元の係数)。
TIP_CONSTS = [(0xaed4f, 15.0), (0xaed58, 300.0)]

# 文字を拡大すると隣の部品と重なる箇所の間隔(命令アドレス, 元の係数, 新しい係数)。mulss xmm,[rip+定数] の定数を付け替える。
# 0xbb44c: 「耐性」見出しの下から属性ひし形の中心までの距離(34.0*s)。見出しが大きくなると、ひし形(半径19*s)の上端と重なるため広げる。
SPACING_CONSTS = [(0xbb44c, 34.0, 42.0)]

# 書式文字列を組み立てる断片のうち、同じ文字列が他でも使われるため、特定の参照箇所だけ訳すもの: (原文, lea アドレス, 訳)
# 0xd9eee: ポーション調合通知の末尾に付ける「.」
SITE_STR = [('.', 0xd9eee, '。')]

# rdata に文字列が無い (命令の即値から組み立てられる) 表示文字列: (原文, 領域開始, 領域終了(排他), 基準レジスタ, 変位, 訳)
IMM_REGIONS = [
    ('none',     0xc152d, 0xc1555, 'rbp', 0x150, 'なし'),   # ポーション欄のツールチップ「Potions: none」
    ('everyone', 0x80a16, 0x80a3e, 'rbp', 0x80,  '全員'),   # 「Taunted, but everyone shrugged it off.」 (rdx が領域後も生きているため直接書き込み。先頭のゼロ詰めは残す)
]

# rdata への参照が rip 相対ではなく「lea rax,[rip-自身]; lea rax,[rax+RVA]」(イメージベース経由)で作られるため、自動検出に掛からない長文 std::string:
# (原文, 領域開始, 領域終了(排他), 基準レジスタ, 変位)。領域 = mov ecx,サイズ(ALLOC引数) から 終端NULの書き込みまで。
EXTRA_HEAP = [
    # 上空視点タブのツールチップ「The whole fight from above: …」 (std::string は [rbp-0x80])
    ("The whole fight from above: blue rings for the party, red for enemies, white for you. Indoors the ceiling is cut away above everyone's heads. Click an enemy to send someone after them.",
     0xb30a6, 0xb3152, 'rbp', -0x80),
]

# 上空視点で自キャラの頭上に出す「あなた」(原文 YOU) のラベルを、輪と重ならないよう上へずらす。
# TextOnWorld(draw, pos(packed xy), color, size, string_view*, alpha) の呼び出し箇所ごとに、y から size*係数 を引く中継スタブへ向ける。
# (呼び出しアドレス, 係数)。係数は「文字サイズ(14*s)の何倍上へ」。輪の半径が約24px(s=1)なので 3.0 (=42px)。
TEXTONWORLD = 0xd1f70
WORLD_LABEL_LIFT = [(0xb3c74, 3.0)]

# 内容(日本語か英字か)に関係なく常に文字を拡大する Text / TextSize の呼び出し: {呼び出しアドレス: 倍率}。測定(TextSize)と描画(Text)は必ず対で同じ倍率にする。
NUM_SCALE = 1.25   # 数値だけの表示(英字扱いで拡大されず小さく見える)を「もう少し大きく」する倍率
FORCE_SCALE = {
    0xb813f: FONT_SCALE, 0xb818f: FONT_SCALE,   # 魔法選択の一覧の各行(魔法名): 日本語名は拡大されるのに英語名だけ小さくなるのを揃える
    0xbb118: NUM_SCALE, 0xbb158: NUM_SCALE,     # 従者パネル右上の3本のバーの下の数値 ({:.0f} / {:.0f})
}
# 日本語のとき拡大する Paragraph(折り返し描画)の呼び出し: 0xb8f6f = バトルプラン画面「メイジは…」の説明、0xbe270 = 手の選択ポップアップの同じ説明
PARA_SCALE_CALLS = {0xb8f6f, 0xbe270}
