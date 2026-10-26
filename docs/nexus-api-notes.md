# Nexus API メモ

2026-10-26 調査。出典: houseCARL(Avick3110/houseCARL、GPL-3.0、`1037f7f`)の `src/housecarl-mcp/NexusClient.cs` と `docs/architecture/nexus.md`。コードはコピーしていない。

## 分かっていること(houseCARL の記述による。ここでは未検証)
- v2 GraphQL の読み取りは公開・匿名。エンドポイント `https://api.nexusmods.com/v2/graphql`、POST、`{query, variables}`。認証ヘッダなし。
- 使われているクエリ: `mods`(検索)、`mod(modId, gameId)`、`modFiles(modId, gameId)`、`game(domainName|id)`、`fileHashes(md5s)`。
- Skyrim SE の game id は 1704(ドメイン名 `skyrimspecialedition`)。
- 失敗は HTTP 429(レート制限)、GraphQL の `errors` 配列で返る。

## 未確認だった事項(古い記述。下の「2026-10-26 実測」で更新済み)
- このセッションでは `api.nexusmods.com` への接続がプロキシに拒否された(CONNECT 403)ため、**実際の応答は一度も見ていない**。`tools/nexus_query.py` の実接続は未試験。オフラインで確認したのは mutation 拒否と接続失敗時のメッセージのみ。
- 匿名で本当に読めるか(houseCARL の主張が現在も正しいか)。
- フィールド `description` / `changelogText` などの有無。**権限(Permissions and credits)に当たるフィールドがあるか**。
- 無ければの代替: v1 REST + 個人 API キー(`apikey` ヘッダ)。houseCARL は使っていない。キーは環境の secrets に置き、リポジトリに入れない。

## 2026-10-26 実測(このクラウド環境から。api.nexusmods.com は許可されていた)
匿名(API キーなし)で応答が返った。houseCARL の主張どおり。

### できること(実際に取れた)
- `mod`: modId / name / version / summary / author / category / endorsements / downloads / updatedAt / createdAt / status。ほかに `description`(ページ本文の BBCode)、`tags`、`modRequirements`、`fileSize`。
- `modFiles`: fileId / name / version / **category(MAIN・OLD_VERSION・ARCHIVED)** / date(epoch 秒)/ description / changelogText / sizeInBytes / primary / scanned。
- `modFileContents`(filter に modId・gameId を `[{value:N, op:EQUALS}]` で渡す): zip 内のファイルパスとサイズ。**取れたのは 0.1.0〜0.3.0 の 4 ファイル分のみ(16 件)。0.5.0 の 2 ファイル(825447, 825644)は 0 件**(インデックス未作成か、理由は未確認)。
- 導入: `__schema` / `__type` の introspection が通る(フィールド確認に使える)。

### できないこと・分からないこと
- **Permissions and credits(権限)に当たるフィールドは `Mod` 型に無い**(フィールド一覧を確認)。`description` 本文にも権限の記述は無かった。→ 権限はブラウザかユーザー確認のまま。
- zip の中身そのもの(ファイル内容)は取れない。ダウンロードは認証が要る(未試験、試さない)。0.5.0 の `Translations` の中身はこの API では見えない → 配布 zip はユーザーが添付する。
- 書き込み(アップロード・説明文の更新)は不可。送らない方針。
- 非公開・審査中のページや自分の下書きは見えない(未試験)。

### 0.5.0 の差し替え(2026-10-26 に判明)
- 825447: 2026-10-24 20:04 UTC、2,312,890 バイト(ARCHIVED)。
- 825644: 2026-10-25 04:43 UTC、2,323,130 バイト(MAIN)。差は 10,240 バイト。changelogText は同一。
- 同じ版番号 0.5.0 のまま約 8 時間後に差し替えられている。パッチの元にした zip がどちらかは記録が無い → 要確認。
