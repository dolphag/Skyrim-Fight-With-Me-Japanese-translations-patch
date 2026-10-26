Fight With Me - Japanese Translations Patch 0.5.0-1 (対象: Fight With Me 0.5.0)
=====================================================================
Fight With Me 0.5.0 を日本語化するパッチです。原作がメッセージを外部のテキストファイルに分けて読み込んでいるので、その日本語版を置きます。DLL は変更しません(ファイルを置くだけです)。
0.3.0-2 以前の日本語化パッチ(DLL を差し替える版)とは別のものです。旧版を使っていた場合は、先に外してください。
原MOD:
- Fight With Me        https://www.nexusmods.com/skyrimspecialedition/mods/194766
- Path of the Companions (Paths、任意の連携先)  https://www.nexusmods.com/skyrimspecialedition/mods/196635
原作者: hashhbbrown (GitHub: fatalCMD)

■ 必須
- Fight With Me 0.5.0
- SKSE Menu Framework 3(日本語を表示する設定を含む)。SKSEMenuFramework.ini の [Fonts] で EnableJapanese = true、PrimaryFont = NotoSansJP-Medium.ttf など。
  日本語環境を導入済みなら追加の設定は不要です。作者は 2game 様の日本語化ファイルで動作を確認しています。
  https://skyrimspecialedition.2game.info/detail.php?id=120352
- 日本語フォント(別ファイル「Japanese UI Font」)。**これを入れないと、日本語が「?」になります。**
  原作の画面は、日本語の字形を持たないテーマ用フォント(Lora / Spectral / BarlowSemiCondensed)で描かれるためです。
  別ファイルのフォントは、同じ名前の日本語対応フォントです(Noto Sans JP を元にしています。SIL OFL)。
  MOD の優先順位は「原作 → 日本語化パッチ → Japanese UI Font」の順にして、フォントが原作のフォントに勝つようにしてください。

■ Path of the Companions(Paths)を併用する場合
Paths は別の MOD で、Fight With Me がなくても動きます(Fight With Me は任意の連携先です)。Paths を使う場合は、Paths 用の日本語化パッチ(Path of the Companions - Japanese Translations Patch、別ページ)も入れてください。
Paths 用パッチの訳にも、この MOD の画面の文言の大部分が含まれています。両方を入れても問題ありません(共通の文言は、この MOD 用パッチが後に読まれて優先されます)。

■ 推奨
- SKSEMenuFramework.ini の [Fonts] で EnableChinese = true を設定(SMF v3.18 以降)。
  魔法名・従者名など、ゲームや他の MOD から取得する文字列は本パッチでは変更できず、日本語グリフ範囲外の漢字が「?」になります。
- 姉妹MODの日本語化パッチ: Walk With Me - Japanese Translations Patch  https://www.nexusmods.com/skyrimspecialedition/mods/194872

■ 日本語にならないとき
言語はゲームの設定(Skyrim.ini の sLanguage)に従います。sLanguage=JAPANESE のときに読まれます。
英語版ゲームなどで、sLanguage が JAPANESE でない場合は、次のファイルに書いてください(無ければ新規作成。反映はゲームの再起動後)。
  SKSE/Plugins/FightWithMe_user.ini
      [Interface]
      sLanguage = JAPANESE
SKSE のログ(Documents/My Games/Skyrim Special Edition/SKSE)に「[Text] JAPANESE: N lines from ...」と出ていれば、日本語のファイルは読まれています。
この行が無い、または「no translation files, so English」なら、ファイルの置き場所を確認してください。

■ 導入
MOD として入れてください(MO2・Vortex など)。置かれるファイルは次のとおりです。
SKSE/Plugins/FightWithMe/Translations/FightWithMe_JAPANESE.txt    Fight With Me の画面(バトルプラン・設定・通知)
ファイルを置くだけで、DLL・INI・セーブには影響しません。無効にすれば元に戻ります。
原作を更新するときは、パッチを外す必要はありません。ただし、新しく増えた文言は英語のまま表示されます(パッチの更新をお待ちください)。
本体とパッチのバージョンは合わせてください。バージョン番号は原則として本体と同じで、パッチだけを修正したときは x.x.x-1 のように枝番をつけます。

訳文ファイルの SHA-256:
  FightWithMe_JAPANESE.txt       {SHA_JA}

