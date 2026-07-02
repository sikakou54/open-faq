#!/usr/bin/env python3
"""Upload individual image files to a NotebookLM notebook as sources.

Each matched file is uploaded as a separate source.  On --replace, existing
sources whose title matches a file basename are deleted first.

Usage
-----
  python3 nlm_sync_images.py \\
      --notebook NOTEBOOK_ID \\
      --root /path/to/repo \\
      --globs "02_basic_design/**/*.png" \\
      --ids-out _build/nlm_sync/image_source_ids.json \\
      [--replace]
"""
import os, sys, json, glob as glob_mod, subprocess, argparse

ENV = dict(os.environ)
ENV["PATH"] = os.path.expanduser("~/.local/bin") + ":" + ENV.get("PATH", "")


def run(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, env=ENV, timeout=600, **kw)


def list_sources(nb):
    r = run(["nlm", "source", "list", nb, "--json"])
    try:
        return json.loads(r.stdout or "[]")
    except json.JSONDecodeError:
        return []


def main():
    ap = argparse.ArgumentParser(description="Sync image files to NotebookLM")
    ap.add_argument("--notebook", required=True, help="notebook ID or alias")
    ap.add_argument("--root", default=".", help="repo root (glob base)")
    ap.add_argument("--globs", required=True, help="comma-separated glob patterns relative to --root")
    ap.add_argument("--ids-out", default="_build/nlm_sync/image_source_ids.json")
    ap.add_argument("--replace", action="store_true", help="delete existing sources by title before re-adding")
    a = ap.parse_args()

    patterns = [p.strip() for p in a.globs.split(",")]
    files = []
    for pattern in patterns:
        matched = sorted(glob_mod.glob(os.path.join(a.root, pattern), recursive=True))
        files.extend(matched)
    files = sorted(set(files))

    if not files:
        print(f"[nlm-images] no files matched: {a.globs}")
        return

    print(f"[nlm-images] {len(files)} image file(s) to sync")

    ids = {}
    if os.path.exists(a.ids_out):
        try:
            ids = json.load(open(a.ids_out))
        except Exception:
            ids = {}

    existing = {}
    if a.replace:
        existing = {s.get("title"): s.get("id") for s in list_sources(a.notebook)}

    for f in files:
        name = os.path.basename(f)
        if a.replace and name in existing:
            print(f"[replace] delete old source {existing[name]} ({name})")
            run(["nlm", "source", "delete", existing[name], "--confirm"])
        r = run(["nlm", "source", "add", a.notebook, "--file", f, "--wait"])
        out = r.stdout + r.stderr
        sid = next(
            (line.split()[-1] for line in out.splitlines() if line.strip().startswith("Source ID:")),
            None,
        )
        if not sid:
            sid = {s.get("title"): s.get("id") for s in list_sources(a.notebook)}.get(name)
        ids[name] = sid
        status = "[ok]" if sid else "[warn] no source ID returned for"
        print(f"{status} {name} -> {sid}")

    os.makedirs(os.path.dirname(os.path.abspath(a.ids_out)), exist_ok=True)
    json.dump(ids, open(a.ids_out, "w"), indent=2, ensure_ascii=False)
    print(f"wrote {a.ids_out}: {len(ids)} image source(s) tracked")


if __name__ == "__main__":
    main()
