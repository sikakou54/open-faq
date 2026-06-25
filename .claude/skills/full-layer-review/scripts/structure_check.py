#!/usr/bin/env python3
"""Deterministic structure check for the FAQ design-doc corpus (source of truth).

Reports, across 01_requirements / 02_basic_design / 03_future (+ README.md):
  - BROKEN LINKS   : a [..](path) whose target file does not exist
  - BROKEN ANCHORS : a [..](file.md#ID) whose #ID is not defined in the target
  - NUMBERING      : per ID-series range + gaps (gaps must be []) + duplicates

Definitions are `<span id="ID"></span>` anchors. Excludes _build/_nlm/templates/mocks
and the root CLAUDE.md (illustrative example links). Exit code is non-zero if any
broken link/anchor or numbering gap is found, so it can gate CI / a review loop.

Usage:  python3 structure_check.py [REPO_ROOT]
"""
import os, re, sys
from collections import defaultdict

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
SKIP = ("/_build", "/.git", "/_nlm", "/templates", "/mocks")
SKIP_FILES = ("CLAUDE.md",)  # root meta doc with illustrative (non-real) example links

mds = []
for dp, dn, fn in os.walk(ROOT):
    if any(s in dp for s in SKIP):
        continue
    for f in fn:
        if f.endswith(".md") and f not in SKIP_FILES:
            mds.append(os.path.join(dp, f))

anchor_re = re.compile(r'<span\s+id="([^"]+)"\s*>')
link_re = re.compile(r'\]\(([^)]+)\)')
series_re = re.compile(r'^([A-Z]+)-(\d+)$')

defined = defaultdict(set)   # filepath -> set of ids defined
content = {}
for m in mds:
    with open(m, encoding="utf-8") as fh:
        txt = fh.read()
    content[m] = txt
    for mt in anchor_re.finditer(txt):
        defined[m].add(mt.group(1))

broken_links, broken_anchors = [], []
for m in mds:
    base = os.path.dirname(m)
    for lm in link_re.finditer(content[m]):
        target = lm.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if target.startswith("#"):
            anc = target[1:]
            if anc and anc not in defined[m]:
                broken_anchors.append((m, target))
            continue
        path, anc = (target.split("#", 1) + [None])[:2] if "#" in target else (target, None)
        if not path:
            continue
        resolved = os.path.normpath(os.path.join(base, path))
        if not os.path.exists(resolved):
            broken_links.append((m, target))
        elif anc and resolved.endswith(".md") and anc not in defined.get(resolved, set()):
            broken_anchors.append((m, target))

# Numbering. Range/gaps use the cross-file SET of numbers per series (an ID anchored
# in both its canonical file and an index/matrix nav anchor is normal here, not a dup).
# Same-file duplicates ARE a real defect (ambiguous anchor) -> detect those per file.
nums = defaultdict(set)
samefile_dups = []  # (series, num, file)
for m in mds:
    seen = set()
    for mt in anchor_re.finditer(content[m]):
        sm = series_re.match(mt.group(1))
        if sm:
            s, n = sm.group(1), int(sm.group(2))
            nums[s].add(n)
            if mt.group(1) in seen:
                samefile_dups.append((s, n, m))
            seen.add(mt.group(1))

print(f"=== BROKEN LINKS (target file missing) === {len(broken_links)}")
for m, t in broken_links:
    print(f"  {os.path.relpath(m, ROOT)} -> {t}")
print(f"=== BROKEN ANCHORS (id missing in target) === {len(broken_anchors)}")
for m, t in broken_anchors:
    print(f"  {os.path.relpath(m, ROOT)} -> {t}")

has_gap = False
print("=== NUMBERING (range / gaps) ===")
for s in sorted(nums):
    uniq = sorted(nums[s])
    gaps = sorted(set(range(1, max(uniq) + 1)) - set(uniq))
    flag = "  <-- GAP" if gaps else ""
    if gaps:
        has_gap = True
    print(f"  {s}: {min(uniq)}..{max(uniq)} count={len(uniq)} gaps={gaps}{flag}")

print(f"=== SAME-FILE DUPLICATE ANCHORS === {len(samefile_dups)}")
for s, n, m in samefile_dups:
    print(f"  {s}-{n:03d} defined twice in {os.path.relpath(m, ROOT)}")

sys.exit(1 if (broken_links or broken_anchors or has_gap or samefile_dups) else 0)
