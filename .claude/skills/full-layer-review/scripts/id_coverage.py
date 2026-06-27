#!/usr/bin/env python3
"""Deterministic ID-coverage / traceability-completeness check.

NotebookLM CANNOT read large traceability matrices or HTML/pipe tables (it collapses them to
<cited_table>), so it cannot judge "is every requirement traced to a UC/design?". Do that here.

Reports IDs that are DEFINED (a `## <span id="PFX-NNN">` heading or `id="PFX-NNN"` in the def files)
but never REFERENCED in the refs file(s) (e.g. the traceability matrix). Those are the trace gaps.
Inverse (referenced-but-undefined) is also reported — that catches dangling matrix entries.

Usage:
  python3 id_coverage.py --prefix FR \
      --defs '01_requirements/02_functional_requirement/*.md' \
      --refs 02_basic_design/00_traceability/index.md
"""
import re, glob, argparse

ap = argparse.ArgumentParser()
ap.add_argument("--prefix", required=True, help="ID prefix, e.g. FR / BR / UC / SCR / API / TBL")
ap.add_argument("--defs", required=True, help="glob of files that DEFINE the IDs")
ap.add_argument("--refs", nargs="+", required=True, help="file(s) where IDs should be referenced")
a = ap.parse_args()

pfx = a.prefix
defined = set()
for f in glob.glob(a.defs):
    txt = open(f, encoding="utf-8").read()
    # definition = an id="PFX-NNN" attribute (span/heading anchor)
    defined |= set(re.findall(rf'id="({pfx}-\d+)"', txt))

referenced = set()
for rf in a.refs:
    txt = open(rf, encoding="utf-8").read()
    referenced |= set(re.findall(rf'(?<![A-Za-z0-9])({pfx}-\d+)(?![0-9])', txt))

def num(x): return int(x.split("-")[1])
untraced = sorted(defined - referenced, key=num)
dangling = sorted(referenced - defined, key=num)
print(f"{pfx}: defined={len(defined)} referenced_in_refs={len(referenced)}")
print(f"  DEFINED but NOT referenced ({len(untraced)}): {' '.join(untraced)}")
print(f"  REFERENCED but NOT defined ({len(dangling)}): {' '.join(dangling)}")
