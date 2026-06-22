#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P3 step4: 業務UC(画面起点 UC-001..229)の「関連画面イベントID」プレースホルダを
対応 EVT-MMM リンクへ更新する。
- EVT-MMM ↔ UC-PPP は evtmap + uc_crosswalk の突合で一意に求まる。
- システム起点 UC(UC-230..247)は画面イベントなし(—)のまま。
冪等。
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
cw = json.load(open("99_management/crosswalk.json", encoding="utf-8"))
ucw = json.load(open("99_management/uc_crosswalk.json", encoding="utf-8"))
scrmap = cw["scrmap"]
evtmap = cw["evtmap"]

UC_DIR = "01_requirements/02_business_usecases"

# UC-PPP -> EVT-MMM を構築
uc2evt = {}
for key, evt in evtmap.items():            # "旧SCR/EV-nn" -> EVT
    old_scr, ev = key.split("/")
    suffix = old_scr[len("SCR-"):]
    uc_old = f"UC-SCR-{suffix}-EV{ev.split('-')[1]}"
    uc_new = ucw.get(uc_old)
    if uc_new:
        uc2evt[uc_new] = evt

def main():
    updated = 0
    issues = []
    for uc, evt in sorted(uc2evt.items()):
        p = f"{UC_DIR}/{uc}.md"
        if not os.path.exists(p):
            issues.append(f"{uc}: ファイルが無い(EVT {evt})")
            continue
        s = open(p, encoding="utf-8").read()
        link = f"[{evt}](../../02_basic_design/02_screen_events/{evt}.md#{evt})"
        row = f"| 関連画面イベントID | {link} |"
        ns = re.sub(r'(?m)^\| 関連画面イベントID \|.*$', row, s, count=1)
        if ns != s:
            open(p, "w", encoding="utf-8").write(ns)
            updated += 1
    print(f"UC<->EVT linked: {updated} / {len(uc2evt)}")
    if issues:
        print("ISSUES:")
        for x in issues:
            print("  -", x)

if __name__ == "__main__":
    main()
