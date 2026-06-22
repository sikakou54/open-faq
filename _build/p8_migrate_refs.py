#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P8 旧UC参照の一括張替(クロスウォーク駆動)。

旧 UC-001..281 を新 UC-001..088 へ再ポイントする。基本設計(SCR/EVT/API/TBL/SEQ/PERM とその index)
および 08_rule.md・要件サマリ等の本文中 `UC-NNN` トークンを、衝突しない2パス置換で変換する。
複数の旧UCが同一新UCへ畳まれた結果生じる隣接重複リンクは可能な範囲で dedup する。

新UCファイル本体(04_business_usecases/UC-*.md)と そのフォルダの index.md は対象外
(本体は新採番で作成済み / index は別途再構築)。

実行: python3 _build/p8_migrate_refs.py          # ドライラン(集計のみ)
      python3 _build/p8_migrate_refs.py --apply  # 実書換
"""
import os, re, json, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XWALK = os.path.join(ROOT, "99_management", "uc_crosswalk_v2.json")

SENT_L, SENT_R = "", ""
UC_RE = re.compile(r'(?<![A-Za-z0-9])UC-(\d{3})(?![0-9])')
LINK_RE = re.compile(r'\[UC-\d+\]\([^)]*\)')

# 対象ファイル(glob)。04_business_usecases 配下は除外。08_rule.md は適用UC表を
# 専用に再構築(p8_rule_applyuc.py)するためここでは扱わない。
TARGET_GLOBS = [
    "02_basic_design/**/*.md",
    "01_requirements/99_restructure_result.md",
    "02_basic_design/99_restructure_result.md",
]
EXCLUDE_SUBSTR = ["04_business_usecases/"]


def load_map():
    d = json.load(open(XWALK, encoding="utf-8"))
    return d["old_to_new"]


def remap(text, o2n, unknown):
    def r1(m):
        tok = "UC-" + m.group(1)
        new = o2n.get(tok)
        if new is None:
            unknown.add(tok)
            return tok
        return SENT_L + new[3:] + SENT_R
    text = UC_RE.sub(r1, text)
    text = re.sub(SENT_L + r'(\d{3})' + SENT_R, lambda m: "UC-" + m.group(1), text)
    return text


def dedup_line(line):
    """同一新UCリンクの隣接重複を畳む(・ / カンマ / 空白区切り)。変更があれば区切りも整える。"""
    sep = r'(?:\s*[・,]\s*|\s+)'
    new = line
    prev = None
    while prev != new:
        prev = new
        new = re.sub(r'(\[UC-(\d+)\]\([^)]*\))' + sep + r'\[UC-\2\]\([^)]*\)', r'\1', new)
    if new != line:
        new = re.sub(r'(\s*・\s*){2,}', ' ・ ', new)
        new = re.sub(r'\|\s*・\s*', '| ', new)
        new = re.sub(r'\s*・\s*\|', ' |', new)
    return new


def process(text, o2n, unknown):
    text = remap(text, o2n, unknown)
    out = []
    for line in text.split("\n"):
        if LINK_RE.search(line):
            line = dedup_line(line)
        out.append(line)
    return "\n".join(out)


def targets():
    seen = set()
    for g in TARGET_GLOBS:
        for p in glob.glob(os.path.join(ROOT, g), recursive=True):
            rp = os.path.relpath(p, ROOT)
            if any(s in rp for s in EXCLUDE_SUBSTR):
                continue
            if os.path.isfile(p):
                seen.add(p)
    return sorted(seen)


def main():
    apply = "--apply" in sys.argv
    o2n = load_map()
    unknown = set()
    changed_files = 0
    total_tok_files = 0
    for p in targets():
        s = open(p, encoding="utf-8").read()
        if not UC_RE.search(s):
            continue
        total_tok_files += 1
        new = process(s, o2n, unknown)
        if new != s:
            changed_files += 1
            if apply:
                open(p, "w", encoding="utf-8").write(new)
    print(("APPLIED" if apply else "DRY-RUN"))
    print(f"  files containing UC refs: {total_tok_files}")
    print(f"  files changed: {changed_files}")
    if unknown:
        print(f"  WARNING unknown UC ids (no crosswalk entry): {sorted(unknown)}")
    else:
        print("  all UC tokens mapped (no unknowns)")


if __name__ == "__main__":
    main()
