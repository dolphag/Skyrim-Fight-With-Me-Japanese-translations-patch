# Fight With Me / Paths 日本語化パッチ(このリポジトリ)

FWM(Nexus 194766)と Path of the Companions(Paths。Nexus で新 MOD、ID 196635)の日本語化パッチ。原作者は hashhbbrown(GitHub: fatalCMD)。
**0.5.0 / 1.0 から方式が変わった**: DLL パッチをやめ、原作の翻訳ファイル機構に `*_JAPANESE.txt` を渡す(経緯と仕様は `docs/FWM-0.5.0_Paths-1.0-findings.md`)。FWM 0.3.0 / Paths 0.1.0 までの DLL パッチは skill `pe-patch-workflow`(履歴扱い)。
配布は Nexus の 2 ページ(FWM 用 194874、Paths 用は新 MOD 向けに新規作成の見込み。旧 196104 は旧 Paths 用)。
常時読み込まれるので短く保つ。手順は `.claude/skills/`、用語は `docs/GLOSSARY.md`、版ごとの調査は `docs/` に置く。

## 最初のセッションで確認すること(未確認の事項)
- [ ] **テスト版の受け渡し経路**: SendUserFile で zip を渡した(2026-10-26、test1)。ユーザーが受け取れたかは**未確認**。確認できたらここを消して確定を書く。
- [x] 公開リポジトリの追加: `add_repo` は公開リポジトリなら読み取りのみ(clone 可)。非公開の読み書きは未確認。
- [ ] 原 MOD の zip(FWM 用・Paths 用)は毎回ユーザーが添付する。翻訳テンプレートは配布 zip を正とする(git のソースは古いことがある)。

## 応答のしかた
- 日本語。率直・技術的に正確に。褒めない・慰めない。誤りは、どの前提が誤りだったかを示して認める。
- 事実が不確かなら推測せず確認する(Nexus の権限・版・更新時刻、上流の状態など)。確認できなかったことは「未確認」と書く。
- 作業の最後に、やったこと/やっていないこと/ユーザーが判断すること、を分けて報告する。

## 権利・配布(絶対に守る)
- **GitHub はソースのみ。DLL・zip・フォントはコミットしない**(`.gitignore` で除外)。配布物(`*_JAPANESE.txt` 入りの zip)は Nexus のみ。生成した `*_JAPANESE.txt` も `out/`(git 管理外)。
- 逆アセンブル結果や文字列ダンプ(原 DLL の写し)も保存しない。必要なら再生成する(`tools/dev/`)。
- 英日対応表(`translations_en_ja.csv`)の英語列は原作者のもの。0.5.0 の原作 git は GPL-3.0 を宣言しているが、Nexus ページの権限は別に確認する。README に英語列の扱いを明記し続ける。
- リリースごとに、原 MOD の Nexus ページの権限(Permissions and credits)をその時点で確認し、確認日を README に書く。変わっていたら止めてユーザーに報告。
- 原作者クレジット(hashhbbrown / GitHub fatalCMD)を、README・Nexus 説明・Nexus の **File credits 欄**の 3 か所に入れる。
- **ユーザーの許可なしにしない**: main への push、タグ、Nexus 投稿、原作者への連絡、削除。作業ブランチへの push は可。Nexus へのアップロードとタグ付け(GitHub Release)はユーザーが行う。
- ユーザーが添付した元ファイルは編集しない。コピーで作業する。

## 版番号
- 原 MOD に連動する(FWM 0.3.0 → パッチ 0.3.0-N、Paths 0.1.0 → 0.1.0-N)。パッチだけの修正は枝番。
- **Nexus の版と、zip 内 README の版を必ず一致させる**(0.1.0 と 0.1.0-1 の食い違いが過去にあった)。
- 版ごとに新しいセッションで始める。フォークで前の版の文脈を引き継がない(古い前提が混ざる)。前の版から持ち越す知識は `docs/` に書いてあるものだけ。
- 0.5.0 / 1.0 以降は FWM と Paths の版が独立する。パッチの版は各 MOD に連動(FWM 0.5.0 → 0.5.0-N、Paths 1.0.0 → 1.0.0-N)。

## 翻訳・表示のルール
- 用語は `docs/GLOSSARY.md`。skill→**アビリティ**、「スキルツリー」は使わずツリー、手持ち→**武器**、従者専用ツリー。
- 使える漢字は `tools/jp_kanji.txt` の範囲内(範囲外は `lang_build.py` が失敗)。ゲーム由来の文字列は変えられない → README で EnableChinese を推奨している。
- HUD 通知のフォントに `→`(U+2192)が無い(0.3.0 での観察。0.5.0 は未確認)。ASCII 記号・矢印に頼らない。
- 折り返しは ASCII スペースでしか起きない。長文は文節区切りにスペースを入れる(`lang_build.py` が janome で自動)。
- 0.5.0 では表示倍率・位置の補正はできない(DLL を触らない)。窮屈な場所は訳を短くする。
- 言語は `sLanguage`(ゲームか各 INI)。英語版ゲームの利用者には、両 DLL の `_user.ini` への設定を README で案内する。特定の外部作品(MTG 等)を強調しない。

## 作業の進め方
- 手順の詳細は skill `lang-text-workflow`(0.5.0 以降: 生成・検査・テスト版 zip)、`release-package`(README・Changelog・配布 zip・Nexus 文面・タグ。**0.5.0 向けの `release/` 雛形は未更新**)。`pe-patch-workflow` は 0.3.0 まで。zip 作成は `tools/make_zip.py`。
- **実機(ゲーム内)確認なしにリリースしない**。テスト版は `out/` に `test<N>` で作り(git 管理外)、ユーザーのスクリーンショットと所見で直す。
- 逆アセンブル・アドレス調査の結果は必ずファイルに残す(`docs/` またはコード内コメント)。会話には残らない前提で作業する。
- 大きいファイルは全文を読まず、必要な範囲だけ読む。
- 開発用の依存: `pip install -r requirements-dev.txt`(`python3 -I` で実行)。

## 外部の参照(試用中)
- houseCARL(Avick3110/houseCARL、GPL-3.0、確認したのは v2.1.1 = `8f03f27`)の `.claude/skills/skse-plugin-authoring/` を、SKSE プラグイン(CommonLibSSE-NG)の構造を調べるときだけ読む。**セッションにリポジトリを追加しない**(houseCARL 側の CLAUDE.md が運用ルールと競合するため)。必要なときだけ `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/Avick3110/houseCARL <作業ディレクトリ外>` で取得して読む。コピーはしない。調査結果は自分の言葉で `docs/` に書き、出典を併記する。
- 使った回は `docs/houseCARL-reference-log.md` に 1 行記録する。数回分たまったら有効性を判断し、役に立たなければこの節を消す。

## Nexus の確認
- WebFetch は Nexus で失敗しやすい(PROVENANCE_REQUIRED)。ブラウザ(Claude in Chrome 等)が使える場合はそれで開く。使えない場合は、ユーザーに確認を依頼する。
- ページの権限・版・ファイル名・更新時刻は、実際に読み取ったものだけを事実として扱う。
