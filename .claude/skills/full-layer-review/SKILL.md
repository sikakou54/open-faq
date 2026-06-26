---
name: full-layer-review
description: Run a change-agnostic, WHOLE-CORPUS full-layer quality review of THIS FAQ design-doc repo (要件定義 + 基本設計 + 関連設計 + 将来対応) — not a diff review. Bundles every layer, drives Google NotebookLM as the external reviewer across 7 dimensions (取り違え/整合性/逆参照/粒度/画面フォーマット適合/抜け漏れ/総合), runs deterministic link/anchor/numbering/trace + SCR-format(format_check.py) checks as the source of truth, grep-verifies every NotebookLM finding, fixes, and re-reviews until convergence. Use when asked for a 全層フルレビュー / 設計書全体のレビュー / "review the whole doc set" (not just the changes). Builds on the global design-doc-review and notebooklm-review skills.
---

# Full-layer review (whole corpus, not a diff)

Review the **entire** FAQ design-doc set through **Google NotebookLM** (the external judge) plus **deterministic checks** (the source of truth for mechanical facts). NotebookLM judges prose quality (粒度/逆参照/取り違え/抜け漏れ); scripts decide anything countable (broken links, ID gaps, trace completeness). Neither alone is enough. The reviewer NEVER substitutes its own judgment for NotebookLM's — it authors prompts, **grep-verifies every finding**, fixes, and re-reviews.