■ 日本語にならないもの
- パーティ設定ページの、役割・注目対象・位置取りのドロップダウン(選択肢と、その説明のホバー表示)。原作のこの部分がメッセージのファイルを通していないため、英語のままです(原作側の修正が必要です)。
- テーマ名(Vanilla / Oxblood / Nordic)は、原文のままにしています。
- キー名・ボタン表示(Tab / Esc など)、ログ、INI のコメント。
- ゲームや他の MOD から取得する文字列(魔法名、従者名など)。
- 原作の更新で増えた文言(パッチの更新まで英語)。
「スキル」は、バニラのスキルと混同しないよう、Fight With Me のアビリティを指すときは「アビリティ」に統一しています。
新しいアビリティ名(ケイオスダウン、最後の砦 など)は意訳を含み、一部は暫定です。ご意見をお寄せください。
訳文は、SKSE Menu Framework の日本語グリフ範囲(約3000字)内の漢字だけで書いています。

■ 権利・ソース・クレジット
原作者: hashhbbrown (GitHub: fatalCMD)。原作のすべての文言・ツリー・ゲームデザインは原作者のものです。
本パッチは、Fight With Me の Nexus ページの権限表示(2026-10-26 にユーザーが確認: 改変・素材の利用は作者のクレジット表記で可。他サイトへの再アップロードは不可)に従って作った非公式の翻訳です。
本パッチに、原作のファイル(DLL・画像・フォントなど)は含まれません。含まれるのは、原作の英語の文言(メッセージのファイルの左側)と、日本語訳です。
本パッチは Nexus Mods の翻訳ページでのみ配布します。他サイトへの転載はご遠慮ください。
GitHub にはソースコード(生成スクリプトと翻訳表)のみを置き、配布用のファイルやフォントは置いていません。
原作者に本パッチの不具合を問い合わせないでください。作者から削除の依頼があれば速やかに対応します。無保証です。
原作のソース(GPL-3.0-or-later と宣言されています): https://github.com/fatalCMD/potc
パッチの生成スクリプトと翻訳表: https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch (版ごとにタグがあります)
日本語訳と生成スクリプトは GPL-3.0-or-later です。英語の列は原作者のもので、この対象ではありません。
日本語フォント(別ファイル)は、Noto Sans JP(Copyright 2014-2021 Adobe)を元に、内部の名前を付け替えたものです。SIL Open Font License 1.1。全文は同梱の FONT-LICENSE.txt にあります。

■ AIの利用
訳文と本説明文の作成にAI(Claude, Anthropic)を使用しています。
ゲーム内で確認していますが、見落としがあるかもしれません。誤訳や表示崩れがあれば、Nexus のコメントでお知らせください。

■ 謝辞
素晴らしいMODを公開してくださっている原作者 hashhbbrown さんに心から感謝します。
日本語でも楽しめるようにと、感謝を込めて作った非公式の翻訳です。

■ 更新履歴
0.5.0-1: Fight With Me 0.5.0 に対応(バトルプラン・設定・通知を日本語化)。DLL を差し替える旧版(0.3.0-2 以前)とは別の方式です。旧版は外してください。
0.3.0-2: Paths 0.1.0 を日本語化(ツリー画面、全88ノード、ランク、ボーナス、ガイド、設定、通知)。「スキル」を「アビリティ」に統一。Paths 画面の文字位置・折り返しを調整。
0.3.0-1: Fight With Me 0.3.0 に対応(オートバトル、スキル欄、役割・配置の説明の変更、ヒーラーの回復表示、Volley の通知、視認距離、テーマなどを日本語化)。Paths 関連は未対応。
0.2.0-1: Fight With Me 0.2.0 に対応(ヒーラーの仕様変更・マジカ活性・魔法選択画面・身構えなどの新表示を日本語化)。
0.2.0系は本体 0.2.0 用です。
0.1.5系(最終 0.1.5-4)は本体 0.1.5 用です。
0.1.5-4: 上空視点の操作ヒント「LS 移動」の「動」が欠けて「移?」と表示される不具合を修正。
0.1.5-3: 上空視点で自キャラの目印を「あなた」と表示し、輪と重ならないよう上へずらした。
0.1.5-2: スキル欄の「自動」と従者パネルの「レベル」の一部が「?」になる不具合、役職が選べない理由の一部が欠けて表示される不具合を修正。
0.1.5-1: 「?」と表示される漢字(怯・叩・俯・瞰)を描画できる字に置き換え。上空視点タブのツールチップの翻訳漏れを修正。
         調合の通知を「◯◯が◯本の△△を調合した（ほかに□□）。」の語順に修正。「あなた/パーティを攻撃中」を「あなた/パーティへの攻撃者」に変更。
         バトルプラン画面の文字を大きく(約1.2倍→約1.4倍)。
0.1.5  : 初版。
