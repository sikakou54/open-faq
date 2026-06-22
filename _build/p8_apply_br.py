#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P8 BR精度スイープ結果の適用。

/tmp/br_corrections.json([{id, br_ids, changed, rationale}, ...])を読み、
各 UC の `## 対応する業務要件ID` 節を、補正後 BR で書き換える(リンクは BR-ID→ファイル
走査から決定論的に描画)。存在しない BR-ID はスキップして警告。

実行: python3 _build/p8_apply_br.py [--apply]
"""
import os, re, json, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UCDIR = os.path.join(ROOT, "01_requirements", "04_business_usecases")
BRDIR = os.path.join(ROOT, "01_requirements", "01_BusinessRequirement")
CORR = "/tmp/br_corrections.json"


def br_file_map():
    m = {}
    for f in sorted(glob.glob(os.path.join(BRDIR, "*-br.md"))):
        for mid in re.findall(r'id="(BR-\d+)"', open(f, encoding="utf-8").read()):
            m[mid] = os.path.basename(f)
    return m


def render(br_ids, bmap):
    if not br_ids:
        return "—"
    out = []
    for b in sorted(br_ids, key=lambda x: int(x.split("-")[1])):
        out.append(f"- [{b}](../01_BusinessRequirement/{bmap[b]}#{b})")
    return "\n".join(out)


def main():
    apply = "--apply" in sys.argv
    bmap = br_file_map()
    corr = json.load(open(CORR, encoding="utf-8"))
    sec_re = re.compile(r'(## 対応する業務要件ID\n)(.*?)(\n## )', re.S)
    changed = 0
    invalid = []
    for c in corr:
        if not c.get("changed"):
            continue
        ids = [b for b in c["br_ids"] if b in bmap]
        bad = [b for b in c["br_ids"] if b not in bmap]
        if bad:
            invalid.append((c["id"], bad))
        f = os.path.join(UCDIR, f"{c['id']}.md")
        s = open(f, encoding="utf-8").read()
        body = render(ids, bmap)
        new, n = sec_re.subn(lambda m: m.group(1) + "\n" + body + "\n" + m.group(3), s)
        if n != 1:
            invalid.append((c["id"], "SECTION-NOT-FOUND"))
            continue
        if new != s:
            changed += 1
            if apply:
                open(f, "w", encoding="utf-8").write(new)
    print("APPLIED" if apply else "DRY-RUN", "BR sweep")
    print(f"  UCs with BR changes: {changed}")
    if invalid:
        print("  WARN:", invalid)


if __name__ == "__main__":
    main()
