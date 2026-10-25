# Nexus 用テキスト(0.3.0-2)

配布 zip(中身のDLLは同一、SHA-256 203d62f4…accd1d)
- Fight With Me - Japanese Translations Patch 0.3.0-2.zip → FWM 日本語化パッチのページ(194874)の Main へ(バージョンは FWM 0.3.0 に連動)
- Paths - Japanese Translations Patch 0.1.0-1.zip → Paths 日本語化パッチの新規ページへ(バージョンは Paths 0.1.0 に連動。Translation として登録し、原MODに Paths 195610 を指定)

---------------------------------------------------------------
## A. FWM 日本語化パッチ(194874): ファイル更新

ファイル名: Fight With Me - Japanese Translations Patch
バージョン: 0.3.0-2 (旧 0.3.0-1 は Old へ)

ファイルの説明(短く):
Fight With Me 0.3.0 用の日本語化パッチ。Paths(アドオン)も日本語化。ロード順は FWM → Paths → 本パッチ。

更新履歴(Changelog 追記):
0.3.0-2
- Paths を日本語化しました(ツリー画面、全88ノード、ランク、ボーナス、ガイド、設定、通知)。DLLは Paths の日本語化パッチと同一です。
- 「スキル」を「アビリティ」に統一しました。Fight With Me 本体の画面の表記も変わります(バニラのスキルとの混同を避けるため)。
- Paths 画面の文字位置、間隔、折り返しを調整しました。

説明欄に追記する文章(BBCode):
[b]0.3.0-2 から Paths にも対応しました。[/b]
ロード順は [b]Fight With Me → Paths → 本パッチ[/b](本パッチを最後)。
[b]推奨:[/b] SKSEMenuFramework.ini の [Fonts] で EnableChinese = true(SMF v3.18 以降)。ゲーム由来の魔法名などで、日本語範囲外の漢字が「?」になるのを防ぎます。Paths の日本語化パッチと中身は同じDLLなので、どちらか一方を入れてください。
「スキル」は「アビリティ」に変わりました(0.3.0-1 から)。
Paths 0.1.0 の全88ノードの英日対照表: [url=https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch/blob/main/PATHS_TABLE.md]PATHS_TABLE.md[/url]。名称や訳語へのご意見を歓迎します(一部の訳は暫定です)。

---------------------------------------------------------------
## B. Paths 日本語化パッチ: 新規ページ

ページ名: Paths - Japanese Translations Patch
カテゴリ: Translations
原MOD: Paths - Custom Follower Abilities (https://www.nexusmods.com/skyrimspecialedition/mods/195610)
バージョン: 0.1.0-1(Paths 0.1.0 用。DLL自体は Fight With Me 0.3.0 用)

要約(Short description):
Paths(Fight With Me のアドオン)の日本語化パッチ。ツリー、アビリティ、ランク、ボーナス、ガイドを日本語化します。

必須MOD(Requirements): Paths 0.1.0 / Fight With Me 0.3.0 / SKSE Menu Framework 3(日本語フォント設定)

権限(Permissions): 原MODの権限に合わせる。他サイトへのアップロード: 不可。原作者(hashhbbrown)の文字列を含むため、原MODページへのリンクとクレジットを明記。

説明文(BBCode・日本語):
[size=5][b]Paths - 日本語化パッチ[/b][/size]
[url=https://www.nexusmods.com/skyrimspecialedition/mods/195610]Paths - Custom Follower Abilities[/url](作者: hashhbbrown)の非公式日本語化パッチです。

[b]先に知っておいてほしいこと[/b]
Paths は別MODに見えますが、Paths の画面の文字列は Paths ではなく、必須MODの [url=https://www.nexusmods.com/skyrimspecialedition/mods/194766]Fight With Me[/url] の FightWithMe.dll の中にあります。
そのため本パッチは [b]Fight With Me の FightWithMe.dll を置き換える形式[/b]です(Paths のファイルは変更しません)。Fight With Me 本体の画面も日本語になります。
[url=https://www.nexusmods.com/skyrimspecialedition/mods/194874]Fight With Me の日本語化パッチ[/url]と中身は同じDLLなので、どちらか一方だけ入れてください。

[b]日本語になるもの[/b]
- Paths のツリー画面(6つのパス、全88ノードのアビリティ・特性・ランク・ボーナス)、ガイド、設定画面、通知メッセージ
- Fight With Me 本体の画面

[b]導入[/b]
1. Fight With Me 0.3.0 と Paths 0.1.0 を導入
2. SKSE Menu Framework 3 に日本語フォントを設定(日本語環境なら不要)
3. 本パッチを [b]最後(後勝ち)[/b] に導入 … ロード順: Fight With Me → Paths → 本パッチ
4. [b]推奨[/b]: SKSEMenuFramework.ini の [Fonts] で EnableChinese = true(SMF v3.18 以降)。魔法名・シャウト名などゲーム由来の文字列は本パッチでは変更できず、日本語範囲外の漢字が「?」になります。Paths では多く出ると見込まれます。

[b]注意[/b]
- 訳語は「スキル」ではなく「アビリティ」で統一しています。
- 名称には意訳を含み、一部は暫定です。対照表: [url=https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch/blob/main/PATHS_TABLE.md]PATHS_TABLE.md[/url]。ご意見をお寄せください。
- 本体を更新するときは、先に本パッチを無効化してください。
- 訳文と説明文の作成にAI(Claude)を使用しています。ゲーム内で確認していますが、誤訳や表示崩れがあればコメントでお知らせください。
- 非公式の翻訳です。原作者に不具合を問い合わせないでください。

[b]ソース[/b](DLLは含みません): https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch
[b]謝辞[/b] 原作者 hashhbbrown さんに感謝します。

説明文(英語・短縮版):
An unofficial Japanese translation of [url=https://www.nexusmods.com/skyrimspecialedition/mods/195610]Paths[/url] by hashhbbrown (tree screens, all 88 nodes, ranks, bonuses, guide, settings, notices). Note: Paths' screen text is not inside Paths but inside Fight With Me's FightWithMe.dll, so this patch replaces that DLL (and translates Fight With Me's own screens too). Install order: Fight With Me -> Paths -> this patch (last). Recommended: EnableChinese = true under [Fonts] in SKSEMenuFramework.ini (SMF v3.18+). The DLL is identical to the one in the Fight With Me Japanese patch (https://www.nexusmods.com/skyrimspecialedition/mods/194874); install only one of them. Source scripts only on GitHub: https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch . AI-assisted translation (Claude). Unofficial; do not ask the original author for support.

クレジット欄(Credits): hashhbbrown — Paths / Fight With Me(原作者)

---------------------------------------------------------------
## C. GitHub(ユーザー作業・確認後)
- ブランチ wip/paths-0.3.0-2 を main へ統合し、タグ v0.3.0-2 を作成(このセッションからのタグ push は拒否される)
- リリースノート(GitHub Release 本文は Changelog の 0.3.0-2 を流用。バイナリは添付しない)
- Paths ページ作成後、README の「Paths page (not yet created)」を URL に差し替える

## D. 公開前の確認事項
1. 原作者の Paths 説明欄/作者メモの更新(権限が変わっていないか)を投稿直前に再確認
2. Nexus の Paths ページ作成時、画像はゲーム内スクリーンショット(Paths ツリー画面)を使用可
3. 旧 0.3.0-1 を使っていた人へ: 「スキル」→「アビリティ」の表記変更あり
