#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画面モックの HTML ソースを MD の <details> から切り出し、mocks/<画面>-<n>.html として保存する。
MD 側は画像(![]())のみを残し、ソースは表示しない。
- ソースは閲覧可能な「完結 HTML」(HEAD + 断片 + TAIL、#wrap でクロップ可)として書き出す。
- PNG は既存(同一ソースから生成済み)をそのまま使用。再生成は mocks/*.html を編集後に
  html-to-png スキル等で mocks/ を再レンダリングする(CLAUDE.md 参照)。
"""
import os, re, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imagify_mocks import HEAD, TAIL

BD = "02_basic-design"
MOCKS = os.path.join(BD, "mocks")
os.makedirs(MOCKS, exist_ok=True)

# ![alt](mocks/X.png) に続く <details>…```html SRC ```…</details> を丸ごと捉える
BLOCK = re.compile(
    r'!\[(?P<alt>[^\]]*)\]\((?P<png>mocks/[^)]+\.png)\)\s*\n+'
    r'<details>\s*<summary>[^<]*</summary>\s*```html\n(?P<src>.*?)\n```\s*</details>',
    re.S)

def main():
    nf = nb = 0
    for md in sorted(glob.glob(os.path.join(BD, "SCR-*.md"))):
        s = open(md, encoding="utf-8").read()
        def repl(m):
            nonlocal nb
            src, png, alt = m.group("src"), m.group("png"), m.group("alt")
            htmlname = os.path.basename(png)[:-4] + ".html"   # SCR-001-1.html
            needs_lucide = "data-lucide" in src
            lucide = ('<script src="https://unpkg.com/lucide@0.460.0/dist/umd/lucide.min.js"></script>'
                      if needs_lucide else "")
            lucideinit = ('<script>lucide.createIcons();</script>' if needs_lucide else "")
            doc = HEAD.replace("__LUCIDE__", lucide) + src + TAIL.replace("__LUCIDEINIT__", lucideinit)
            open(os.path.join(MOCKS, htmlname), "w", encoding="utf-8").write(doc)
            nb += 1
            return f'![{alt}]({png})'    # MD は画像のみ(ソースは mocks/<同名>.html へ)
        s2 = BLOCK.sub(repl, s)
        if s2 != s:
            s2 = re.sub(r'\n{3,}', '\n\n', s2)
            open(md, "w", encoding="utf-8").write(s2); nf += 1
    print(f"externalized {nb} mock sources across {nf} files -> {MOCKS}/*.html")

if __name__ == "__main__":
    main()
