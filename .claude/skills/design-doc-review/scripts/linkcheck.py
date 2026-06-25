#!/usr/bin/env python3
"""Repo-wide Markdown link/anchor validator. The source of truth for "broken links/anchors = 0/0".

NotebookLM cannot reliably verify links (it collapses tables/anchors), so run this deterministically
after every edit. Anchors are matched against explicit `id="..."` (e.g. <span id="FR-001">) targets.

Usage:
  python3 linkcheck.py --root /path/to/repo \
      --corpus 01_requirements 02_basic_design 03_future README.md \
      --exclude _build _nlm
Only links *originating from* --corpus paths are reported (so example links in the spec/rules doc
don't create noise), but targets may live anywhere under --root.
"""
import os, re, glob, argparse, sys

ap = argparse.ArgumentParser()
ap.add_argument("--root", required=True)
ap.add_argument("--corpus", nargs="*", default=[], help="path prefixes whose links are checked (default: all)")
ap.add_argument("--exclude", nargs="*", default=["_build", "_nlm"], help="dir name fragments to skip")
a = ap.parse_args()
ROOT = os.path.realpath(a.root)

def excluded(p):
    return any(f"/{x}/" in p for x in a.exclude)

allmd = [f for f in glob.glob(os.path.join(ROOT, "**/*.md"), recursive=True) if not excluded(f)]
anchors = {os.path.realpath(f): set(re.findall(r'id="([^"]+)"', open(f, encoding="utf-8").read())) for f in allmd}
corp = tuple(a.corpus) if a.corpus else ("",)
src = [f for f in allmd if os.path.relpath(f, ROOT).startswith(corp)]

lr = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
bf, ba = [], []
for f in src:
    d = os.path.dirname(f)
    for m in lr.finditer(open(f, encoding="utf-8").read()):
        t = m.group(1).strip()
        if t.startswith(("http://", "https://", "mailto:")):
            continue
        p, _, anc = t.partition("#")
        if p == "":  # same-file anchor
            if anc and anc not in anchors.get(os.path.realpath(f), set()):
                ba.append((os.path.relpath(f, ROOT), t))
            continue
        rp = os.path.realpath(os.path.join(d, p))
        if not os.path.exists(rp):
            bf.append((os.path.relpath(f, ROOT), t)); continue
        if anc and rp.endswith(".md") and anc not in anchors.get(rp, set()):
            ba.append((os.path.relpath(f, ROOT), t))

print(f"corpus source files: {len(src)} (of {len(allmd)} scanned)")
print(f"broken file links: {len(bf)}")
for x in bf[:60]: print("  FILE", x[0], "->", x[1])
print(f"broken anchor links: {len(ba)}")
for x in ba[:60]: print("  ANCH", x[0], "->", x[1])
sys.exit(1 if (bf or ba) else 0)
