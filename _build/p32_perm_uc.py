import glob, re
spec="01_requirements/01_specifications"
PERM="02_basic_design/06_permissions"
# FR -> set(UC)
fr_uc={}
for fr in glob.glob(f"{spec}/FR-*.md"):
    fid=re.search(r'FR-(\d+)',fr).group(1)
    s=open(fr,encoding="utf-8").read()
    fr_uc[fid]=set(re.findall(r'UC-(\d+)\.md',s))
n=0
for pf in sorted(glob.glob(f"{PERM}/PERM-*.md")):
    s=open(pf,encoding="utf-8").read()
    frs=set(re.findall(r'FR-(\d+)\.md',s))
    ucs=set()
    for f in frs: ucs|=fr_uc.get(f,set())
    if not ucs: continue
    links=" ".join(f"[UC-{u}](../../01_requirements/02_business_usecases/UC-{u}.md#UC-{u})"
                   for u in sorted(ucs,key=int))
    new,c=re.subn(r'(\|\s*対応業務UC\s*\|\s*)—(\s*\|)', lambda m: m.group(1)+links+m.group(2), s, count=1)
    if c and new!=s:
        open(pf,"w",encoding="utf-8").write(new); n+=1
print("PERM updated:",n)
