# Nexus 用テキスト(FWM 0.5.0-1 / Paths 1.0.0-1)

アップロードはユーザーが行う。**権限(Permissions and credits)と版は、アップロード直前に原ページで再確認する。**
配布物は 4 つ(`out/` に `tools/make_zip.py` で作る)。FWM のページに 2 つ、Paths の翻訳ページ(新規作成)に 2 つ。

| ページ | ファイル | 版 | 種別 |
|---|---|---|---|
| FWM 日本語化(既存、Nexus 194874) | `Fight With Me - Japanese Translations Patch 0.5.0-1.zip` | 0.5.0-1 | Main |
| 同上 | `Fight With Me - Japanese UI Font 0.5.0-1.zip` | 0.5.0-1 | Optional(日本語の表示に必須。説明に明記) |
| Paths 日本語化(**新規**。原 MOD は 196635) | `Path of the Companions - Japanese Translations Patch 1.0.0-1.zip` | 1.0.0-1 | Main |
| 同上 | `Path of the Companions - Japanese UI Font 1.0.0-1.zip` | 1.0.0-1 | Optional(同上) |

旧 Paths 用ページ(196104、Paths 0.1.0 用)は、説明の先頭に「Paths 1.0 用の新ページ(リンク)へ移行。旧版用」と追記する(ユーザー判断)。

## File credits 欄(各ファイル。空にしない)
- hashhbbrown(Fight With Me / Path of the Companions の作者)。GitHub: fatalCMD
- フォントのファイルには、Noto Sans JP(Adobe)も入れる。

## ファイル説明(Main、短く)
FWM: `Fight With Me 0.5.0 の日本語訳です。翻訳ファイル(FightWithMe_JAPANESE.txt)を置くだけで、DLLは変更しません。日本語表示には、別ファイル「Japanese UI Font」とSKSE Menu Framework の日本語設定が必要です。詳細は同梱のREADME。`
Paths: `Path of the Companions 1.0.0 の日本語訳です。(以下同じ。Fight With Me は任意の連携先で、併用する場合も、この zip だけで FWM の画面まで日本語になります。FWM 用のパッチを別に入れる必要はありません)`

## ファイル説明(Japanese UI Font)
`日本語化パッチ用の日本語フォントです。入れないと日本語が「?」になります。原作と同名のフォントを置き換えるので、MODの優先順位は 原作 → 日本語化パッチ → このファイル にしてください。Noto Sans JP(SIL OFL)を元にしています。`

## 更新履歴(アップロード時の「Changelog」欄)
FWM 0.5.0-1: Fight With Me 0.5.0 に対応。DLL を差し替える方式をやめ、原作の翻訳ファイルに日本語訳を置く方式に変更。旧版(0.3.0-2 以前)は外してください。
Paths 1.0.0-1: 初版(1.0 用)。Paths が独立した MOD になったため、新ページで公開。

## ページの説明(注意書きの要点。bbcode に整形して使う)
1. 原作へのリンクとクレジット(hashhbbrown / fatalCMD)。非公式の翻訳で、原作者に問い合わせないこと。
2. **導入に必要なもの**: 本体、SKSE Menu Framework 3 の日本語設定、**Japanese UI Font(別ファイル)**。
3. **日本語にならないとき**: `sLanguage = JAPANESE`(英語版ゲームの場合: FWM は `FightWithMe_user.ini`、Paths は `FightWithMePaths_user.ini`。併用なら両方。DLL ごとに別々に読む)。ログの `[Text] JAPANESE: N lines`。
4. **日本語にならないもの**: パーティ設定ページの役割・注目対象・位置取りのドロップダウン(原作側が翻訳を通していないため)、テーマ名(原文のまま)、ゲーム由来の文字列。
5. スクリーンショット(バトルプラン、設定、Paths のツリー)。AI 利用の開示。他サイトへの転載はご遠慮ください。
6. Paths のページでは、Fight With Me は「任意の連携先」と書く(必須扱いにしない)。Paths の zip に FWM 側の訳も入っているので、FWM 用パッチは別に不要。FWM のページでは、Paths を使う人は Paths 用パッチを入れるよう案内する。
7. 対応版: FWM 0.5.0 / Paths 1.0.0。原作の更新時はパッチを外さなくてよいが、新しい文言は英語のまま。
