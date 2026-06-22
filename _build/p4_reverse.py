#!/usr/bin/env python3
"""P4 reverse-lookup builder.

Scans EVT-*.md and UC-*.md to map each (old) API ID to the screen events
(EVT), screens (SCR) and business use cases (UC) that reference it.

Output: _build/p4_reverse.json
  { oldApiId: { "evts": [...], "scrs": [...], "ucs": [...] } }

All lists are sorted and de-duplicated. EVT/SCR are sourced from the
"呼出API" + "対応画面ID" rows of each EVT page; UC from the "関連API ID" row
of each UC page.
"""
import os, re, glob, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_RE = re.compile(r'#(API-[A-Z]+-\d+)')

def cell_value(text, label):
    """Return the content cell of a `| <label> | ... |` table row."""
    for line in text.splitlines():
        s = line.strip()
        if s.startswith('|') and label in s:
            parts = [p.strip() for p in s.strip().strip('|').split('|')]
            if len(parts) >= 2 and parts[0] == label:
                return parts[1]
    return ''

def main():
    rev = collections.defaultdict(lambda: {"evts": set(), "scrs": set(), "ucs": set()})

    # EVT pages: 呼出API -> API ids ; 対応画面ID -> SCR id ; this EVT id
    for p in glob.glob(os.path.join(ROOT, '02_basic_design/02_screen_events/EVT-*.md')):
        evt = os.path.splitext(os.path.basename(p))[0]
        text = open(p, encoding='utf-8').read()
        api_cell = cell_value(text, '呼出API')
        apis = API_RE.findall(api_cell)
        if not apis:
            continue
        scr_cell = cell_value(text, '対応画面ID')
        scrs = re.findall(r'#(SCR-[0-9A-Za-z\-]+)', scr_cell)
        for a in apis:
            rev[a]["evts"].add(evt)
            for s in scrs:
                rev[a]["scrs"].add(s)

    # UC pages: 関連API ID -> API ids ; this UC id
    for p in glob.glob(os.path.join(ROOT, '01_requirements/02_business_usecases/UC-*.md')):
        uc = os.path.splitext(os.path.basename(p))[0]
        text = open(p, encoding='utf-8').read()
        api_cell = cell_value(text, '関連API ID')
        apis = API_RE.findall(api_cell)
        for a in apis:
            rev[a]["ucs"].add(uc)

    out = {}
    for k in sorted(rev):
        out[k] = {
            "evts": sorted(rev[k]["evts"]),
            "scrs": sorted(rev[k]["scrs"]),
            "ucs": sorted(rev[k]["ucs"]),
        }
    dest = os.path.join(ROOT, '_build/p4_reverse.json')
    json.dump(out, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print("wrote", dest, "with", len(out), "APIs that have references")
    return out

if __name__ == '__main__':
    main()
