Paths - Japanese Translations Patch 0.1.0-1 (対象: Paths 0.1.0 / Fight With Me 0.3.0)
=====================================================================
Paths(Fight With Me のアドオン)を日本語化するパッチです。
Paths は別MODに見えますが、Paths の画面の文字列は Paths ではなく Fight With Me の FightWithMe.dll の中にあります。
そのため本パッチは、Fight With Me 本体の FightWithMe.dll を置き換える形式です(Paths のファイルは変更しません)。
この置き換えにより、Fight With Me 本体の画面も日本語になります。
Fight With Me の日本語化パッチ 0.3.0-2 と中身は同じDLLです。どちらか一方を入れれば足ります。
原MOD:
- Paths         https://www.nexusmods.com/skyrimspecialedition/mods/195610
- Fight With Me https://www.nexusmods.com/skyrimspecialedition/mods/194766
原作者: hashhbbrown (GitHub: fatalCMD)

■ 必須
- Paths 0.1.0 と、その必須MODの Fight With Me 本体 0.3.0
- SKSE Menu Framework 3 で日本語を表示するための日本語フォント設定。
  日本語環境を導入済みなら追加の設定は不要です。作者は 2game 様の日本語化ファイルで動作を確認しています。
  https://skyrimspecialedition.2game.info/detail.php?id=120352
  (自分で設定する場合は SKSEMenuFramework.ini の [Fonts] で PrimaryFont = NotoSansJP-Medium.ttf / EnableJapanese = true)
- 本MODはフォントを同梱しません。Fight With Me は SMF3 のフォントで描画するためです。

■ 推奨
- SKSEMenuFramework.ini の [Fonts] で EnableChinese = true を設定(SMF v3.18 以降)。
  魔法名・シャウト名など、ゲームから取得する文字列は本パッチでは変更できず、日本語グリフ範囲外の漢字が「?」になります。
  Paths ではこうした表示が多く出ると見込まれるため、設定しておくことを推奨します(詳細は下の「魔法名などが「?」になるとき」)。
- 姉妹MODの日本語化パッチ: Walk With Me - Japanese Translations Patch
  https://www.nexusmods.com/skyrimspecialedition/mods/194872

■ ロード順
Fight With Me → Paths → 本パッチ の順で、本パッチを最後(後勝ち)にしてください。
Paths を入れていても、パッチ済みの FightWithMe.dll が使われる順にします。

■ バージョンについて
本パッチのバージョンは、原MOD(Paths)のバージョンにあわせています(Paths 0.1.0 用 → 0.1.0-1)。
ただし、DLLは Fight With Me 0.3.0 用です。Fight With Me のバージョンも必ずあわせてください。
同じバージョン内でパッチだけを修正したときは、x.x.x-1 のように枝番をつけます。
本ファイルは Fight With Me 0.3.0 専用です(アドレス固定のパッチ)。Paths や Fight With Me の他のバージョンには使わないでください。

■ 導入
本体(と Paths)を入れたうえで、本パッチを後勝ちにして有効化します。INIとセーブには影響せず、無効化すれば元に戻ります。
本体を更新するときは、先に本パッチを無効化(削除)してください。古いDLLが新しい本体を上書きして、不具合やクラッシュの原因になります。

元DLL SHA-256 : {ORIG_SHA}
パッチ後DLL   : {OUT_SHA}

■ 魔法名などが「?」になるとき
魔法名など、ゲーム本体から取得した文字列は、本パッチでは変更できません。そこに SKSE Menu Framework の日本語グリフ範囲外の漢字(例: 罠・痺)があると「?」になります。
その場合は SKSEMenuFramework.ini の [Fonts] で EnableChinese = true を設定してみてください(SMF v3.18 以降で追加された項目)。
作者の環境では、日本語範囲では「?」になる漢字(靭・怯)が、中国語の設定では表示されることを確認しています。罠・痺は未確認です。

