# Nexus 用テキスト(Fight With Me 日本語化 0.5.0-1)

アップロードはユーザーが行う。**権限(Permissions and credits)と版は、アップロード直前に原ページで再確認する。**
既存の FWM 日本語化ページ(Nexus 194874)に、1 つのファイルを置く(翻訳と日本語フォントを同じ zip にまとめる。2 ファイルに分けると、MO2 で「一つにまとめる/置き換える」のダイアログが出て混乱するため)。Paths 用は別リポジトリ・別ページ(`dolphag/Skyrim-POTC-JP-Patch`)。

| ファイル | 版 | 種別 |
|---|---|---|
| `Fight With Me - Japanese Translations Patch 0.5.0-1.zip` | 0.5.0-1 | Main |

## File credits 欄(各ファイル。空にしない)
- hashhbbrown(Fight With Me の作者)。GitHub: fatalCMD
- Noto Sans JP(Adobe)も入れる(フォントを同梱しているため)。

## ファイル説明(Main、短く)
`Fight With Me 0.5.0 の日本語訳です。原作が外部のテキストファイルに分けているメッセージの日本語版(FightWithMe_JAPANESE.txt)を置くだけで、DLLは変更しません。日本語フォントを同梱しています(原作のテーマ用フォントを置き換えます)。日本語表示にはSKSE Menu Framework の日本語設定も必要です。詳細は同梱のREADME。`

## 更新履歴(アップロード時の「Changelog」欄)
0.5.0-1: Fight With Me 0.5.0 に対応。DLL を差し替える旧版(0.3.0-2 以前)とは別の方式です。旧版は外してください。

## ページの説明(要点。bbcode に整形して使う)
1. 原作へのリンクとクレジット(hashhbbrown / fatalCMD)。非公式の翻訳で、原作者に問い合わせないこと。
2. **導入に必要なもの**: Fight With Me 0.5.0、SKSE Menu Framework 3 の日本語設定、SKSE Menu Framework の日本語設定。旧版(0.3.0-2 以前の DLL 版)は外す。
3. **日本語にならないとき**: `sLanguage = JAPANESE`(英語版ゲームの場合は `FightWithMe_user.ini`)。ログの `[Text] JAPANESE: N lines`。
4. **日本語にならないもの**: パーティ設定ページの役割・注目対象・位置取りのドロップダウン(原作側の漏れ)、テーマ名(原文のまま)、ゲーム由来の文字列。
5. Path of the Companions を使う人には、Paths 用の日本語化パッチ(別ページ)を案内する。
6. スクリーンショット(バトルプラン、設定)。AI 利用の開示。他サイトへの転載はご遠慮ください。
7. 対応版: Fight With Me 0.5.0。原作の更新時はパッチを外さなくてよいが、新しい文言は英語のまま。
8. GitHub(ソースのみ): https://github.com/dolphag/Skyrim-Fight-With-Me-Japanese-translations-patch
