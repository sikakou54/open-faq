# `nlm` CLI cheat-sheet (NotebookLM)

`nlm` drives Google NotebookLM through a saved Chromium/Google login. Installed via `uv` at `~/.local/bin/nlm`. For full machine docs run `nlm --ai`.

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Auth / health
```bash
nlm doctor                  # installation + auth + browser status (shows account)
nlm login                   # (re)authenticate; sessions last ~20 min, auto-recovers
nlm login --check           # validate current auth only
```

## Notebooks
```bash
nlm list notebooks --json
nlm notebook create "Title"
nlm notebook rename <id|alias> "New Title"
nlm notebook delete <id> --confirm
nlm alias set <name> <id>             # memorable alias for a UUID (works anywhere an id is expected)
nlm alias list
```

## Sources (the documents NotebookLM grounds on)
```bash
nlm source add <nb> --file path.md --wait     # upload local file (MD/TXT/PDF/DOCX/CSV/...), wait until ready
nlm source add <nb> --text "..." --title T    # add raw text
nlm source add <nb> --url https://...         # add a URL/YouTube
nlm source list <nb> --json
nlm source content <source-id>                # raw extracted text
nlm source delete <source-id> --confirm
```
Limits: many sources per notebook (tens–hundreds depending on plan), ~500k words/source. Bundle a big corpus into a few `.md` files.

## Query (this is the "review" — NotebookLM answers, grounded in sources)
```bash
nlm chat configure <nb> --response-length longer       # fuller answers (set before reviews)
nlm notebook query <nb> "question" --json              # -> {answer, references[], citations, conversation_id}
nlm notebook query <nb> "q" --json --source-ids id1,id2 # scope to specific sources
nlm notebook query <nb> "follow up" --conversation-id <cid>
```
Parse the `.answer` field (prose + `[n]` citation markers); `.references[].cited_text` is the grounding evidence.

## Optional generation (Studio)
```bash
nlm report create <nb> --format "Briefing Doc" --confirm
nlm mindmap create <nb> --confirm
nlm audio create <nb> --format deep_dive --confirm
nlm studio status <nb>           # list artifacts
nlm download report <nb> --output report.md
```

## Gotchas
- NotebookLM can **misread concatenated Markdown pipe-tables** and over-generalize. Always grep the cited file to confirm a finding before acting on it.
- Concatenate files with `===== <relpath> =====` headers so answers can cite by path.
- If a command returns "Cookies have expired", run `nlm login`.