This skill is repo-tailored (bundle layers, ID series, file paths are this corpus's). It builds on **design-doc-review** (prompts + id_coverage/linkcheck) and **notebooklm-review** (`nlm` CLI: bundle → sync → ask), both vendored as local copies under `.claude/skills/` so the workflow is self-contained — read those for primitives. (The `nlm` CLI binary itself is still a prerequisite; see §0.)

> Scope rule: review by OBSERVATION (whole set), never by diff. Pre-existing issues are in scope.

## 0. Prerequisites

```bash
export PATH="$HOME/.local/bin:$PATH"     # nlm (uv tool) installs here
nlm doctor                                # Cookies present + Account ; if expired: nlm login
SK=.claude/skills/full-layer-review/scripts
DDR=.claude/skills/design-doc-review/scripts           # id_coverage.py / linkcheck.py (local copy)
NLM=.claude/skills/notebooklm-review/scripts           # nlm_bundle.py / nlm_sync.py / nlm_ask.py (local copy)
```

## 1. Deterministic checks FIRST (the source of truth)

Run these before and after every edit. They — not NotebookLM — decide mechanical facts.

```bash
python3 $SK/structure_check.py .      # broken links/anchors = 0 ; per-series gaps = [] ; same-file dup anchors = 0 (EVT/EM/EV are page-local, excluded from the global series gap check)
python3 $SK/trace_consistency.py .    # UC<->TR 1:1 ; every TBL reverse-list == matrix DB column ; orphans (TBL-011 future-reserved is the only expected one)
python3 $SK/format_check.py .         # SCR format conventions (FORMAT VIOLATIONS TOTAL = 0): §4 種類≠div(label) / no out-of-format [!NOTE]・補足 / no stray §4 bullets / EVT page-local EVT-01..N / mermaid fences well-formed / EVT refs screen-qualified (SCR-NNN EVT-MM) / no detail-design granularity (endpoint paths・physical columns・JSON keys) in SCR bodies
# general coverage per series (defined-but-untraced), via the global skill:
python3 $DDR/id_coverage.py --prefix UC  --defs '01_requirements/04_business_usecases/UC-*.md'        --refs 02_basic_design/00_traceability/index.md
# repeat --prefix for SCR/SYS/API/TBL (defs = each layer's *.md, refs = the matrix)
```
A finding from NotebookLM that contradicts these scripts is wrong — **the script wins** (grep the file to confirm). Known: NotebookLM calls populated `## 利用テーブル` pipe-tables "empty" (recurs every run) — never act on that without grep.

## 2. Bundle the whole corpus by layer

11 layers. Re-run any subset by name after edits (positional `only` args). `**` globs are recursive.

```bash
python3 $NLM/nlm_bundle.py --root . --out _nlm/bundles \
  --bundle rules='CLAUDE.md' \
  --bundle requirements='01_requirements/index.md,01_requirements/01_business_requirement/**/*.md,01_requirements/02_functional_requirement/**/*.md,01_requirements/03_non_functional_requirement/**/*.md' \
  --bundle usecases='01_requirements/04_business_usecases/**/*.md' \
  --bundle traceability='02_basic_design/00_traceability/**/*.md' \
  --bundle screens='02_basic_design/01_frontend/01_screens/*.md' \
  --bundle system='02_basic_design/02_backend/01_system/**/*.md' \
  --bundle apis='02_basic_design/02_backend/03_apis/**/*.md' \
  --bundle database='02_basic_design/02_backend/04_database/**/*.md' \
  --bundle sequences='02_basic_design/03_sequences/**/*.md' \
  --bundle crosscut='02_basic_design/index.md,02_basic_design/05_billing-design.md,02_basic_design/04_permissions/**/*.md,02_basic_design/05_errors/**/*.md,02_basic_design/06_messages/**/*.md' \
  --bundle future='03_future/**/*.md'
```
Note: `screens` uses `*.md` (top level) to exclude `mocks/*.html`. Always include `rules` (CLAUDE.md) so NotebookLM judges against the intended structure.

## 3. Sync to a FRESH notebook

```bash
python3 $NLM/nlm_sync.py --notebook fullreview --create "FAQ 全層フルレビュー $(date +%F)" \
  --bundles-dir _nlm/bundles --ids-out _nlm/source_ids.json
```
**Known bug**: `nlm_sync.py` often dies on a flaky `source list --json` parse *after* creating the notebook. Fallback — add each bundle manually and build the ids-map yourself (the notebook ID is printed on create; `nlm source add ... --wait` prints `Source ID:` reliably):
```bash
NB=<notebook-id-from-create>
for f in rules requirements usecases traceability screens system apis database sequences crosscut future; do
  out=$(nlm source add "$NB" --file "_nlm/bundles/$f.md" --wait)
  sid=$(echo "$out" | grep -oE '[a-f0-9-]{12,}' | head -1)
  python3 -c "import json,os;p='_nlm/source_ids.json';m=json.load(open(p)) if os.path.exists(p) else {};m['$f']='$sid';json.dump(m,open(p,'w'),ensure_ascii=False,indent=2)"
done
```
(`nlm chat configure --response-length longer` may return NOT_FOUND — skip it; ask for exhaustiveness in the prompt instead.)

## 4. Run the 7 dimensions (scoped per dimension)

Prompts live in `.claude/skills/design-doc-review/prompts/` (local copy). Recommended scoping (learned):

| Dimension | prompt | `--sources` |
|----|----|----|
| 相互参照取り違え | `xref_mismatch.md` | requirements,usecases,traceability,crosscut |
| 整合性 | `consistency.md` | (all) |
| 逆参照・委譲 | `reverse_reference.md` | rules,requirements,usecases |
| 構成・記載粒度 | `granularity.md` | rules,system,sequences,apis,database |
| 画面フォーマット適合 | `format_conformance.md` | rules,screens |
| 抜け漏れ | `gaps.md` | (all) — but trust §1 scripts over this |
| 総合/再レビュー | `overall.md` | (all) |

**画面フォーマット適合** judges the SCR conventions that need prose judgment (the countable ones are in §1's `format_check.py`): §1 概要 = 箇条書き; §7 = 業務的結果のみ(画面内部で管理する変数・状態や引継ぎ・処理手順を書かない一方で、**呼び出す API は記載する**); フォーマット外記述なし; リード文を勝手に増補しない; データパターンは表(画面項目/表示名/補足); 詳細設計粒度の本文転記なし。`format_check.py` で機械的に拾える違反は再掲しない。

```bash
PROMPTS=.claude/skills/design-doc-review/prompts
python3 $NLM/nlm_ask.py --notebook "$NB" --prompt-file $PROMPTS/xref_mismatch.md \
  --sources requirements,usecases,traceability,crosscut --ids-map _nlm/source_ids.json --out _nlm/results/xref
```
Highest yield on a renumbered corpus = **相互参照取り違え** (semantic ID↔title mismatch; link-checkers can't catch it). Read each `_nlm/results/<dim>_answer.md`.

## 5. Verify EVERY finding with grep before acting (this repo's NotebookLM failure modes)

For each finding: confirm the quoted text exists, check the claim's scope, classify confirmed / false-positive / needs-decision. Recurring **false positives** here:
- **"API 利用テーブルが空欄"** — pipe-table misread; the tables are populated. `grep -A6 '## 利用テーブル' <api>` to confirm.
- **BR vs RULE column confusion** — the matrix req-table has separate BR / FR / RULE columns; NotebookLM collapses them and says "BR-x should be RULE-y" when BR-x is correctly in the BR column and the RULE column is separately filled. Verify the actual row.
- **Hallucinated changelogs / IDs** — e.g. "管理者 was deprecated in v2.2" (no such changelog; 管理者 is a live role), or "NFR-905" (max is NFR-079). `grep -rn` the claimed ID/term.
- **Over-generalized requirement** — flags a missing field/guard the requirement never mandated (adding it = inventing a requirement). Check the requirement's actual scope.

**Genuinely strong** (lean on these, still verify): semantic ID↔title mismatch (取り違え), 逆参照/委譲 phrasing, UI-文言/ボタン名 in UC bodies, HTTP-code/impl-method leaking into requirements.

## 6. Fix → re-sync changed layers → re-review until convergence

- Fix confirmed, grounded findings in the docs. Don't invent specs the requirements don't support.
- Re-bundle the changed layers (positional `only` args), re-add as sources (the manual loop is fine; update `_nlm/source_ids.json` with the new IDs), re-run **overall** with a "今回の修正概要" preamble (see `overall.md`'s comment) scoped to the updated source IDs.
- After every edit re-run §1 scripts (links/anchors 0/0, no gaps, trace consistent).
- Loop until 総合 reports "指摘なし" or only design-decisions remain.

## 7. Decisions / gaps → GitHub Issues (per CLAUDE.md 課題管理)

Anything needing a stakeholder call (mechanism choice, scope, a 9-file contract change) → `gh issue create` with 概要/背景/影響/提案/確認したいこと/関連ドキュメント, plain language, a concrete proposal, and a `[design-gap]`/`[needs-review]`/`[traceability]` title prefix. Close only after docs updated, impact analyzed both directions, §1 scripts clean, and (ideally) a NotebookLM re-review.

## Final report

Per-dimension results, fix list (with grounded IDs), rejected NotebookLM findings + reasons, residual issues / Issues filed, and a final 判定 (合格 / 条件付き合格 / 要追加対応). Record `findings/`, `correspondence.md`, `STATUS.md` as in design-doc-review for an audit trail.
