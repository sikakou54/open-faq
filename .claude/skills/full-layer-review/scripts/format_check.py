#!/usr/bin/env python3
"""Deterministic FORMAT-CONFORMANCE check for the FAQ design-doc corpus.

Enforces the template/CLAUDE.md formatting conventions that prose review cannot
count reliably. The source of truth for "does the doc obey the format". Run
alongside structure_check.py / trace_consistency.py.

Checks (each prints a count; non-zero total -> exit 1 so it can gate a review loop):

  [SCR-TYPE]   §4 画面項目 "種類" must not be `div` (display-only text = `label`).
  [SCR-NOTE]   No out-of-format `> [!NOTE]` / `**補足**` blocks in a SCR (everything
               lives inside the 8 fixed sections).
  [SCR-BULLET] No stray bullet list directly under the §4 画面項目 table (value
               patterns belong in the データパターン table, not inline bullets).
  [MERMAID]    Code-fence lines (```), opening/closing, must be alone on their line
               (trailing content breaks rendering). Whole corpus.
  [EVT-LOCAL]  In each SCR, EVT ids must be page-local EVT-01..N (2-digit, no gaps,
               no dups, no legacy 3-digit EVT-NNN).
  [EVT-REF]    Outside the screens layer, an EVT reference must be screen-qualified
               (`SCR-NNN EVT-MM`); a bare `EVT-MM` is flagged.

Usage:  python3 format_check.py [REPO_ROOT]
"""
import os, re, sys, glob

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
SCR_DIR = os.path.join(ROOT, "02_basic_design/01_frontend/01_screens")
# layers that reference EVT and must screen-qualify them
REF_GLOBS = [
    "02_basic_design/02_backend/03_apis/*.md",
    "02_basic_design/02_backend/01_system/*.md",
    "02_basic_design/03_sequences/*.md",
    "02_basic_design/04_permissions/*.md",
    "02_basic_design/05_errors/*.md",
    "02_basic_design/06_messages/*.md",
]
ALL_GLOBS = ["01_requirements/**/*.md", "02_basic_design/**/*.md", "03_future/**/*.md"]


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def rel(p):
    return os.path.relpath(p, ROOT)


def section_span(txt, start_head, end_heads):
    """Return substring from the start_head line to the next of end_heads (or EOF)."""
    lines = txt.splitlines()
    s = None
    for i, l in enumerate(lines):
        if start_head in l:
            s = i
            break
    if s is None:
        return ""
    e = len(lines)
    for j in range(s + 1, len(lines)):
        if any(h in lines[j] for h in end_heads):
            e = j
            break
    return "\n".join(lines[s:e])


scr_files = sorted(glob.glob(os.path.join(SCR_DIR, "*.md")))

scr_type, scr_note, scr_bullet, evt_local, mermaid, evt_ref, scr_grain, scr_apiid, sys_fmt = [], [], [], [], [], [], [], [], []
apiid_re = re.compile(r'<a href="[^"]*API-(\d+)\.md#API-\1">([^<]*)</a>')

fence_re = re.compile(r"^\s*```(.*)$")
row_type_re = re.compile(r"^\|[^|]*\|[^|]*\|\s*([^|]+?)\s*\|")  # 3rd cell = 種類
# detail-design granularity that must not appear in basic-design SCR bodies
GRAIN_PATTERNS = [
    re.compile(r"(GET|POST|PATCH|DELETE|PUT)\s+/[a-z]"),   # endpoint path literal
    re.compile(r"owner_user_id|\bvalid=[01]\b|users\.valid|\bproject_id\b"),  # physical columns
    re.compile(r"`[a-z]+[A-Z][a-zA-Z]*`"),                 # camelCase key in code span
    re.compile(r"pk_live_"),                                # key format literal
]

