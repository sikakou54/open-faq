import glob, re, os
spec="01_requirements/01_specifications"
# Build BR -> set(UC) via FR rows (BR and UC co-occur on same table row)
br_uc={}
for fr in sorted(glob.glob(f"{spec}/FR-*.md")):
    for line in open(fr, encoding="utf-8"):
        if "BR-" in line and line.lstrip().startswith("|"):
            brs=re.findall(r'BR-(\d+)\.md', line)
            ucs=re.findall(r'UC-(\d+)\.md', line)
            if brs and ucs:
                for b in brs: br_uc.setdefault(b,set()).update(ucs)
PLACE="(該当UCなし=ギャップ)"
indirect=true_gap=0
for bf in sorted(glob.glob(f"{spec}/BR-*.md")):
    s=open(bf,encoding="utf-8").read()
    if PLACE not in s: continue
    bid=re.search(r'BR-(\d+)\.md', bf) or re.search(r'BR-(\d+)', os.path.basename(bf))
    bid=re.search(r'(\d+)', os.path.basename(bf)).group(1)
    if bid in br_uc:
        rep="（直接対応 UC なし。BR→FR→UC で間接的に対応）"; indirect+=1
    else:
        rep="（該当 UC なし）"; true_gap+=1
    open(bf,"w",encoding="utf-8").write(s.replace(PLACE,rep))
print("indirect(間接対応):",indirect," true_gap(真ギャップ):",true_gap)
