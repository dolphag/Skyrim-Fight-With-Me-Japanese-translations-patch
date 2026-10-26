# FWM 0.5.0 / Path of the Companions 1.0 の調査結果(2026-10-26)

> **リポジトリの分離(2026-10-26 決定)**: Paths 用パッチは `dolphag/Skyrim-POTC-JP-Patch` に移した(そこにこの文書のコピーがある)。このリポジトリは FWM 用(`FightWithMe_JAPANESE.txt`、822 項目)のみ。Paths の zip に `FightWithMe_ENGLISH.txt` が付いているのは**原作の意図**(原作の `BuildPathsPackage.ps1` がコピーする。README にも記載。Paths の DLL に 833 件中 824 件の文字列が実在)で、同梱ミスではない。Paths 側のパッチはその一覧を含めた和集合を `FightWithMePaths_JAPANESE.txt` 1 本にする。

会話には残らないので、ここに書く。確認していないことは「未確認」と明記する。

## 結論: 方式が変わった(DLL パッチ → 翻訳テキスト)
- 0.5.0 / 1.0 は、原作が**翻訳ファイルの仕組み**を持つ。`SKSE/Plugins/FightWithMe/Translations/<Mod>_<LANGUAGE>.txt`(1 行 = 英語 TAB 訳)。
  DLL の書き換えは不要。0.3.0 までの PE パッチ(`legacy/0.3.0/fwm_patch.py` など)は 0.5.0 には使えない(アドレスも文字列の持ち方も別物)。
- ローダ仕様(原作ソース `src/Text.cpp` で確認): フォルダ内の `*_<LANGUAGE>.txt` を**全部**読み、ファイル名の昇順で後勝ち。UTF-8(BOM 可)か UTF-16。
  `#` 始まりは注釈。`\n` `\t` `\\` は戻す。右側が空なら英語のまま。鍵は英語の全文(一致しなければ英語が出る)。書式は `std::format`(`{}` `{:.0f}` `{0}`)。
  書式が合わない訳は英語に戻る(落ちない)。
- 言語: INI の `[Interface] sLanguage`(空ならゲームの `sLanguage`)。**各 DLL が自分の INI と `_user.ini` を読む**(FWM: `FightWithMe(_user).ini`、Paths: `FightWithMePaths(_user).ini`)。
  英語版ゲームの利用者は、両方の `_user.ini` に `sLanguage = JAPANESE` が要る。
- 文字は UTF-8 を 1 文字ずつ描く実装に変わっている(旧 Label の 1 バイト描画問題は無い)。表示倍率・位置補正の per-site 調整は不要になった。
  折り返し(`Paragraph`/`TextWrapped`)は ASCII スペースのみ → 長文の文節区切りにスペースを入れる(`tools/lang_build.py`、janome)。

## FWM と Paths の関係(0.5.0 / 1.0)
- Paths は **別 DLL(`FightWithMePaths.dll`)の別 MOD** になった。0.3.0 の「Paths の文字列は FWM の DLL の中」は終わり。Nexus では新しい MOD(添付ファイル名の MOD ID は **196635**、旧 Paths は 195610)。
- FWM 0.5.0 = 戦闘指示(バトルプラン、Numpad 7)のみ。アビリティ・特性・レベルは Paths 側。Paths は FWM 無しでも動く。両方あると、Paths が役割の制限を与え、FWM がアビリティの要求(標的など)を実行する。
- 両方の DLL は同じソースからビルドされ(`FWM_HOST_PATHS`)、**同じ翻訳フォルダ**を読む。FWM 無しだと Paths 自身が画面(パネル・ツリー)を描く。
- Paths 用の追加ダウンロード **POTC Effects**(1.0.21 以上必須。メッシュ・テクスチャ・クラス背景 PNG 18 枚。プラグインなし)。ソースの生成指示では背景に文字は入らない(「no text, no class label」)。翻訳対象は無いと見ているが、中身の実物は未確認。
- 翻訳ファイル: FWM zip は `FightWithMe_ENGLISH.txt`(822 項目)。Paths zip は `FightWithMe_ENGLISH.txt`(833 項目、FWM 側より新しい・多い)と `FightWithMePaths_ENGLISH.txt`(291 項目)。
  鍵の和集合は 1100(FWM 側 834 / Paths 側 291、重複 25)。

## 版・出典(確認したもの)
- FWM 0.5.0 の `FightWithMe.dll` SHA-256 `58257335f8802e5ed7e6ac4d576f9e3fea66e44d235e28dfc1e623ca37fdbf09`(原作ソースの SOURCE-MANIFEST と一致)。
- Paths 1.0.0 の `FightWithMePaths.dll` SHA-256 `dd915a09e1a5b8b5a32474ffc8c44f5fef2dfeba8b2ccb5b96f64e550d77debf`。**原作 git(`fatalCMD/potc`、commit 17d5032)の SOURCE-MANIFEST の値(`e78e3ac3…`)と一致しない**。
  Paths の配布 zip の方が新しい(Arrow Rain の文面、Party balance、Compact summons が配布版にだけある)。**鍵の集合は git ではなく配布 zip を正とする**。
- 配布 zip: `Fight With Me - 0.5.0`(Nexus 194766、2026-10-24T20:04Z)、`Path Of The Companions - Main File`(196635、版 "1"、2026-10-25T04:42Z)。
- ほぼ全ての鍵が DLL の中に文字列として実在する(FWM 側 822 のうち 13 が FWM の DLL に無いが、Paths の DLL にはある。Paths の 291 は全部ある)。
  テンプレートに無い画面文言(ハードコード)は簡易スキャンでは見当たらなかったが、網羅の保証は無い。

