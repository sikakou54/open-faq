#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P8 08_rule.md の `適用UC` 表を新業務UCで再構築。

各 RULE の `適用UC` 表(`| [UC-NNN](...) | 旧名称 |`)を、旧→新クロスウォークで
新業務UC へ写像・重複排除し、新名称付きで作り直す。表外に UC 参照が無いことも検証。

実行: python3 _build/p8_rule_applyuc.py [--apply]
"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XWALK = os.path.join(ROOT, "99_management", "uc_crosswalk_v2.json")
RULEFILE = os.path.join(ROOT, "01_requirements", "01_BusinessRequirement", "08_rule.md")

TABLE_RE = re.compile(r'(\|\s*適用UC\s*\|\s*名称\s*\|\n\|[-|: ]+\|\n)((?:\|[^\n]*\|\n)+)')


def main():
    apply = "--apply" in sys.argv
    d = json.load(open(XWALK, encoding="utf-8"))
    o2n = d["old_to_new"]
    names = {k: v["name"] for k, v in d["meta"].items()}

    s = open(RULEFILE, encoding="utf-8").read()

    def rebuild(m):
        header, body = m.group(1), m.group(2)
        news = []
        for line in body.strip().split("\n"):
            mm = re.search(r'\[UC-(\d+)\]', line)
            if not mm:
                continue
            n = o2n.get("UC-" + mm.group(1))
            if n and n not in news:
                news.append(n)
        rows = "".join(
            f"| [{n}](../04_business_usecases/{n}.md#{n}) | {names[n]} |\n" for n in news)
        return header + rows

    new = TABLE_RE.sub(rebuild, s)

    # 表外に旧UC参照が残っていないか検証(全UCトークンが新ID範囲か)
    leftover = sorted({"UC-" + x for x in re.findall(r'(?<![A-Za-z0-9])UC-(\d+)(?![0-9])', new)
                       if int(x) > d["count"]})
    print("APPLIED" if apply else "DRY-RUN", "rule applyuc rebuild")
    print("  tables rebuilt:", len(TABLE_RE.findall(s)))
    if leftover:
        print("  WARNING out-of-range UC tokens remain:", leftover)
    else:
        print("  all UC tokens within new range UC-001..UC-%03d" % d["count"])
    if apply:
        open(RULEFILE, "w", encoding="utf-8").write(new)


if __name__ == "__main__":
    main()
