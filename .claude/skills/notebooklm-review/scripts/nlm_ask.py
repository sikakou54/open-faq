#!/usr/bin/env python3
"""Ask NotebookLM a prompt over a notebook and save the grounded answer.

Runs `nlm notebook query`, optionally scoping to specific bundles (resolved to
source ids via the name->id map written by nlm_sync.py), then extracts the
`answer` text and citation evidence.

Usage
-----
  python3 nlm_ask.py --notebook myreview --prompt-file q1.md \
      --sources rules,docs --ids-map _nlm/source_ids.json --out _nlm/results/q1
  python3 nlm_ask.py --notebook myreview --prompt "Summarize the auth flow."

Output
------
  <out>.json        raw CLI JSON
  <out>_answer.md   answer text + cited evidence (references)
If --out is omitted, prints the answer to stdout.
"""
import os, sys, json, subprocess, argparse

ENV = dict(os.environ)
ENV["PATH"] = os.path.expanduser("~/.local/bin") + ":" + ENV.get("PATH", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--notebook", required=True)
    ap.add_argument("--prompt-file")
    ap.add_argument("--prompt")
    ap.add_argument("--sources", default="", help="comma list of bundle names to scope to")
    ap.add_argument("--ids-map", default="_nlm/source_ids.json")
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    if a.prompt_file:
        prompt = open(a.prompt_file, encoding="utf-8").read()
    elif a.prompt:
        prompt = a.prompt
    else:
        sys.exit("provide --prompt-file or --prompt")

    cmd = ["nlm", "notebook", "query", a.notebook, prompt, "--json"]
    if a.sources:
        ids = json.load(open(a.ids_map))
        sel = []
        for k in [s.strip() for s in a.sources.split(",") if s.strip()]:
            if k not in ids:
                sys.exit(f"source '{k}' not in {a.ids_map} (have: {', '.join(ids)})")
            sel.append(ids[k])
        cmd += ["--source-ids", ",".join(sel)]

    sys.stderr.write(f"[ask] notebook={a.notebook} sources={a.sources or 'ALL'} prompt_bytes={len(prompt.encode())}\n")
    p = subprocess.run(cmd, capture_output=True, text=True, env=ENV, timeout=600)
    if p.returncode != 0:
        sys.stderr.write(p.stderr[-2000:] + "\n")
        sys.exit(p.returncode)

    raw = p.stdout
    try:
        d = json.loads(raw)
        ans = d.get("answer", raw)
        refs = d.get("references", []) or []
    except json.JSONDecodeError:
        d, ans, refs = None, raw, []

    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        open(a.out + ".json", "w", encoding="utf-8").write(raw)
        lines = [f"# NotebookLM answer", "",
                 f"*sources: {a.sources or 'ALL'}*", "", ans, "", "## Cited evidence", ""]
        for r in refs:
            ct = (r.get("cited_text") or "").strip().replace("\n", " ")
            lines.append(f"- [{r.get('citation_number')}] src={str(r.get('source_id',''))[:8]} … {ct[:300]}")
        open(a.out + "_answer.md", "w", encoding="utf-8").write("\n".join(lines))
        sys.stderr.write(f"[ask] answer_len={len(ans)} refs={len(refs)} -> {a.out}_answer.md\n")
    print(ans)


if __name__ == "__main__":
    main()
