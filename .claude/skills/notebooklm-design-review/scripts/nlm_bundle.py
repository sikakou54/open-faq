#!/usr/bin/env python3
"""Concatenate local files into NotebookLM source bundles (idempotent).

NotebookLM caps how many sources a notebook holds, so a large corpus is bundled
into a few files. Each source file gets a `===== <relpath> =====` header before
its content so NotebookLM can cite findings by relative path.

Usage
-----
  # from a JSON config:
  python3 nlm_bundle.py --config bundles.json [keyA keyB ...]

  # inline (repeatable --bundle key=glob[,glob...]):
  python3 nlm_bundle.py --root . --out _nlm/bundles \
      --bundle rules=CONTRIBUTING.md --bundle docs='docs/**/*.md'

config.json
-----------
  {
    "root": ".",                 # base dir for globs (default ".")
    "out": "_nlm/bundles",       # output dir (default "_nlm/bundles")
    "bundles": {
      "rules":    ["CONTRIBUTING.md"],
      "docs":     ["docs/**/*.md"],
      "api":      ["openapi/**/*.yaml", "api/**/*.md"]
    }
  }

Positional args (bundle keys) limit which bundles are (re)generated — useful for
re-bundling only what changed before a re-review.
"""
import os, re, sys, glob, json, argparse


def natkey(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p)]


def expand(root, patterns):
    seen, files = set(), []
    for pat in patterns:
        for f in sorted(glob.glob(os.path.join(root, pat), recursive=True), key=natkey):
            rel = os.path.relpath(f, root)
            if os.path.isfile(f) and rel not in seen:
                seen.add(rel)
                files.append((rel, f))
    return files


def build(root, out, key, patterns):
    files = expand(root, patterns)
    parts = [f"# NotebookLM source bundle: {key} ({len(files)} files)\n",
             "# Files are separated by `===== <relative path> =====`.\n",
             "# When reporting findings, cite the relative path of the file.\n"]
    for rel, full in files:
        with open(full, encoding="utf-8", errors="replace") as fh:
            parts.append(f"\n\n===== {rel} =====\n\n{fh.read()}")
    text = "".join(parts)
    os.makedirs(out, exist_ok=True)
    outp = os.path.join(out, f"{key}.md")
    with open(outp, "w", encoding="utf-8") as fh:
        fh.write(text)
    b = len(text.encode())
    print(f"{key:18s} files={len(files):4d} bytes={b:>9,} (~{b/1024:.0f}KB) ~words={b//6:,} -> {outp}")
    if b // 6 > 480_000:
        print(f"  WARNING: {key} ~{b//6:,} words approaches NotebookLM's ~500k words/source limit; split it.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="_nlm/bundles")
    ap.add_argument("--bundle", action="append", default=[], help="key=glob[,glob...]")
    ap.add_argument("only", nargs="*", help="optional subset of bundle keys to (re)build")
    a = ap.parse_args()

    if a.config:
        cfg = json.load(open(a.config, encoding="utf-8"))
        root = cfg.get("root", a.root)
        out = cfg.get("out", a.out)
        bundles = cfg["bundles"]
    else:
        root, out, bundles = a.root, a.out, {}
        for spec in a.bundle:
            k, _, v = spec.partition("=")
            bundles[k.strip()] = [g.strip() for g in v.split(",") if g.strip()]
    if not bundles:
        sys.exit("no bundles defined (use --config or --bundle key=glob)")

    keys = a.only or list(bundles)
    for k in keys:
        if k not in bundles:
            sys.exit(f"unknown bundle key: {k} (valid: {', '.join(bundles)})")
        build(root, out, k, bundles[k])


if __name__ == "__main__":
    main()
