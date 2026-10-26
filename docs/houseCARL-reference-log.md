# houseCARL 参照ログ(試用中)

CLAUDE.md の「外部の参照」を使った回を 1 行ずつ記録する。数回分たまったら有効性を判断する(役に立たなければ CLAUDE.md の該当節を消す)。

参照先: Avick3110/houseCARL(GPL-3.0)、確認した版 v2.1.1(`8f03f27`)。読むのは主に `.claude/skills/skse-plugin-authoring/`。

| 日付 | 調べたかったこと | 読んだ資料 | 結果(役に立った/誤りを避けられた/役に立たなかった) |
|---|---|---|---|
| 2026-10-26 | Nexus API へのアクセス方法 | `src/housecarl-mcp/NexusClient.cs`、`docs/architecture/nexus.md`(`1037f7f`。上の版とは別の HEAD) | 方式(キーなしの v2 GraphQL)は分かった。実接続はプロキシ 403 で未検証のため、有効性は未判定 |
| 2026-10-26 | Nexus API の実接続(同じ資料の再確認) | 同上 | 役に立った: 方式どおり匿名で `mod` / `modFiles` が取れた。権限は取れず、これは資料に無かった |
