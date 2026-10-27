# Fight With Me 日本語化パッチ(このリポジトリ)

Fight With Me(FWM。Nexus 194766)の日本語化パッチ。原作者は hashhbbrown(GitHub: fatalCMD)。Path of the Companions(Paths。Nexus 196635)は別 MOD で、FWM の任意の連携先。**Paths の日本語化パッチは別リポジトリ**(dolphag/Skyrim-POTC-JP-Patch、2026-10-26 に分離)。
**0.5.0 から方式が変わった**: DLL パッチをやめ、原作が外部ファイルに分けたメッセージ(`Translations` フォルダ)の日本語版 `FightWithMe_JAPANESE.txt` を置く(経緯と仕様は `docs/FWM-0.5.0_Paths-1.0-findings.md`)。FWM 0.3.0 までの DLL パッチのツールは `legacy/0.3.0/`、手順は skill `pe-patch-workflow`(履歴扱い)。
配布は Nexus の FWM 用ページ(194874)。
常時読み込まれるので短く保つ。手順は `.claude/skills/`、用語は `docs/GLOSSARY.md`、版ごとの調査は `docs/` に置く。

## 最初のセッションで確認すること(未確認の事項)
- [x] テスト版の受け渡し: SendUserFile で zip を渡せる(ユーザーが受け取って実機試験済み、2026-10-26)。
- [x] タグの push: このクラウド環境からは **403 で拒否される**(2026-10-26、`git push origin <tag>`)。GitHub MCP にもタグ作成は無い。タグ(GitHub Release)はユーザーが、main の HEAD の commit に付ける。迂回しない。
- [x] 公開リポジトリの追加: `add_repo` は公開リポジトリなら読み取りのみ(clone 可)。非公開の読み書きは未確認。
- [ ] 原 MOD の zip は毎回ユーザーが添付する。翻訳のもとになる一覧は配布 zip を正とする(原作 git は古いことがある)。

## 応答のしかた
- 日本語。率直・技術的に正確に。褒めない・慰めない。誤りは、どの前提が誤りだったかを示して認める。
- 事実が不確かなら推測せず確認する(Nexus の権限・版・更新時刻、上流の状態など)。確認できなかったことは「未確認」と書く。
- 作業の最後に、やったこと/やっていないこと/ユーザーが判断すること、を分けて報告する。
- リポジトリのドキュメントと既存のコードに矛盾がある場合は、既存のコードで採用されている規約に従い、最終的な返信では、ドキュメントとコードの間で見つけた不一致を一つずつ指摘する。

## 権利・配布(絶対に守る)
- **GitHub はソースのみ。DLL・zip・フォントはコミットしない**(`.gitignore` で除外)。配布物(`FightWithMe_JAPANESE.txt` 入りの zip)は Nexus のみ。生成物も `out/`(git 管理外)。
- 逆アセンブル結果や文字列ダンプ(原 DLL の写し)も保存しない。必要なら再生成する(`legacy/0.3.0/dev/`)。
- 英日対応表(`translations_en_ja.csv`)の英語列は原作者のもの。0.5.0 の原作 git は GPL-3.0 を宣言しているが、Nexus ページの権限は別に確認する。README に英語列の扱いを明記し続ける。
- リリースごとに、原 MOD の Nexus ページの権限(Permissions and credits)をその時点で確認し、確認日を README に書く。変わっていたら止めてユーザーに報告。
- 原作者クレジット(hashhbbrown / GitHub fatalCMD)を、README・Nexus 説明・Nexus の **File credits 欄**の 3 か所に入れる。
- **ユーザーの許可なしにしない**: main への push、タグ、Nexus 投稿、原作者への連絡、削除。作業ブランチへの push は可。Nexus へのアップロードとタグ付け(GitHub Release)はユーザーが行う。
- ユーザーが添付した元ファイルは編集しない。コピーで作業する。

## 版番号
- FWM に連動する(FWM 0.5.0 → パッチ 0.5.0-N)。パッチだけの修正は枝番。タグは `v0.5.0-1` の形(Paths 用は別リポジトリ)。
- **Nexus の版と、zip 内 README の版を必ず一致させる**(0.1.0 と 0.1.0-1 の食い違いが過去にあった)。
- 版ごとに新しいセッションで始める。フォークで前の版の文脈を引き継がない(古い前提が混ざる)。前の版から持ち越す知識は `docs/` に書いてあるものだけ。

