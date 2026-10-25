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
4. README(日本語・英語)、翻訳表 CSV、対照表、出力 DLL の SHA-256 を更新する。
5. zip を作る(構成は下記)。
6. Nexus 用テキスト(更新履歴・説明・クレジット欄)を作る。
7. **main へ統合 → main の HEAD を確認 → ユーザーがそのコミットにタグ**(main 更新前にタグを打って旧コミットを指した事故あり)。タグは GitHub の Release で、ユーザーが付ける。
8. ユーザーが Nexus にアップロードしたら、ブラウザで開いて確認する(版、ファイル名、サイズ、説明、File credits 欄)。

## zip の構成
```
SKSE/Plugins/FightWithMe.dll
README_Japanese.txt / README_English.txt
THIRD-PARTY-NOTICES_FightWithMe.md   (原 MOD のものをそのまま)
```
- FWM 用と Paths 用で、DLL は同一。README のタイトルと冒頭だけが違う(Paths 用は「Paths の文字列は FWM の DLL の中」から説明する)。
- zip は Python の `zipfile` で作る(パス区切りと改行を揃える)。

## README / Nexus 文面に必ず入れること
- 原作者クレジット(hashhbbrown / fatalCMD)、原 MOD へのリンク、権限の確認日。
- ロード順 FWM → Paths → 日本語化パッチ(最後)。EnableChinese の推奨。
- 元 DLL と出力 DLL の SHA-256。他版には使わないこと。更新時は先にパッチを外すこと。
- 「GitHub にはソースのみ、バイナリは Nexus のみ」。AI 利用の開示。非公式で、原作者に問い合わせないこと。
- 特定の外部作品(MTG 等)を強調しない。

## Nexus の File credits 欄
- 原作者(hashhbbrown)を入れる。空のままにしない。
