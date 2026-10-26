---
name: release-package
description: FWM / Paths 日本語化パッチのリリース準備(配布 zip、README、Nexus 用テキスト、タグ)。版番号・クレジット・権限確認・作業の順序のチェックリスト。
---

# リリース準備チェックリスト

**0.5.0 / 1.0 以降の方式(翻訳ファイル + 日本語フォント別ファイル)向けに更新(2026-10-26)。** 0.3.0 までの DLL 方式の雛形・文面は `legacy/0.3.0/release/`。

配布はユーザーが行う(Nexus アップロード、GitHub のタグ/Release)。このスキルは準備と確認。

## 順序(守る)
1. 実機確認が済んでいること(ユーザーの「OK」)。
2. **原 MOD の Nexus ページの権限をその時点で確認**(Permissions and credits)。確認日を README に書く。変更があれば止めてユーザーに報告。
3. 版番号を決める: 原 MOD に連動(FWM 0.3.0-N、Paths 0.1.0-N)。**Nexus の版と zip 内 README の版を一致させる**。
4. README 雛形(`release/README_{Japanese,English}.{fwm,paths}.txt`)を更新する: 1 行目の版、変更点、**更新履歴(Changelog。最新を先頭に追記)**、確認日、必要なら注意書き。ハッシュは `{ORIG_SHA}` / `{OUT_SHA}` のまま(zip 作成時に埋まる)。翻訳表 CSV(`fwm_export_csv.py`)と対照表(`paths_table.py`)、リポジトリの README も更新する。
5. zip を作る(4 本: FWM 用・Paths 用の翻訳パッチ、同じ名前の日本語フォント 2 本):
   - 翻訳: `python3 -I tools/lang_build.py --fwm <FWM zip> --paths <Paths zip> --out out/ja`(検査つき)
   - フォント: `python3 -I tools/make_font_pack.py --font NotoSansJP-Medium.ttf --license OFL.txt --out out/font`(ユーザーがフォントと OFL を添付。内部名を付け替える。GitHub にはコミットしない)
   - `python3 -I tools/make_zip.py release fwm out/ja --version <版>` / `release paths ...` / `font fwm out/font --version <版>` / `font paths ...`
   - README の 1 行目に版がなければ失敗する。`{SHA_FWM_JA}` `{SHA_PATHS_JA}` は訳文ファイルの SHA-256 で埋まる。
6. Nexus 用テキストを作る: 前回の文面 `release/NEXUS_TEXT_<前回の版>.md`(0.5.0-1 が現行)を複製して更新(ファイル更新用の「更新履歴」「ファイルの説明」と、ページの説明文。File credits 欄の指示も含める)。
7. **main へ統合 → main の HEAD を確認 → ユーザーがそのコミットにタグ**(main 更新前にタグを打って旧コミットを指した事故あり)。タグは GitHub の Release で、ユーザーが付ける。
8. ユーザーが Nexus にアップロードしたら、ブラウザで開いて確認する(版、ファイル名、サイズ、説明、File credits 欄)。

## zip の構成(`tools/make_zip.py` が作る)
```
翻訳パッチ(fwm) : SKSE/Plugins/FightWithMe/Translations/FightWithMe_JAPANESE.txt + README_Japanese.txt / README_English.txt
翻訳パッチ(paths): 上 + FightWithMePaths_JAPANESE.txt
フォント        : SKSE/Plugins/Fonts/{Lora,Spectral,BarlowSemiCondensed}-SemiBold.ttf + FONT-LICENSE.txt + README_*.txt
```
- 原作のファイル(DLL・画像・フォント)は入れない。入るのは、原作の英語の文言(左列)と日本語訳だけ。
- 日本語フォントは、日本語の表示に必須。説明に明記する。FWM と Paths で同名の原作フォントがあるので、優先順位は 原作 → 翻訳 → フォント。

## README / Nexus 文面に必ず入れること
- 原作者クレジット(hashhbbrown / fatalCMD)、原 MOD へのリンク、権限の確認日。
- ロード順 FWM → Paths → 日本語化パッチ(最後)。EnableChinese の推奨。
- 訳文ファイルの SHA-256。原作の更新時、パッチを外す必要は無いが、新しい文言は英語のまま(パッチの更新待ち)。旧 DLL 方式の版と併用しない。
- 日本語にならないときの手順(`sLanguage = JAPANESE` を両方の `_user.ini` に)、日本語にならないもの(ドロップダウン等)。
- 「GitHub にはソースのみ、バイナリは Nexus のみ」。AI 利用の開示。非公式で、原作者に問い合わせないこと。
- 特定の外部作品(MTG 等)を強調しない。

## Nexus の File credits 欄
- 原作者(hashhbbrown)を入れる。空のままにしない。