## 翻訳・表示のルール
- 用語は `docs/GLOSSARY.md`。skill→**アビリティ**、手持ち→**武器**。
- 文体・書式・下訳の使い方など訳全般の方針は `docs/TRANSLATION_POLICY.md`(下書き。【要決定】の項目は未決)。
- 使える漢字は `tools/jp_kanji.txt` の範囲内(範囲外は `lang_build.py` が失敗)。ゲーム由来の文字列は変えられない → README で EnableChinese を推奨している。
- HUD 通知のフォントに `→`(U+2192)が無い(0.3.0 での観察。0.5.0 は未確認)。ASCII 記号・矢印に頼らない。
- 折り返しは ASCII スペースでしか起きない。長文は文節区切りにスペースを入れる(`lang_build.py` が janome で自動)。
- 0.5.0 では表示倍率・位置の補正はできない(DLL を触らない)。窮屈な場所は訳を短くする。
- **利用者向けの文面(README・Nexus)では、原作に「翻訳機能」があるように書かない**。原作はメッセージを外部ファイルに出しているだけ(翻訳のためではあるが、機能として謳われているわけではない)。旧 DLL 版(0.3.0-2 以前)との違いは、旧版を使っていた人への注意に絞る。Paths は別 MOD の任意の連携先として書く。
- 言語は `sLanguage`(ゲームか各 INI)。JAPANESE のときは `FightWithMe_JAPANESE.txt`、ENGLISH のときは同じ内容の `FightWithMe_JA_ENGLISH.txt`(英語設定のまま日本語化している環境向け。名前は原作の英語ファイルより後に並ぶものにする)が読まれる。`_user.ini` は配らない(個人設定を消すため)。英語版ゲームの利用者には、`FightWithMe_user.ini` への設定を README で案内する。日本語フォントが必須: 原作のテーマ用フォントは日本語を含まない。**翻訳と同じ zip に同梱する**(別ファイルにすると、同じページ名の MOD として MO2 に入れるとき「一つにまとめる/置き換える」のダイアログが出て混乱するため。2026-10-26 に統合)。`tools/make_font_pack.py`(ユーザーが添付する OFL のフォントから作る。フォントは GitHub に置かない。出力は決定的)。特定の外部作品(MTG 等)を強調しない。

## 作業の進め方
- 手順の詳細は skill `lang-text-workflow`(生成・検査・テスト版 zip)、`release-package`(README・Changelog・配布 zip・Nexus 文面・タグ)。`pe-patch-workflow` は 0.3.0 まで。zip 作成は `tools/make_zip.py`。テストの前に、ユーザーの SKSE ログの 1 行目の版と `[Text] JAPANESE: N lines` を確認する。
- **実機(ゲーム内)確認なしにリリースしない**。テスト版は `out/` に `test<N>` で作り(git 管理外)、ユーザーのスクリーンショットと所見で直す。
- 逆アセンブル・アドレス調査の結果は必ずファイルに残す(`docs/` またはコード内コメント)。会話には残らない前提で作業する。
- 大きいファイルは全文を読まず、必要な範囲だけ読む。
- 開発用の依存: `pip install -r requirements-dev.txt`(`python3 -I` で実行)。

## 外部の参照(試用中)
- houseCARL(Avick3110/houseCARL、GPL-3.0、確認したのは v2.1.1 = `8f03f27`)の `.claude/skills/skse-plugin-authoring/` を、SKSE プラグイン(CommonLibSSE-NG)の構造を調べるときだけ読む。**セッションにリポジトリを追加しない**(houseCARL 側の CLAUDE.md が運用ルールと競合するため)。必要なときだけ `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/Avick3110/houseCARL <作業ディレクトリ外>` で取得して読む。コピーはしない。調査結果は自分の言葉で `docs/` に書き、出典を併記する。
- 使った回は `docs/houseCARL-reference-log.md` に 1 行記録する。数回分たまったら有効性を判断し、役に立たなければこの節を消す。

## Nexus の確認
- WebFetch は Nexus で失敗しやすい(PROVENANCE_REQUIRED)。ブラウザ(Claude in Chrome 等)が使える場合はそれで開く。使えない場合は、ユーザーに確認を依頼する。
- API で引く手段: skill `nexus-check`(`tools/nexus_query.py`、キー不要、版・ファイル一覧は実測済み)。環境が api.nexusmods.com を許可している必要がある。**権限(Permissions)と配布 zip のダウンロードは API で取れない**(後者は非プレミアムで 403)→ ブラウザかユーザー確認、zip はユーザーが添付。詳細は `docs/nexus-api-notes.md`。
- ページの権限・版・ファイル名・更新時刻は、実際に読み取ったものだけを事実として扱う。
