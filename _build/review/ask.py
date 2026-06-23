#!/usr/bin/env python3
"""NotebookLM へレビュー依頼を投げ、結果を保存する標準ヘルパー。

  python3 _build/review/ask.py <name> [--sources k1,k2,...] [--prompt-file PATH]

- 既定で `_build/review/<name>_prompt.md` を依頼文として読む(--prompt-file で上書き可)。
- bundle key(00_rules/01_requirements/...)を source_ids.txt で実 source-id へ解決し
  --source-ids でスコープする(--sources 省略時は全ソース)。
- `nlm notebook query faqrev <prompt> --json` を実行。
- 生 JSON を results/<name>.json、回答本文(+引用根拠)を results/<name>_answer.md に保存。
"""
import os, sys, json, subprocess, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REV = os.path.join(ROOT, "_build", "review")
RES = os.path.join(REV, "results")
NB = "faqrev"


def load_source_ids():
    m = {}
    for line in open(os.path.join(REV, "source_ids.txt"), encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            m[k.strip()] = v.strip()
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--sources", default="")
    ap.add_argument("--prompt-file", default="")
    a = ap.parse_args()

    pf = a.prompt_file or os.path.join(REV, f"{a.name}_prompt.md")
    prompt = open(pf, encoding="utf-8").read()

    cmd = ["nlm", "notebook", "query", NB, prompt, "--json"]
    if a.sources:
        ids = load_source_ids()
        sel = [ids[k.strip()] for k in a.sources.split(",") if k.strip()]
        cmd += ["--source-ids", ",".join(sel)]

    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.local/bin") + ":" + env.get("PATH", "")
    print(f"[ask] name={a.name} sources={a.sources or 'ALL'} prompt_bytes={len(prompt.encode())}")
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=600)
    if p.returncode != 0:
        sys.stderr.write(p.stderr[-2000:])
        sys.exit(p.returncode)

    os.makedirs(RES, exist_ok=True)
    raw = p.stdout
    open(os.path.join(RES, f"{a.name}.json"), "w", encoding="utf-8").write(raw)
    try:
        d = json.loads(raw)
        ans = d.get("answer", "")
        refs = d.get("references", []) or []
        out = [f"# NotebookLM 回答: {a.name}", "",
               f"*sources: {a.sources or 'ALL'} / conversation_id: {d.get('conversation_id','-')}*", "",
               "## 回答本文", "", ans, "", "## 引用根拠(references)", ""]
        for r in refs:
            ct = (r.get("cited_text") or "").strip().replace("\n", " ")
            out.append(f"- [{r.get('citation_number')}] src={r.get('source_id','')[:8]} … {ct[:300]}")
        open(os.path.join(RES, f"{a.name}_answer.md"), "w", encoding="utf-8").write("\n".join(out))
        print(f"[ask] answer_len={len(ans)} refs={len(refs)} -> results/{a.name}_answer.md")
        print("\n========== ANSWER ==========\n")
        print(ans)
    except json.JSONDecodeError:
        open(os.path.join(RES, f"{a.name}_answer.md"), "w", encoding="utf-8").write(raw)
        print("[ask] non-JSON output saved raw")
        print(raw[:4000])


if __name__ == "__main__":
    main()
