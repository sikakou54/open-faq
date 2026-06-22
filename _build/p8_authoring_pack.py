#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P8 業務UC オーサリング用データパック生成。

uc_crosswalk_v2.json + FR/BR ファイル走査から、新UCごとに
  - 構成元の旧UCスナップショットパス
  - 事前レンダリング済み FR / RULE リンク行(正しいカテゴリファイルへ解決)
  - BR 選定用の候補(当該機能グループの br ファイルパス)
をまとめた uc_authoring_pack.json を出力する。
"""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XWALK = os.path.join(ROOT, "99_management", "uc_crosswalk_v2.json")
FRDIR = os.path.join(ROOT, "01_requirements", "02_FunctionalRequirement")
BRDIR = os.path.join(ROOT, "01_requirements", "01_BusinessRequirement")
SNAP = "/tmp/uc_old_snapshot"
OUT = os.path.join(ROOT, "99_management", "uc_authoring_pack.json")

GROUP_FILE = {  # group -> ファイル接頭(br/fr 共通)
    "account": "01_account", "faq-ai": "02_faq-ai", "usage": "03_usage",
    "widget": "04_widget", "notification": "05_notification", "security": "06_security",
}


def scan_ids(directory, prefix, suffix):
    """<prefix>-NNN -> ファイル名(basename) を返す。"""
    m = {}
    for f in sorted(glob.glob(os.path.join(directory, f"*{suffix}"))):
        t = open(f, encoding="utf-8").read()
        for mid in re.findall(rf'id="({prefix}-\d+)"', t):
            m[mid] = os.path.basename(f)
    return m


def main():
    d = json.load(open(XWALK, encoding="utf-8"))
    fr_file = scan_ids(FRDIR, "FR", "-fr.md")
    br_file = scan_ids(BRDIR, "BR", "-br.md")

    def fr_link(fid):
        return f"[{fid}](../02_FunctionalRequirement/{fr_file[fid]}#{fid})"

    def rule_link(rid):
        return f"[{rid}](../01_BusinessRequirement/08_rule.md#{rid})"

    packs = []
    for nid in sorted(d["meta"], key=lambda x: int(x.split("-")[1])):
        m = d["meta"][nid]
        g = m["group"]
        gf = GROUP_FILE[g]
        packs.append(dict(
            id=nid,
            name=m["name"],
            actor=m["actor"],
            group=g,
            kind=m["kind"],
            old_ids=d["new_to_old"][nid],
            old_paths=[f"{SNAP}/{o}.md" for o in d["new_to_old"][nid]],
            fr_links=[fr_link(f) for f in m["fr"]],
            rule_links=[rule_link(r) for r in m["rule"]],
            br_group_file_abs=f"01_requirements/01_BusinessRequirement/{gf}-br.md",
            br_group_file_rel=f"../01_BusinessRequirement/{gf}-br.md",
        ))

    json.dump(dict(count=len(packs), br_file_map=br_file, packs=packs),
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # 検証: 全FRがファイル解決できたか
    missing = sorted({f for m in d["meta"].values() for f in m["fr"] if f not in fr_file})
    print(f"packs: {len(packs)}  output: {OUT}")
    if missing:
        print("WARNING unresolved FR ids:", missing)
    else:
        print("all FR ids resolved to category files")


if __name__ == "__main__":
    main()
