---
name: sync-docs-to-notebooklm
description: Bundle all design-doc Markdown files and replace sources in a NotebookLM notebook. Config-driven (notebook ID and bundle globs come from .claude/nlm-sync.json). Reusable for any notebook — just point --config at a different JSON file or pass --notebook to override.
---

# NotebookLM ドキュメント同期

## 手動実行

```bash
# 通常同期 (.claude/nlm-sync.json を使用)
bash .claude/skills/sync-docs-to-notebooklm/scripts/sync.sh

# バンドル確認のみ(アップロードしない)
bash .claude/skills/sync-docs-to-notebooklm/scripts/sync.sh --dry-run

# 別ノートブックへ同期
bash .claude/skills/sync-docs-to-notebooklm/scripts/sync.sh --notebook OTHER-ID

# 別設定ファイルを使用
bash .claude/skills/sync-docs-to-notebooklm/scripts/sync.sh --config path/to/nlm-sync.json
```

## 自動実行

`.claude/settings.local.json` の `PostToolUse(Bash)` フックに登録済み。
`git commit` を含む Bash コマンド完了後に自動でバックグラウンド実行する。
ログ: `/tmp/nlm-sync.log`

## 設定ファイル (.claude/nlm-sync.json)

```json
{
  "notebook": "UUID-OR-ALIAS",
  "bundles": {
    "bundle_name": ["glob1", "glob2"]
  }
}
```

## 依存スキル

`full-layer-review` スキルの `scripts/nlm_bundle.py` と `scripts/nlm_sync.py` を再利用する。
