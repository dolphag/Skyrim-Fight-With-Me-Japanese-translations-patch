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
- **権限(Permissions and credits)がこの API で取れるかは未確認**。取れなければ従来どおりブラウザかユーザー確認(CLAUDE.md「Nexus の確認」)。API で取れた値だけを事実として書き、確認日を README に書く。
- このクラウド環境は `api.nexusmods.com` への CONNECT がプロキシに 403 で拒否される(2026-10-26)。使うには、ユーザーが環境の Network access で許可ドメインに追加する必要がある。拒否されたら回避せず報告する。
- API が応答しても、スキーマ(フィールド名)は houseCARL の使用分に限る。足すときは introspection で確認し、結果を `docs/nexus-api-notes.md` に書く。
