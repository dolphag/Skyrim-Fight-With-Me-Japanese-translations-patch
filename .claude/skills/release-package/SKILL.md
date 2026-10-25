---
name: release-package
description: FWM / Paths 日本語化パッチのリリース準備(配布 zip、README、Nexus 用テキスト、タグ)。版番号・クレジット・権限確認・作業の順序のチェックリスト。
---

# リリース準備チェックリスト

配布はユーザーが行う(Nexus アップロード、GitHub のタグ/Release)。このスキルは準備と確認。

## 順序(守る)
1. 実機確認が済んでいること(ユーザーの「OK」)。
2. **原 MOD の Nexus ページの権限をその時点で確認**(Permissions and credits)。確認日を README に書く。変更があれば止めてユーザーに報告。
3. 版番号を決める: 原 MOD に連動(FWM 0.3.0-N、Paths 0.1.0-N)。**Nexus の版と zip 内 README の版を一致させる**。
4. README 雛形(`release/README_{Japanese,English}.{fwm,paths}.txt`)を更新する: 1 行目の版、変更点、**更新履歴(Changelog。最新を先頭に追記)**、確認日、必要なら注意書き。ハッシュは `{ORIG_SHA}` / `{OUT_SHA}` のまま(zip 作成時に埋まる)。翻訳表 CSV(`fwm_export_csv.py`)と対照表(`paths_table.py`)、リポジトリの README も更新する。
5. zip を作る(FWM 用・Paths 用の 2 本。DLL は同一):
   - `git clone --depth 1 https://github.com/fatalCMD/fight-with-me <作業ディレクトリ外>` で原作の `THIRD-PARTY-NOTICES.md` を取得する。
   - `python3 -I tools/make_zip.py release fwm   out/<最終>.dll --version <版> --notices <THIRD-PARTY-NOTICES.md>`
   - `python3 -I tools/make_zip.py release paths out/<最終>.dll --version <版> --notices <THIRD-PARTY-NOTICES.md>`
   - README の 1 行目に版がなければ失敗する(Nexus の版との食い違い防止)。出力 DLL の SHA-256 が README の値と一致していることも確認する。
6. Nexus 用テキストを作る: 前回の文面 `release/NEXUS_TEXT_<前回の版>.md` を複製して更新(ファイル更新用の「更新履歴」「ファイルの説明」と、ページの説明文。File credits 欄の指示も含める)。
7. **main へ統合 → main の HEAD を確認 → ユーザーがそのコミットにタグ**(main 更新前にタグを打って旧コミットを指した事故あり)。タグは GitHub の Release で、ユーザーが付ける。
8. ユーザーが Nexus にアップロードしたら、ブラウザで開いて確認する(版、ファイル名、サイズ、説明、File credits 欄)。

## zip の構成(`tools/make_zip.py` が作る)
```
SKSE/Plugins/FightWithMe.dll
README_Japanese.txt / README_English.txt
THIRD-PARTY-NOTICES_FightWithMe.md   (原 MOD のものをそのまま)
```
- FWM 用(`Fight With Me - Japanese Translations Patch <版>.zip`)と Paths 用(`Paths - Japanese Translations Patch <版>.zip`)で、DLL は同一。README のタイトルと冒頭だけが違う(Paths 用は「Paths の文字列は FWM の DLL の中」から説明する)。

## README / Nexus 文面に必ず入れること
- 原作者クレジット(hashhbbrown / fatalCMD)、原 MOD へのリンク、権限の確認日。
- ロード順 FWM → Paths → 日本語化パッチ(最後)。EnableChinese の推奨。
- 元 DLL と出力 DLL の SHA-256。他版には使わないこと。更新時は先にパッチを外すこと。
- 「GitHub にはソースのみ、バイナリは Nexus のみ」。AI 利用の開示。非公式で、原作者に問い合わせないこと。
- 特定の外部作品(MTG 等)を強調しない。

## Nexus の File credits 欄
- 原作者(hashhbbrown)を入れる。空のままにしない。
