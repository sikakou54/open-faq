import glob, re, os
EVT="02_basic_design/02_screen_events"
n=0; skip=0
for f in sorted(glob.glob(f"{EVT}/EVT-*.md")):
    s=open(f,encoding="utf-8").read()
    m=re.search(r'\|\s*対応画面ID\s*\|\s*(.+?)\s*\|', s)
    if not m: skip+=1; continue
    scr=re.search(r'SCR-(\d+)', m.group(1))
    if not scr: skip+=1; continue
    sid=f"SCR-{scr.group(1)}"
    link=f"[{sid} の §6 画面イベント一覧](../01_screens/{sid}.md#6-画面イベント一覧)"
    body=f"処理内容の正本は対応画面 {link} を参照（二重管理を避けるため本ページには再掲しない）。"
    # replace 処理 section body (between '## 処理' and next '## ')
    new,c=re.subn(r'(## 処理\n)(.*?)(\n## )', lambda mm: mm.group(1)+"\n"+body+"\n"+mm.group(3), s, count=1, flags=re.S)
    if c==0: skip+=1; continue
    # tidy 備考: "...§6 と本ページ。" -> "...§6。"
    new=re.sub(r'(処理内容の正本は\s*SCR-\d+\s*§6)\s*と本ページ。', r'\1。', new)
    if new!=s:
        open(f,"w",encoding="utf-8").write(new); n+=1
print("updated:",n," skipped:",skip)