■ 日本語になるもの / ならないもの
設定ページ、バトルプラン画面、Paths のツリー画面(各パスのアビリティ・特性・ランク・ボーナス・ガイド)、戦闘中の通知メッセージが日本語になります。
Paths の全ノード(88)の英日対照表は、GitHub の PATHS_TABLE.md にあります。
キー名・ボタン表示・ログ・INIのコメントと、一部の短い表示は英語のままです(文字列がその場で展開されていて安全に差し替えられないため)。
「スキル」は、バニラのスキルと混同しないよう「アビリティ」に統一しました(0.3.0-1 から変更。Fight With Me 本体の画面の表記も変わります)。
Paths の画面の名称は「PATHS - 従者専用ツリー」で、従者ごとのツリーという意味です。
アビリティ名は公式日本語訳に合わせています。シャウト「Slow Time」は「時間減速」、回復魔法「Healing Hands」は「治癒の手」です。
Paths の各ツリー・アビリティの名称には意訳を含み、一部は暫定です。ご意見をお寄せください。
SKSE Menu Framework は日本語グリフを約3000字に限定しています。範囲外の漢字は「?」になるため、訳文は範囲内の漢字だけを使っています。

■ 原版からの変更点
1. FightWithMe.dll の文字列を日本語に差し替えています。
2. 文字を1バイトずつ描く関数(Label / LabelWidth)の呼び出しを、日本語を含むときだけ通常の描画関数(Text / TextSize)へ振り分けています。
   英字だけの文字列は原版と同じ処理です。
3. 日本語を約1.4倍に拡大しています(日本語は英字より小さく見えるため)。題字は拡大しません。
   ツールチップは文字サイズと折り返し幅を約1.2倍に拡大して枠に収めています。
   Paths の画面では、アイコンや帯と文字が揃うよう、場所ごとに表示位置・間隔を調整しています。
4. Paths の長い説明は、日本語が途中で切れないよう、文節の区切りに折り返し用のスペースを入れています。
5. 日本語の文字列と処理は、DLL末尾に追加したセクション(.jpn)にあります。

■ 権利・ソース
原MODの配布物にはライセンスファイルがありません。各原MODページの権限表示(Fight With Me: 2026-10-11時点、Paths: 2026-10-20時点で確認:
改変・素材の利用は作者のクレジット表記で可、他サイトへの再アップロードは不可)に従い、
本パッチは Nexus Mods の、各原MODの翻訳ページでのみ配布します。他サイトへの転載はご遠慮ください。
GitHub にはソースコード(パッチ生成スクリプトと翻訳表)のみを置き、DLLは置いていません。
本パッチは、権限表示の範囲で作った非公式の翻訳です。原作者に本パッチの不具合を問い合わせないでください。作者から削除の依頼があれば速やかに対応します。
同梱の THIRD-PARTY-NOTICES_FightWithMe.md は、本体のものをそのまま収録しています(Paths のものと同一内容です)。
本体のソース: https://github.com/fatalCMD/fight-with-me (確認時点: コミット 6a5f5ce。0.3.0 の配布DLLと一致するコミット)
Paths のソース: https://github.com/fatalCMD/paths-fwm-addon
パッチ生成のスクリプトと翻訳表(DLLは含みません): https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch (版ごとにタグがあります)
無保証です。

■ AIの利用
訳文と本説明文の作成にAI(Claude, Anthropic)を使用しています。
ゲーム内で確認していますが、見落としがあるかもしれません。誤訳や表示崩れがあればNexusのコメントでお知らせください。

■ 謝辞
素晴らしいMODを公開してくださっている原作者 hashhbbrown さんに心から感謝します。
日本語でも楽しめるようにと、感謝を込めて作った非公式の翻訳です。

■ 更新履歴
0.1.0-1: 初版。Paths 0.1.0 を日本語化(ツリー画面、全88ノード、ランク、ボーナス、ガイド、設定、通知)。DLLは Fight With Me 日本語化パッチ 0.3.0-2 と同じです。
(Fight With Me 側の履歴は、Fight With Me 日本語化パッチのページを参照してください。)
