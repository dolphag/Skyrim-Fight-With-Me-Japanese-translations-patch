---
name: release-package
description: Fight With Me 日本語化パッチのリリース準備(配布 zip、README、Nexus 用テキスト、タグ)。版番号・クレジット・権限確認・作業の順序のチェックリスト。
---

# リリース準備チェックリスト

配布はユーザーが行う(Nexus アップロード、GitHub のタグ/Release)。このスキルは準備と確認。

## 順序(守る)
1. 実機確認が済んでいること(ユーザーの「OK」)。
2. **原 MOD の Nexus ページの権限(Permissions and credits)をその時点で確認**(ユーザーが貼り付ける)。確認日を README に書く。変更があれば止めてユーザーに報告。
3. 版番号を決める: FWM に連動(FWM 0.5.0 → 0.5.0-N)。**Nexus の版と zip 内 README の版を一致させる**。
4. README 雛形(`release/README_{Japanese,English}.txt`)を更新する: 1 行目の版、変更点、**更新履歴(最新を先頭に追記)**、確認日。`{SHA_JA}` はそのまま(zip 作成時に埋まる)。リポジトリの README と `translations_en_ja.csv` も更新する。
5. zip を作る(1 本。翻訳と日本語フォントを同梱する):
   - 翻訳: `python3 -I tools/lang_build.py --fwm <FWM zip> --out out/ja`(検査つき)
   - フォント: `python3 -I tools/make_font_pack.py --font NotoSansJP-Medium.ttf --license OFL.txt --out out/font`(ユーザーがフォントと OFL を添付。内部名を付け替える。GitHub にはコミットしない)
   - `python3 -I tools/make_zip.py release out/ja --font-dir out/font --version <版>`
   - README の 1 行目に版がなければ失敗する。
6. Nexus 用テキストを作る: 前回の文面 `release/NEXUS_TEXT_<前回の版>.md` を複製して更新(ファイル説明・更新履歴・ページの説明文・File credits 欄の指示)。
7. **main へ統合 → main の HEAD を確認 → ユーザーがそのコミットにタグ**(`v<版>`、例 `v0.5.0-1`)。タグはこのクラウド環境から push できない(403)。GitHub の Release でユーザーが付ける。main 更新後に docs だけの commit を足すと HEAD が動くので注意。
8. ユーザーが Nexus にアップロードしたら、確認を依頼する(版、ファイル名、サイズ、説明、File credits 欄)。

## zip の構成(`tools/make_zip.py` が作る)
```
SKSE/Plugins/FightWithMe/Translations/FightWithMe_JAPANESE.txt
SKSE/Plugins/Fonts/{Lora,Spectral,BarlowSemiCondensed}-SemiBold.ttf + FONT-LICENSE.txt
README_Japanese.txt / README_English.txt
```
- 原作のファイル(DLL・画像・フォント)は入れない。入るのは、原作の英語の文言(左列)と日本語訳だけ。
- 日本語フォントは日本語の表示に必須なので、翻訳と同じ zip に入れる(別ファイルにすると、MO2 で同名 MOD のダイアログが出て混乱する)。優先順位は 原作 → 本パッチ。Path of the Companions の日本語化パッチにも同じフォントが入る(ビルドは決定的で、同一のファイル)。

## README / Nexus 文面に必ず入れること
- 原作者クレジット(hashhbbrown / fatalCMD)、原 MOD へのリンク、権限の確認日。
- Paths は**任意の連携先**として書く(併用するなら Paths 用パッチ(別リポジトリ・別ページ)も入れるよう案内)。旧 DLL 版(0.3.0-2 以前)を外すよう注意する。
- 日本語にならないときの手順(`sLanguage = JAPANESE`、`FightWithMe_user.ini`)、日本語にならないもの(ドロップダウン等)。
- 訳文ファイルの SHA-256。原作更新時、パッチを外す必要は無いが、新しい文言は英語のまま。
- 「GitHub にはソースのみ、配布物は Nexus のみ」。AI 利用の開示。非公式で、原作者に問い合わせないこと。
- 「原作に翻訳機能がある」ように書かない。原作はメッセージを外部ファイルに出しているだけ。

## Nexus の File credits 欄
- 原作者(hashhbbrown)を入れる。空のままにしない。Noto Sans JP(Adobe)も(フォントを同梱しているため)。
