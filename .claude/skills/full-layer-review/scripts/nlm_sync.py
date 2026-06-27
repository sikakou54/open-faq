#!/usr/bin/env python3
"""Upload bundle files into a NotebookLM notebook as sources (via `nlm` CLI).

Creates or reuses the notebook, uploads each `<bundles-dir>/*.md` as a file
source (waiting until processed), and writes a name -> source-id map JSON.
Re-run with --replace to delete the prior source for a bundle (matched by
title `<name>.md`) and re-add it — use after editing files for a re-review.

Usage
-----
  python3 nlm_sync.py --notebook myreview --create "My Review" \
      --bundles-dir _nlm/bundles --ids-out _nlm/source_ids.json
  python3 nlm_sync.py --notebook myreview --bundles-dir _nlm/bundles \
      --ids-out _nlm/source_ids.json --replace [only names...]

Notes
- `--notebook` may be an alias, a notebook id, or a title to match. If it does
  not resolve and `--create T` is given, a new notebook is created and aliased.
- Requires `nlm` on PATH (export PATH="$HOME/.local/bin:$PATH").
"""
import os, sys, json, glob, subprocess, argparse

ENV = dict(os.environ)
ENV["PATH"] = os.path.expanduser("~/.local/bin") + ":" + ENV.get("PATH", "")


def run(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, env=ENV, timeout=600, **kw)


def resolve_notebook(ref, create_title, alias):
    r = run(["nlm", "list", "notebooks", "--json"])
    try:
        nbs = json.loads(r.stdout or "[]")
    except json.JSONDecodeError:
        nbs = []
    for nb in nbs:
        if ref in (nb.get("id"), nb.get("title")) or (alias and alias == nb.get("title")):
            return nb["id"]
    # try alias resolution
    ra = run(["nlm", "alias", "get", ref])
    if ra.returncode == 0 and ra.stdout.strip() and "-" in ra.stdout:
        for tok in ra.stdout.split():
            if tok.count("-") >= 4:
                return tok
    if create_title:
        rc = run(["nlm", "notebook", "create", create_title])
        out = rc.stdout + rc.stderr
        nid = next((t for t in out.replace("\n", " ").split() if t.count("-") >= 4 and len(t) >= 32), None)
        if not nid:
            # fall back: re-list and take newest empty
            r2 = run(["nlm", "list", "notebooks", "--json"])
            nbs2 = json.loads(r2.stdout or "[]")
            for nb in nbs2:
                if nb.get("title") == create_title:
                    nid = nb["id"]; break
        if nid:
            run(["nlm", "alias", "set", (alias or ref), nid])
            print(f"created notebook '{create_title}' -> {nid} (alias {alias or ref})")
            return nid
    sys.exit(f"could not resolve notebook '{ref}' (pass --create TITLE to make one)")


def list_sources(nb):
    r = run(["nlm", "source", "list", nb, "--json"])
    try:
        return json.loads(r.stdout or "[]")
    except json.JSONDecodeError:
        return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--notebook", required=True)
    ap.add_argument("--create", default="")
    ap.add_argument("--alias", default="")
    ap.add_argument("--bundles-dir", default="_nlm/bundles")
    ap.add_argument("--ids-out", default="_nlm/source_ids.json")
    ap.add_argument("--replace", action="store_true")
    ap.add_argument("only", nargs="*", help="optional subset of bundle names to sync")
    a = ap.parse_args()

    nb = resolve_notebook(a.notebook, a.create, a.alias)
    run(["nlm", "chat", "configure", nb, "--response-length", "longer"])

    files = sorted(glob.glob(os.path.join(a.bundles_dir, "*.md")))
    if a.only:
        files = [f for f in files if os.path.splitext(os.path.basename(f))[0] in a.only]
    if not files:
        sys.exit(f"no bundle .md files in {a.bundles_dir}")

    ids = {}
    if os.path.exists(a.ids_out):
        try:
            ids = json.load(open(a.ids_out))
        except Exception:
            ids = {}

    existing = {s.get("title"): s.get("id") for s in list_sources(nb)} if a.replace else {}

    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        title = f"{name}.md"
        if a.replace and title in existing:
            print(f"[replace] delete old source {existing[title]} ({title})")
            run(["nlm", "source", "delete", existing[title], "--confirm"])
        r = run(["nlm", "source", "add", nb, "--file", f, "--wait"])
        out = r.stdout + r.stderr
        sid = next((line.split()[-1] for line in out.splitlines() if line.strip().startswith("Source ID:")), None)
        if not sid:  # fallback: re-list and match title
            sid = {s.get("title"): s.get("id") for s in list_sources(nb)}.get(title)
        ids[name] = sid
        print(f"[ok] {title} -> {sid}")

    os.makedirs(os.path.dirname(a.ids_out) or ".", exist_ok=True)
    json.dump(ids, open(a.ids_out, "w"), indent=2, ensure_ascii=False)
    print(f"wrote {a.ids_out}: {json.dumps(ids, ensure_ascii=False)}")
    print(f"notebook id: {nb}")


if __name__ == "__main__":
    main()
