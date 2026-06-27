#!/bin/bash
# Claude Code PostToolUse hook.
# Receives the tool call JSON via stdin; runs sync.sh when git commit was executed.
input=$(cat)

cmd=$(echo "$input" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', d).get('command', ''))
except Exception:
    pass
" 2>/dev/null || true)

if echo "$cmd" | grep -qE 'git[[:space:]].*commit'; then
  THIS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  LOG="/tmp/nlm-sync.log"
  bash "$THIS/sync.sh" >> "$LOG" 2>&1 &
  echo "[nlm-sync] sync started in background (log: $LOG)"
fi