for f in scr_files:
    txt = read(f)
    # [SCR-NOTE]
    for i, l in enumerate(txt.splitlines(), 1):
        if "[!NOTE]" in l or "**補足**" in l or "**補足:" in l:
            scr_note.append(f"{rel(f)}:{i}")
    # §4 section
    sec4 = section_span(txt, "## ", [])  # placeholder; recompute properly below
    sec4 = section_span(txt, "4. 画面項目", ["5. バリデーション", "## 5", "## <span id=\"5"])
    if sec4:
        # [SCR-TYPE]  種類 == div  (markdown pipe rows only)
        for l in sec4.splitlines():
            if l.strip().startswith("|") and l.count("|") >= 7:
                m = row_type_re.match(l)
                if m and m.group(1).strip() == "div":
                    scr_type.append(rel(f))
                    break
        # [SCR-BULLET]  bullet line(s) inside §4 that are NOT inside a table
        for l in sec4.splitlines():
            s = l.lstrip()
            if s.startswith("- ") or s.startswith("* "):
                scr_bullet.append(rel(f))
                break
    # [SCR-APIID] API hyperlinks must show the API-ID in the link text (e.g. ログイン(API-002))
    for i, l in enumerate(txt.splitlines(), 1):
        for m in apiid_re.finditer(l):
            if f"API-{m.group(1)}" not in m.group(2):
                scr_apiid.append(f"{rel(f)}:{i}  {m.group(0)[:60]}")
    # [SCR-GRAIN] detail-design granularity in the SCR body
    for i, l in enumerate(txt.splitlines(), 1):
        for p in GRAIN_PATTERNS:
            m = p.search(l)
            if m:
                scr_grain.append(f"{rel(f)}:{i}  ...{m.group(0)}")
                break
    # [EVT-LOCAL]
    evts = re.findall(r'<span id="(EVT-\d+)">', txt)
    if evts:
        nums = []
        bad = False
        for e in evts:
            d = e.split("-")[1]
            if len(d) != 2:        # legacy 3-digit global id
                bad = True
            nums.append(int(d))
        if len(nums) != len(set(nums)):
            bad = True
        if sorted(nums) != list(range(1, len(nums) + 1)):
            bad = True
        if bad:
            evt_local.append(f"{rel(f)}  ids={evts}")

# [SYS-FMT] SYS files must not have a '## 詳細設計への移管候補' section (フォーマット外)
SYS_DIR = os.path.join(ROOT, "02_basic_design/02_backend/01_system")
for f in glob.glob(os.path.join(SYS_DIR, "SYS-*.md")):
    if "## 詳細設計への移管候補" in read(f):
        sys_fmt.append(rel(f))

# [MERMAID] whole corpus: a fence line with trailing content
seen = set()
for g in ALL_GLOBS:
    for f in glob.glob(os.path.join(ROOT, g), recursive=True):
        if any(s in f for s in ("/_nlm", "/_build", "/mocks")) or f in seen:
            continue
        seen.add(f)
        for i, l in enumerate(read(f).splitlines(), 1):
            m = fence_re.match(l)
            if m:
                rest = m.group(1).strip()
                # allowed: bare ``` (close) or ```<lang> (open). lang = letters only.
                if rest and not re.fullmatch(r"[a-zA-Z]+", rest):
                    mermaid.append(f"{rel(f)}:{i}  {l.strip()[:70]}")

# [EVT-REF] non-screens layers must screen-qualify EVT
ref_re = re.compile(r"(.{0,18})EVT-\d+")
for g in REF_GLOBS:
    for f in glob.glob(os.path.join(ROOT, g)):
        for i, l in enumerate(read(f).splitlines(), 1):
            for m in ref_re.finditer(l):
                pre = m.group(1)
                if not re.search(r"SCR-\d+\s*$", pre):
                    evt_ref.append(f"{rel(f)}:{i}  ...{m.group(0)[-30:]}")

groups = [
    ("[SCR-TYPE]  §4 種類=div (should be label)", scr_type),
    ("[SCR-NOTE]  out-of-format [!NOTE]/補足 in SCR", scr_note),
    ("[SCR-BULLET] stray bullets under §4 画面項目", scr_bullet),
    ("[EVT-LOCAL] non page-local EVT ids in SCR", evt_local),
    ("[MERMAID]   malformed code fence (breaks render)", mermaid),
    ("[EVT-REF]   bare EVT ref (need SCR-NNN EVT-MM)", evt_ref),
    ("[SCR-GRAIN] detail-design granularity in SCR body", scr_grain),
    ("[SCR-APIID] API link missing API-ID in text (業務名(API-NNN))", scr_apiid),
    ("[SYS-FMT]  out-of-format ## 詳細設計への移管候補 in SYS", sys_fmt),
]
total = 0
for title, items in groups:
    print(f"=== {title} === {len(items)}")
    for it in items[:40]:
        print(f"  {it}")
    if len(items) > 40:
        print(f"  ... (+{len(items) - 40} more)")
    total += len(items)

print(f"=== FORMAT VIOLATIONS TOTAL === {total}")
sys.exit(1 if total else 0)
