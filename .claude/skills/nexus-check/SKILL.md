---
name: nexus-check
description: Nexus Mods の mod ページ(FWM 194766、パッチ 194874 など)の版・更新日・ファイル一覧・changelog を API で読む。リリース前の「原 MOD の最新版確認」「自分のページの版の確認」に使う。権限(Permissions and credits)は取れるか未確認。
---

# Nexus API で確認する

## 方式(houseCARL の `NexusClient.cs` に倣う)
- `POST https://api.nexusmods.com/v2/graphql`、本文は `{query, variables}` の JSON。**API キーなし**(houseCARL の主張。ここでは未確認 → `docs/nexus-api-notes.md`)。
- 読み取り専用。mutation/subscription は送らない。ユーザー入力は variables で渡す。
- 実行: `python3 -I tools/nexus_query.py mod <modId> [--game skyrimspecialedition]`(概要+ファイル一覧)、`raw '<query>'`。

## 手順
1. `mod 194766`(FWM)で `version` / `updatedAt` / `modFiles` を読み、手元の zip の版と照合する。
2. 自分のページは `mod 194874`。Nexus の版と zip 内 README の版の一致確認に使う。
3. 失敗したら(終了コード 1)、出たメッセージをそのまま報告する。**推測で埋めない**。

## 限界(必ず守る)
- **権限(Permissions and credits)はこの API で取れない**(`Mod` 型にフィールドが無いことを確認済み)。取れなければ従来どおりブラウザかユーザー確認(CLAUDE.md「Nexus の確認」)。API で取れた値だけを事実として書き、確認日を README に書く。
- 2026-10-26 時点で、このクラウド環境から匿名で接続できた(以前の 403 は解消)。拒否された場合は回避せず報告し、ユーザーに Network access の許可を依頼する。
- 版が同じでも **ファイルが差し替わることがある**(FWM 0.5.0 は 8 時間後に差し替え)。版だけでなく `modFiles` の fileId・date・sizeInBytes・category を見る。
- できること/できないことの一覧は `docs/nexus-api-notes.md` の「2026-10-26 実測」。
- API が応答しても、スキーマ(フィールド名)は houseCARL の使用分に限る。足すときは introspection で確認し、結果を `docs/nexus-api-notes.md` に書く。
