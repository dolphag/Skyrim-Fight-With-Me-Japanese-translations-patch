# Nexus API メモ

2026-10-26 調査。出典: houseCARL(Avick3110/houseCARL、GPL-3.0、`1037f7f`)の `src/housecarl-mcp/NexusClient.cs` と `docs/architecture/nexus.md`。コードはコピーしていない。

## 分かっていること(houseCARL の記述による。ここでは未検証)
- v2 GraphQL の読み取りは公開・匿名。エンドポイント `https://api.nexusmods.com/v2/graphql`、POST、`{query, variables}`。認証ヘッダなし。
- 使われているクエリ: `mods`(検索)、`mod(modId, gameId)`、`modFiles(modId, gameId)`、`game(domainName|id)`、`fileHashes(md5s)`。
- Skyrim SE の game id は 1704(ドメイン名 `skyrimspecialedition`)。
- 失敗は HTTP 429(レート制限)、GraphQL の `errors` 配列で返る。

## 未確認(実機で確認したら更新する)
- このセッションでは `api.nexusmods.com` への接続がプロキシに拒否された(CONNECT 403)ため、**実際の応答は一度も見ていない**。`tools/nexus_query.py` の実接続は未試験。オフラインで確認したのは mutation 拒否と接続失敗時のメッセージのみ。
- 匿名で本当に読めるか(houseCARL の主張が現在も正しいか)。
- フィールド `description` / `changelogText` などの有無。**権限(Permissions and credits)に当たるフィールドがあるか**。
- 無ければの代替: v1 REST + 個人 API キー(`apikey` ヘッダ)。houseCARL は使っていない。キーは環境の secrets に置き、リポジトリに入れない。
