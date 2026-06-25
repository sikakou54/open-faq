---
name: design-doc-review
description: Run a full multi-layer quality review of a requirements/design document set (要件定義 + 基本設計 + 関連設計) using Google NotebookLM as the external reviewer, then organize findings, verify them, fix the docs, and re-review until convergence. Use when the user wants a comprehensive design-document review/audit, a "全層フルレビュー", a 逆参照/粒度/抜け漏れ/整合性 review, or to drive design QA through NotebookLM across many files. NotebookLM is the review judge; this skill orchestrates bundling, phased review prompts, groundedness verification, fixes, and the re-review loop. Builds on the notebooklm-review skill for the `nlm` CLI primitives.
---

# Full design-doc review via NotebookLM

Drive a complete, multi-dimension quality review of a requirements + basic-design corpus through **Google NotebookLM** (the review judge), then verify, fix, and re-review until convergence. The orchestrator/agents NEVER substitute their own review — they author NotebookLM prompts, organize results, **verify groundedness**, decide fixes, edit docs, and re-review.

This skill uses the [notebooklm-review](../notebooklm-review/SKILL.md) skill's `nlm` primitives (bundle → sync → ask). Read that first for setup (`nlm doctor`, auth).

## The review dimensions (phases)

Run these as focused NotebookLM queries (scoped with `--sources`). Prompt templates are in [prompts/](prompts/):
1. **逆参照** ([reverse_reference.md](prompts/reverse_reference.md)) — does the requirements layer reference/delegate to downstream (basic design / 画面ID / API / TBL / "…を正本とする" 委譲文)? Trace must be 要件→基本設計.
2. **構成・粒度** ([granularity.md](prompts/granularity.md)) — requirements vs basic-design responsibility split; impl-level leakage (SQL / method names / physical columns / formulas) in basic design.
3. **抜け漏れ** ([gaps.md](prompts/gaps.md)) — 要件→基本設計 coverage (画面/API/TBL/権限/エラー/メッセージ/SYS/バッチ/外部連携), 異常系/非機能.
4. **整合性** ([consistency.md](prompts/consistency.md)) — 用語/ID/ステータス/ロール/エラーコード unification, legacy IDs, 重複/矛盾, cross-layer I/O.
5. **相互参照取り違え** ([xref_mismatch.md](prompts/xref_mismatch.md)) — references that point to a **real but wrong** ID (e.g. `(FR-073)` where FR-073's actual title is unrelated). NotebookLM is genuinely *good* at this semantic ID↔title matching, and link-checkers CANNOT catch it (the target resolves). This is the highest-yield NotebookLM dimension on a corpus that has been renumbered — ask it to enumerate ALL mismatches in one pass, then verify each against the real `## ID: title` heading.
6. **総合/再レビュー** ([overall.md](prompts/overall.md)) — integrated final sweep; also used to re-review after fixes ("is X resolved + any new issues?").

Tailor each prompt: tell NotebookLM to answer **only from sources**, cite the **relative path** (from the `===== <path> =====` bundle separators), **not speculate**, ground every finding in a **real ID**, and output a **fixed table format** so results parse. Run `nlm chat configure <nb> --response-length longer` first.

## Deterministic checks are the source of truth for mechanical facts (run alongside NotebookLM)

NotebookLM judges *prose quality* (粒度/逆参照/抜け漏れ/取り違え). It **cannot** verify mechanical structure — it collapses large traceability matrices and HTML/pipe tables to `<cited_table>`, so it will hallucinate "this table is empty" / "this requirement is untraced". For anything countable, the orchestrator runs scripts and treats THOSE as authoritative:
- **Trace completeness** — [scripts/id_coverage.py](scripts/id_coverage.py): which `PFX-NNN` are defined but never referenced in the traceability matrix (and the inverse). This — not NotebookLM — answers "is every requirement/UC traced to a design?". Run per series (FR/BR/UC/SCR/API/TBL/SYS/SEQ).
- **Broken links/anchors** — [scripts/linkcheck.py](scripts/linkcheck.py): must be 0/0 after every edit. Note it canNOT catch wrong-but-existing references (the link resolves); that semantic class is the 相互参照取り違え phase above.
- **Numbering gaps / orphans** — grep the `id="PFX-NNN"` set for gaps; cross-check design files against the matrix for orphans.

Workflow: deterministic checks find the *structural* defects (gaps, orphans, broken links), NotebookLM finds the *semantic* defects (wrong altitude, delegation, wrong-meaning citations). Neither alone is sufficient. When NotebookLM and a script disagree on a mechanical fact (e.g. "table empty"), the **script wins** — grep the file to confirm.

## Process (per phase, then loop)

1. **Bundle** the corpus by layer (rules + each design layer) and **sync** to a notebook — see notebooklm-review. Always include the rules/spec doc (e.g. CONTRIBUTING/CLAUDE.md) as a `rules` source so NotebookLM judges against the intended structure. Bundle by layer so you can scope and re-sync each independently (e.g. `requirements`, `usecases`, `traceability`, `screens`, `apis`, `database`, `system`, `sequences`, `crosscut`). If `nlm_sync.py` errors mid-run (the `source list --json` parse is occasionally flaky), fall back to a manual loop: `nlm source add <nb> --file <bundle> --wait` per bundle (it prints `Source ID:` reliably) and record the IDs into the ids-map yourself. Re-sync a changed layer by `nlm source delete <old> --confirm` then re-adding.
2. **Ask** each dimension's prompt, scoped to relevant sources. Save raw + answer.
3. **VERIFY every finding before acting** (see below). Classify each: confirmed / false-positive / needs-decision, each with a reason.
4. **Decide & fix** the confirmed, grounded ones in the docs. Don't invent specs the requirements don't support; mark unsupported "gaps" as 要確認/design-decision.
5. **Re-bundle changed layers, re-sync (`--replace`), re-ask** a focused "is it resolved + new issues?" prompt. Loop until NotebookLM reports resolved / only design-decisions remain.
6. **Validate** the docs after every edit (broken links/anchors = 0, no ID gaps) and regenerate any nav/index.

## CRITICAL: NotebookLM hallucinates — verify before you act

NotebookLM is grounded but **not reliable on mechanical detail**. Observed failure modes (verify against the real files every time):
- **Misreads concatenated Markdown pipe-tables** — it repeatedly claimed "API utilization-table cells are empty" when the tables were fully populated (this recurred 5×). Always `grep` the cited file before "fixing".
- **Over-generalizes a requirement** — e.g. flags a missing optimistic-lock/version column as a gap when the requirement only mandates it for one entity. Adding it would be **inventing a requirement**. Check the requirement's actual scope.
- **Mis-attributes** — cites the wrong ID for a real concern (right problem, wrong location), or claims a field is missing when it's present.

For each finding: confirm the quoted text exists, check the claim's scope against the source of truth, then act. This verification is the orchestrator's job; the *review judgment* still originates from NotebookLM. Record confirmed / false-positive / needs-decision with reasons — never silently drop a NotebookLM finding, and never blindly apply one.

**What NotebookLM is genuinely good at** (lean on these): wrong-altitude/粒度 prose, 逆参照/委譲 phrasing, and **semantic ID↔title mismatch** (the 相互参照取り違え phase) — citing `(FR-073)` where FR-073's real subject is unrelated. On a renumbered corpus this surfaced ~11 real wrong-but-existing references that link-checkers passed clean; NotebookLM's title-based attribution was reliable there. Still verify each against the real heading, because NotebookLM occasionally mislabels an ID's own title.

## Track everything

- `findings/phaseN_findings.md` — NotebookLM's raw verdict organized into the dimension's table + your verification result + 対応要否.
- `correspondence.md` — cross-phase master: each finding → fix → status (対応済み / 一部対応 / 対応不要 / 要確認), with reasons for rejections.
- `STATUS.md` — phase progress + final判定 (合格 / 条件付き合格 / 要追加対応).
- A final report: review-count, per-phase results, fix list, 逆参照 check, residual issues, final判定.

## Scale knobs
- For a big corpus or a generative fix (e.g. authoring many new design files, or mapping many untraced requirements to UCs), fan out parallel agents — **one per category/subsystem**, each reading its requirement files + the UCs + the matrix and returning a strict machine-readable mapping (`REQ-ID | MAP/CROSSCUT/GAP | UC-IDs | reason`). Then the orchestrator applies the mapping centrally with a script and validates. Classify honestly: MAP (a specific UC realizes it), CROSSCUT (a cross-cutting quality attribute with no single owning UC — do NOT force it into the matrix; annotate instead), GAP (no design exists — route to an Issue/decision). Run agents in the background so contained fixes proceed in parallel.
- Re-review only the changed layers between loops (re-bundle + `nlm source` replace those bundles) to keep it fast.
- **Deletions require renumbering** (no gaps): build the full old→new map for the series, replace via a placeholder pass (`PFX-NNN` → token → new number) to avoid collisions, then run linkcheck + id_coverage to confirm 0 gaps / 0 broken refs.

## Decisions & gaps → GitHub Issues
GAP findings and anything needing a stakeholder call (scope, priority, design choice) become GitHub Issues, not silent edits. Write each with 概要/背景/影響/提案/確認したいこと/関連ドキュメント in plain language and a concrete proposal. Drive the docs from the user's answers, then close the Issue only after docs are updated, impact analyzed both directions, links/anchors are 0/0, and NotebookLM re-review is clean.
