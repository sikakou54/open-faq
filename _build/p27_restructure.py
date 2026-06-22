import re, glob, os, shutil, sys
UC="01_requirements/02_business_usecases"; SPEC="01_requirements/01_specifications"

dup = {249:("FR-020","UC-127"),256:("FR-042","UC-036"),264:("FR-076","UC-061"),
 265:("FR-077","UC-077"),266:("FR-078","UC-078"),267:("FR-079","UC-067"),
 269:("FR-081","UC-059"),287:("FR-126","UC-098"),289:("FR-128","UC-099"),294:("FR-133","UC-223")}
reclass = {277:("FR-106","ux"),278:("FR-107","ux"),279:("FR-108","ux"),280:("FR-110","ux"),
 281:("FR-111","ux"),282:("FR-112","ux"),295:("FR-134","ux"),298:("FR-159","ux"),299:("FR-160","ux"),
 290:("FR-129","nfr"),291:("FR-130","nfr"),292:("FR-131","nfr"),293:("FR-132","nfr")}
deleted=set(dup)|set(reclass)
kept=[n for n in range(248,305) if n not in deleted]
renum={old:248+i for i,old in enumerate(kept)}
NOTE={"ux":"(表示・UX要件 — 業務UC対象外)","nfr":"(非機能要件相当 — 業務UC対象外)"}
LABEL={"ux":"表示・UX要件","nfr":"非機能要件相当"}
assert len(deleted)==23 and len(kept)==34, (len(deleted),len(kept))

def rd(p): return open(p,encoding="utf-8").read()
def wr(p,s): open(p,"w",encoding="utf-8").write(s)

# ---- VALIDATE ----
errs=[]
prov=lambda n: re.compile(r'P7 後続\(第2段\)で本要件を実現する業務UC \[UC-%03d\]\([^)]*\) を新設した。'%n)
link=lambda n: f"[UC-{n:03d}](../02_business_usecases/UC-{n:03d}.md#UC-{n:03d})"
for n,(fr,_) in {**dup,**reclass}.items():
    p=f"{SPEC}/{fr}.md"
    if not os.path.exists(p): errs.append(f"missing {p}"); continue
    s=rd(p)
    if link(n) not in s: errs.append(f"{fr}: no table link UC-{n}")
    if not prov(n).search(s): errs.append(f"{fr}: no provenance UC-{n}")
# kept files exist + capture name/fr
keptinfo={}
for old in kept:
    p=f"{UC}/UC-{old:03d}.md"
    if not os.path.exists(p): errs.append(f"missing kept {p}"); continue
    s=rd(p)
    nm=re.search(rf'# <span id="UC-{old:03d}"></span>UC-{old:03d}: (.+)', s)
    fr=re.search(r'対応要件ID \| \[(FR-\d+)\]', s)
    keptinfo[old]=(nm.group(1).strip() if nm else "?", fr.group(1) if fr else "?")
if errs:
    print("VALIDATION FAILED:"); [print(" -",e) for e in errs]; sys.exit(1)
print("validation ok. kept=34 deleted=23")

# ---- MUTATE FR files ----
for n,(fr,tgt) in dup.items():
    p=f"{SPEC}/{fr}.md"; s=rd(p)
    tl=f"[{tgt}](../02_business_usecases/{tgt}.md#{tgt})"
    s=prov(n).sub(f'P7 後続レビューで、本要件は既存の業務UC {tl} が実現すると判断し結び直した。', s)
    s=s.replace(link(n), tl)
    wr(p,s)
for n,(fr,kind) in reclass.items():
    p=f"{SPEC}/{fr}.md"; s=rd(p)
    s=prov(n).sub(f'P7 後続レビューで、本要件は{LABEL[kind]}のため独立した業務UCを持たないと分類した。', s)
    s=s.replace(link(n), NOTE[kind])
    wr(p,s)

# ---- DELETE 23 ----
for n in deleted: os.remove(f"{UC}/UC-{n:03d}.md")

# ---- GLOBAL REMAP (kept old->new) across all design + mgmt ----
def remap(s):
    def f(m):
        n=int(m.group(1))
        return f"UC-{renum[n]:03d}" if n in renum else m.group(0)
    return re.sub(r'UC-(\d{3})', f, s)
files=glob.glob("0[123]_*/**/*.md",recursive=True)+glob.glob("99_management/*.md")+["README.md"]
for p in files:
    if not os.path.exists(p): continue
    s=rd(p); ns=remap(s)
    # refresh kept UC review note
    ns=ns.replace("(機械支援・要レビュー)","(機械支援生成・レビューで存置を確認)")
    if ns!=s: wr(p,ns)

# ---- RENAME kept files old->new (two-phase) ----
for old in kept: shutil.move(f"{UC}/UC-{old:03d}.md", f"{UC}/TMP-{old:03d}.md")
for old in kept: shutil.move(f"{UC}/TMP-{old:03d}.md", f"{UC}/UC-{renum[old]:03d}.md")

# ---- REGENERATE index §5 ----
ip=f"{UC}/index.md"; s=rd(ip)
rows=[]
for old in kept:
    nm,fr=keptinfo[old]; new=renum[old]
    rows.append(f"| [UC-{new:03d}](UC-{new:03d}.md#UC-{new:03d}) | [{fr}](../01_specifications/{fr}.md#{fr}) | {nm} |")
sec=("## <span id=\"req-origin\"></span>5. 要件起点ユースケース(第2段新設)\n\n"
 "P7 後続(第2段)で、画面・システム起点ユースケースに未連結だった機能要件(FR)を起点に業務ユースケースを新設し、"
 "後続レビューで精査しました。重複していた FR は既存の操作 UC へ結び直し、表示・UX / 非機能の FR は業務UC 対象外として要件側に分類した結果、"
 "要件起点 UC は **UC-248〜UC-281(34 件)** に整理されています。下表は各 UC と起点 FR・名称です。\n\n"
 "| UC | 起点FR | 名称 |\n|---|---|---|\n"+"\n".join(rows)+"\n")
s=re.sub(r'## <span id="req-origin"></span>5\..*?(?=\n---\n\n<!-- portal-bottom -->)', sec, s, flags=re.S)
# 総数 247 -> 281, and metadata
s=s.replace("総数 247(画面起点 229 ・ システム起点 18)","総数 281(画面起点 229 ・ システム起点 18 ・ 要件起点 34)")
wr(ip,s)
print("done. UC total now", len(glob.glob(f"{UC}/UC-*.md")))
