---
name: lang-text-workflow
description: FWM 0.5.0 / Paths 1.0 以降の日本語化(翻訳テキスト *_JAPANESE.txt)を作る・直す・検証するときの手順。訳の追加、新しい版への追従、テスト版 zip。
---

# 翻訳テキスト方式の作業手順(0.5.0 / 1.0 以降)

DLL は触らない。原作の翻訳ファイル機構に `*_JAPANESE.txt` を渡す。背景と仕様は `docs/FWM-0.5.0_Paths-1.0-findings.md`。
(0.3.0 までの DLL パッチは skill `pe-patch-workflow`。0.5.0 には使えない。)

## 前提
- 原 MOD の zip(FWM 用、Paths 用)をユーザーが添付する。**テンプレートは配布 zip を正とする**(git のソースは配布版より古いことがある)。
- 依存: `pip install -r requirements-dev.txt`(janome)。実行は `python3 -I`。

## 通常の変更(訳の修正・追加)
1. 訳の正本は `translations_en_ja.csv`(列 `en,ja`。鍵 = 英語全文、`\n` は実改行。ja は折り返し用スペースを入れる前の文)。
   英語のままにする項目は ja を en と同じ値にする。
2. 生成と検査: `python3 -I tools/lang_build.py --fwm <FWM zip> --paths <Paths zip> --out out/ja`
   - 未訳、書式欄(`{}` `{:.0f}` `{0}`)の種類・順序の不一致、`tools/jp_kanji.txt` 範囲外の漢字、CSV に残った古い項目があると失敗する。
   - 範囲外の漢字はひらがなにする(叩→たたく、噛→かむ など)。番号付き書式(`{1}`)にすれば順序を入れ替えられる。
3. テスト版: メモを `release/TEST_MEMO_TEMPLATE.txt` の形で書き、`python3 -I tools/make_zip.py test out/ja <N> --memo <メモ>` → `out/FWM_Paths_ja_test<N>.zip`。
   ユーザーへは SendUserFile で渡す。ユーザーのスクリーンショットと所見で直す。

## 新しい版へ移行するとき
1. 新しい zip のテンプレートと旧 CSV を比べる(`lang_build.py` の「未訳」「テンプレートに無い項目」が差分)。同じ英語は訳が自動で当たる。
2. 変わった英語は訳を直す(数値が変わっただけの文も、鍵が変わるので別項目になる)。古い項目は CSV から外す。
3. 版ごとの調査は `docs/` に残す。新しいセッションで始める。

## 落とし穴
- **テストの前に、ユーザーの SKSE ログ(FightWithMe 系 .log)の 1 行目で版を確認する**。`Fight With Me 0.3.0.0 loading.` なら、0.5.0 が入っていない(test1/test2 は旧版のまま試されて無効だった)。`[Text] JAPANESE: N lines from ...` が出れば読み込み成功。テスト版メモには、最初にログの該当行を送ってもらうよう書く。
- 鍵は 1 文字でも違えば当たらない(英語のまま表示される)。文字化けした鍵(`Â·`)もそのまま一致させる。
- 言語が JAPANESE でないと読まれない。各 DLL が自分の INI(`_user.ini` 含む)の `sLanguage` を見る。ログの `[Text] JAPANESE: N lines` で確認する。
- 折り返しは ASCII スペースのみ。`lang_build.py` が 19 文字以上の行に janome で入れる(`--no-wrap` で無効化)。
- 位置・倍率は原作のレイアウトのまま。窮屈な場所は訳を短くして対応する(DLL 側では直せない)。
