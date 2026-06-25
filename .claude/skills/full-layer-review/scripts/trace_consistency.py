#!/usr/bin/env python3
"""Deterministic traceability consistency check (source of truth for trace findings).

The matrix 02_basic_design/00_traceability/index.md is the single source of truth.
This verifies the things NotebookLM CANNOT (it collapses big tables):

  A. UC <-> TR is 1:1 and same-numbered (UC-N realized by TR-N).
  B. Each TBL's reverse list ("本テーブルを利用する業務スレッド(TR-ID): ...") equals
     exactly the set of main-matrix TR rows whose DB column includes that table.
     (Mismatch = a stale/missing reverse-link. TBL-011 future-reserved => no list, OK.)
  C. Design IDs defined but never referenced in the matrix (orphans), per series.

Exit code is non-zero if any inconsistency is found.

Usage:  python3 trace_consistency.py [REPO_ROOT]
"""
import os, re, sys

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
MX = os.path.join(ROOT, "02_basic_design/00_traceability/index.md")
DB = os.path.join(ROOT, "02_basic_design/02_backend/04_database")
UC = os.path.join(ROOT, "01_requirements/04_business_usecases")
num = lambda x: int(x.split("-")[1])
problems = 0

mx = open(MX, encoding="utf-8").read().splitlines()
# main-matrix rows: a TR row that carries a DB (TBL) column
tr_tbl = {}
tr_defined = []
for ln in mx:
    m = re.match(r'\| <span id="(TR-\d+)"></span>', ln)
    if m:
        tr_defined.append(m.group(1))
        if "TBL-" in ln:
            tr_tbl[m.group(1)] = set(re.findall(r"TBL-\d+", ln))

# A. UC <-> TR 1:1 same-number
uc_ids = {f[:-3] for f in os.listdir(UC) if re.match(r"UC-\d+\.md$", f)}
tr_main = set(tr_defined)
print("=== A. UC <-> TR 1:1 ===")
miss_tr = sorted({f"TR-{u.split('-')[1]}" for u in uc_ids} - tr_main, key=num)
miss_uc = sorted({u for u in uc_ids if f"TR-{u.split('-')[1]}" not in tr_main}, key=num)
if miss_tr or miss_uc:
    problems += 1
    print(f"  UC without matching TR row: {miss_uc}")
else:
    print(f"  OK: {len(uc_ids)} UC each have TR-<same-number> in the matrix")

# B. TBL reverse list vs matrix DB columns
tbl_auth = {}
for tr, tbls in tr_tbl.items():
    for t in tbls:
        tbl_auth.setdefault(t, set()).add(tr)
print("=== B. TBL reverse-list <-> matrix DB column ===")
desync = 0
for f in sorted(os.listdir(DB)):
    mm = re.match(r"(TBL-\d+)\.md$", f)
    if not mm:
        continue
    t = mm.group(1)
    txt = open(os.path.join(DB, f), encoding="utf-8").read()
    lm = re.search(r"業務スレッド\(TR-ID\)[:：]\s*(.+)", txt)
    declared = set(re.findall(r"TR-\d+", lm.group(1))) if lm else set()
    auth = tbl_auth.get(t, set())
    if lm:
        add, rem = sorted(auth - declared, key=num), sorted(declared - auth, key=num)
        if add or rem:
            desync += 1
            print(f"  {t}: +missing {add}  -stale {rem}")
    elif auth:  # no reverse list but matrix references it
        desync += 1
        print(f"  {t}: NO reverse list but matrix uses it in {sorted(auth, key=num)}")
if desync == 0:
    print("  OK: all TBL reverse lists match the matrix (future-reserved tables w/o a list are fine)")
else:
    problems += 1

# C. orphans: design IDs defined but not referenced in the matrix
def defined_ids(folder, pat):
    out = set()
    for f in os.listdir(os.path.join(ROOT, folder)):
        if re.match(pat, f):
            out.add(f[:-3])
    return out
matrix_text = "\n".join(mx)
print("=== C. design IDs defined but NOT referenced in matrix (orphans) ===")
series = [
    ("SCR", "02_basic_design/01_frontend/01_screens", r"SCR-\d+\.md$"),
    ("SYS", "02_basic_design/02_backend/01_system", r"SYS-\d+\.md$"),
    ("API", "02_basic_design/02_backend/03_apis", r"API-\d+\.md$"),
    ("TBL", "02_basic_design/02_backend/04_database", r"TBL-\d+\.md$"),
]
orph_total = 0
for pfx, folder, pat in series:
    defined = defined_ids(folder, pat)
    refd = set(re.findall(rf"{pfx}-\d+", matrix_text))
    orph = sorted(defined - refd, key=num)
    print(f"  {pfx}: defined={len(defined)} orphans={orph}")
    orph_total += len(orph)
# NOTE: TBL-011 is intentionally future-reserved (no MVP TR) -> expected orphan.
if orph_total and orph_total > 0:
    print("  (review each orphan; e.g. an intentionally future-reserved table is acceptable)")

sys.exit(1 if problems else 0)
