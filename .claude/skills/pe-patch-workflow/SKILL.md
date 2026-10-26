---
name: pe-patch-workflow
description: FightWithMe.dll の日本語化パッチを作る・直す・検証するときの手順。翻訳表の変更、表示位置の調整、新しい版への移行(アドレスの再導出)、ビルドと検証の流れ、既知の落とし穴。
---

# FWM / Paths DLL パッチの作業手順(0.3.0 まで・履歴扱い)

**FWM 0.5.0 / Paths 1.0 以降は使わない**(翻訳ファイル方式に変わった。skill `lang-text-workflow`)。0.3.0 のバイナリを直すときだけ読む。`tools/make_zip.py` は 0.5.0 向けに書き換えたため、この手順の「テスト版 zip」は旧版のコミットで行う。

対象: `FightWithMe.dll`(FWM 0.3.0。Paths の文字列も同じ DLL にある)。静的な PE パッチ。アドレスは版固定。

## 前提
- 元 DLL はユーザーが添付する。SHA-256 が `tools/fwm_patch.py` の `ORIG_SHA256` と一致しなければ失敗する(0.3.0-2 の作業後に追加。別版への誤適用を防ぐ)。
- 作業ディレクトリは `x/SKSE/Plugins/FightWithMe.dll`(元)と `out/`(出力、git 管理外)。依存は `pip install -r requirements-dev.txt`。実行は `python3 -I`。

## 通常の変更(翻訳・表示の調整)
1. 訳文は `tools/fwm_trans1..6.py`(Paths は `fwm_trans6.py` と `fwm_names6.py`)。FWM と共有する文字列(Taunt, Heal など)は FWM 側の訳に統一。統合順は T1..T6 で後勝ち。
2. 書式の検査: `python3 -I tools/fwm_fmtcheck.py`(`{}` などのフィールド数の一致)。
3. 生成: `python3 -I tools/fwm_patch.py x/SKSE/Plugins/FightWithMe.dll out/test<N>.dll out/test<N>.json`
4. 検証(全部通す):
   - `python3 -I tools/fwm_verify.py <元> <出力>`(変更バイトがすべて記録され、参照が新セクションに届くか)
   - `python3 -I tools/fwm_emu_stub.py <出力> <json>`(スタブの振り分け・拡大率。unicorn)
   - `python3 -I tools/fwm_scan_flag.py <元> <出力>`(レジスタを長さとフラグの両用にしている箇所の検出)。**既知の誤検出以外が出たら止めて調べる**。既知: 0x10305b(ecx の値がアドレスで変わる)。
5. 翻訳表の更新: `python3 -I tools/fwm_export_csv.py <json>.sites > translations_en_ja.csv`、Paths 対照表: `python3 -I tools/paths_table.py <FWM の include/FWM/Paths.h> > PATHS_TABLE.md`。
6. テスト版 zip を作ってユーザーに渡す(経路は CLAUDE.md の「最初のセッションで確認すること」)。
   - メモを `release/TEST_MEMO_TEMPLATE.txt` の形で書く(前回からの変更、確認してほしい点、補足)。
   - `python3 -I tools/make_zip.py test out/test<N>.dll <N> --memo <メモ>` → `out/FWM_Paths_test<N>.zip`(DLL + テスト用メモ.txt)。
   - ユーザーのスクリーンショットと所見で直す。

## 表示位置の調整(`tools/fwm_cfg.py`)
- 日本語は `FONT_SCALE`(1.4)で拡大され、**上端基準で下に伸びる** → アイコン・帯に対して低く見える。
- 場所ごとの手段: `LABEL_LIFT` / `TEXT_LIFT`(y を size×係数だけ上げる)、`SPACING_CONSTS`(rip 相対の float 定数を場所ごとに書き換え)、`FORCE_SCALE`(呼び出しごとの倍率)、`TITLE_CALLS`(題字は拡大しない)、`TIP_SCALE`(ツールチップ)。
- 修正前に、どの呼び出しアドレスの話かを特定する(`tools/dev/xref.py`、`annot.py`)。推測で全体の倍率を変えない。

## 既知の落とし穴
- ImGui の `Paragraph` は ASCII スペースでしか折り返さない → 長文は文節区切りにスペース(janome、`fwm_trans6.py` の `_wrapfix`)。
- ImGui のフォントは `tools/jp_kanji.txt` の漢字だけ。範囲外はビルド失敗(咆・哮 など)。HUD 通知のフォントには `→` が無い。
- `Label`/`LabelWidth` は 1 バイトずつ描画して UTF-8 を壊す → 日本語を含むときだけ `Text`/`TextSize` にスタブで振り分ける。
- 長さ即値、インライン展開された `std::string`、ポインタスロット、デストラクタのフラグ兼用レジスタ(edi など)が代表的な事故源。

## 新しい版へ移行するとき
1. 新しい元 DLL を受け取り、SHA-256 を記録する。
2. 旧版の命令列(アドレスをマスク)から、新版の対応アドレスを探す: `tools/dev/sigfind.py`(`sig2.py` が使用例)。
3. 文字列の増減(新規・削除)を洗い出し、翻訳表と `fwm_cfg.py` の各表を更新する。
4. 版ごとの調査結果を `docs/ADDRESSES-<版>.md` に残す。前の版のセッションの文脈を引き継がない。
