import glob, re
n=0; coll=0
for f in sorted(glob.glob("02_basic_design/04_database/TBL-*.md")):
    s=open(f,encoding="utf-8").read()
    # section heading ids like id="3131-概要" -> id="概要"
    def repl(m):
        return f'id="{m.group(2)}"'
    new=re.sub(r'id="(\d+)-([^"]+)"', repl, s)
    if new==s: continue
    # collision guard: ensure resulting ids unique within page
    ids=re.findall(r'id="([^"]+)"', new)
    if len(ids)!=len(set(ids)): coll+=1; print("COLLISION",f); continue
    open(f,"w",encoding="utf-8").write(new); n+=1
print("updated:",n,"collisions:",coll)
