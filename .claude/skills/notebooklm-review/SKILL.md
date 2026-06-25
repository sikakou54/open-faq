---
name: notebooklm-review
description: Drive Google NotebookLM via the local `nlm` CLI to have NotebookLM review, analyze, or answer questions over a corpus of LOCAL documents (Markdown, code docs, specs, PDFs). Use when the user wants an external NotebookLM review of their docs/design, wants to "ask NotebookLM" about a local document set, or wants to route document QA/grounded review through NotebookLM rather than reviewing inline. Bundles many files into a few NotebookLM sources, uploads them to a notebook, runs review prompts, and parses the grounded answers. Triggers: "use NotebookLM", "NotebookLM CLI", "review my docs with NotebookLM", "ask NotebookLM about ...".
---

# NotebookLM review (via `nlm` CLI)

Route document review / QA to **Google NotebookLM** through the local `nlm` CLI. NotebookLM is the judge; this skill only prepares inputs (bundles + prompts) and parses outputs. The model itself does NOT substitute its own review — it asks NotebookLM and organizes the grounded results.

## Prerequisites (check once)

```bash
export PATH="$HOME/.local/bin:$PATH"     # nlm installs here (uv tool)
nlm --version            # confirm installed
nlm doctor               # confirm Authentication: Cookies present + Account
nlm list notebooks --json
```
- Sessions last ~20 min with auto-recovery. If a command says "Cookies have expired", run `nlm login`.
- Full machine-readable CLI docs: `nlm --ai`. Quick cheat-sheet: [reference.md](reference.md).

## Core workflow

1. **Bundle** local files into a few sources (NotebookLM caps source count; bundling keeps cross-file review possible and preserves per-file provenance via `===== <path> =====` separators):
   ```bash
   python3 scripts/nlm_bundle.py --config bundles.json
   # or inline: python3 scripts/nlm_bundle.py --root . --out _nlm/bundles \
   #   --bundle rules=GUIDE.md --bundle src='src/**/*.md'
   ```
2. **Sync** bundles into a notebook as file sources (creates/reuses the notebook, writes a name→source-id map). Re-run with `--replace` after editing files to swap only changed bundles:
   ```bash
   python3 scripts/nlm_sync.py --notebook myreview --create "My Review" \
     --bundles-dir _nlm/bundles --ids-out _nlm/source_ids.json
   ```
3. **Ask** NotebookLM a review/QA prompt, optionally scoped to specific bundles, and parse the grounded answer:
   ```bash
   python3 scripts/nlm_ask.py --notebook myreview --prompt-file _nlm/q1.md \
     --sources rules,src --ids-map _nlm/source_ids.json --out _nlm/results/q1
   ```
   Output: `_nlm/results/q1.json` (raw) + `_nlm/results/q1_answer.md` (`answer` text + cited evidence).

## Writing good review prompts

- Tell NotebookLM to answer **only from the provided sources**, cite the **relative path** from the `===== <path> =====` separators, and **not to speculate** ("実在する ID・記述を根拠に挙げ、無ければ『指摘なし』").
- Ask for a fixed **table format** so results parse cleanly.
- Split a big review into **focused queries** (one concern each, scoped with `--sources`); retrieval-grounded answers are more thorough and less likely to hallucinate than one mega-prompt.
- `nlm chat configure <notebook> --response-length longer` before reviews for fuller answers.

## CRITICAL: verify groundedness before acting

NotebookLM can **misread concatenated Markdown tables** and occasionally **over-generalize** (e.g. flag a gap that the requirements don't actually mandate). Before treating any finding as actionable:
- grep the cited file/line to confirm the quoted text actually exists;
- check the claim's scope against the source of truth (don't "fix" something into existence).
Record each finding as confirmed / false-positive / needs-decision with a reason. This verification is the model's job; the *review judgment* still comes from NotebookLM.

## Iterate (re-review loop)

After applying fixes: re-bundle only the changed bundles, `nlm_sync.py --replace`, then re-ask a focused "is X resolved + any new issues?" prompt. Repeat until NotebookLM reports resolved / only design-decision items remain.

## Notes
- Supported source file types include MD, TXT, PDF, DOCX, CSV (and audio/image). Bundling to `.md` is simplest for text corpora.
- Generation extras (audio overview, mind map, report, quiz) are available via `nlm audio|report|mindmap|... create <notebook> --confirm` if the user wants them.
- Clean up with `nlm source delete <id> --confirm` / `nlm notebook delete <id> --confirm`.