## 原ページの権限(ユーザーが貼付、2026-10-26。私は読み取っていない)
- Fight With Me: 他サイトへのアップロード**不可**(どんな場合も)、改変は作者クレジットで可、他ゲームへの変換は不可、素材の利用はクレジットで可(販売物・寄付ポイントも可)。
- Path of the Companions(新): アップロード可(クレジット)、改変可(クレジット)、変換可、素材の利用可(同上)。
- 翻訳はどちらも「改変・素材の利用」に収まると判断し、配布は各原 MOD の翻訳ページ(Nexus)のみ。原作のファイルは入れない。権限は版ごとに再確認する。

## 権利(要確認)
- 原作 git に `COPYING`(GPL-3.0)があり、「プラグインのコードは GPL-3.0-or-later と宣言」とある(BUILD-SOURCE.md)。0.3.0 の頃は「ライセンスファイル無し」だった。
- **Nexus ページの権限(Permissions and credits)は未確認**(WebFetch は 403、検索でもページを確認できなかった)。リリース前にユーザーがブラウザで確認すること。新しい Paths ページは旧ページと権限が違う可能性がある。

## 原作側の不具合(連絡は許可を得てから)
- 文字化けした鍵がある(`Â·` `ÃƒÆ’…` など、「·」の二重エンコード)。英語でも文字化けして表示されるはず。訳は「・」にしてある(鍵は原文の文字化けのまま一致させる)。
- `FightWithMe_ENGLISH.txt` の鍵 `RIGHT HAND`/`LEFT HAND` などが、DLL 内に無い(使われていない可能性)。未調査。

## 訳の作り方(0.5.0)
- 旧訳(`translations_en_ja.csv`、745 組)を鍵(英語全文)で流用: 1100 件中 438 件。残り 662 件を新規に訳した。
- POTC Effects(ユーザーが分割で添付、003 欠け。zip 末尾の一覧は読めた): 360 エントリ = NIF 316 / DDS 22 / PNG 18(`interface/FightWithMe/backdrops`)/ readme・credits・manifest。テキスト資産は無く、翻訳対象なし。PNG に文字が無いかの目視は未実施。
- 新アビリティ名(ケイオスダウン、最後の砦、風渡り、爆裂矢、カイナレスの顎 など)は暫定。「カイナレス」の表記は未確認。
- 旧 DLL ツールは `legacy/0.3.0/` に退避済み。手順は skill `lang-text-workflow`。

## テスト経過
- test1/test2(2026-10-26): ユーザー環境で全部英語。ログは `Fight With Me 0.3.0.0 loading.`、`[Text]` 行なし、旧 Paths(内蔵)が接続 → **0.5.0 が読み込まれていなかった**(訳の問題ではない)。Skyrim.ini は `sLanguage=JAPANESE`(音声は英語 `Voices_en0.bsa`)。
  最初に言語名の不一致を疑ったのは、DLL の版を確認する前の推測で、誤りだった。
- test2 + 旧 Paths を外して FWM 0.5.0: ログに `[Text] JAPANESE: 1125 lines`(読み込み成功)。ただし本文が「?」。
  原因: 作者の画面は SMF 経由でテーマ別フォント `Lora-SemiBold`(Oxblood)/`Spectral-SemiBold`/`BarlowSemiCondensed-SemiBold`(Nordic)を使う(`MenuFontName()`、`src/Menu.cpp`)。同梱 TTF はラテン文字のみ。
  確認: ユーザーが SMF の `NotoSansJP-Medium.ttf` を上の 3 名前でコピー → FWM の画面も Paths(刃の道のツリー、詳細、ガイド下のキーヒント)も日本語で表示された。**SMF は日本語の字形範囲を、これらのフォントにも当てている**(字形がフォントに有れば出る)。
  ソース上、`*-Medium.ttf` は使われていない(名前を返すのは SemiBold のみ)。
- パーティ画面のドロップダウン(役割・注目対象・位置取り)は英語のまま(原作側で翻訳機構を通していない可能性。ソースは未確認)。
- ドロップダウン: `RoleName`/`FocusName`/`PositionName`(`src/Menu.cpp` 7902-7904、`RosterCombo` のコールバック)が `Tr` を通さず英語名を返す → 翻訳ファイルでは直せない。原作側の修正待ち(報告文案: `docs/upstream-report-draft.md`、未送信)。DLL を直す案は 0.5.0 専用になり版ごとに作り直しなので採らない。
- フォント配布: 案 A(日本語フォントを入れた任意の別ファイル)に決定(2026-10-26、ユーザー判断。原作は版ごとに実装が変わりそうなので手順書き案は採らない)。ツール `tools/make_font_pack.py`(ユーザーが用意した OFL フォントを漢字表の範囲にサブセット化して 3 つの名前で出力)。フォント本体は PyPI に無く、ユーザー環境の `NotoSansJP-Medium.ttf` を待つ。フォントは GitHub にコミットしない。
- test3(2026-10-26): 日本語フォントを別ファイル化(Noto Sans JP、OFL。内部名 `FWM Japanese UI`、全グリフ)。ユーザーの実機で FWM / Paths とも正常。テーマ名は原文(Vanilla/Oxblood/Nordic)に統一(ドロップダウンとツールチップの不統一をユーザーが指摘)。
- パーティ画面のホバー表示(役割・注目対象・位置取りの説明)も未翻訳。`Help(roles[..].summary.data())` が `Tr` を通していないため(原作側)。
