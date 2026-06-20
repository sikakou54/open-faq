#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SCR 画面モック(埋め込み HTML)を PNG 画像化し、元 HTML は <details> で保持する。
- 対象: 02_basic-design/SCR-*.md の行頭 <div>(背景 #f5f6f8 / scr-mock / layout-embed)
- 各モックを assets/mocks/<stem>-<n>.png として画像化(レンダリングは render_mocks.js)
- md 内のモックを「画像 + <details>(ソース)」へ置換
出力: /tmp/mockwork/manifest.json(html→png のリスト)
"""
import os, re, json, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from html2md import find_block_end

ROOT = os.getcwd()
BD = "02_basic-design"
ASSETS = "assets/mocks"
WORK = "/tmp/mockwork"
os.makedirs(os.path.join(ROOT, ASSETS), exist_ok=True)
os.makedirs(WORK, exist_ok=True)

SIG = re.compile(r'(background:\s*#f5f6f8|class="[^"]*\b(?:scr-mock|layout-embed)\b)')

HEAD = """<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">
<style>
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff}
body{font-family:'Noto Sans JP','Hiragino Kaku Gothic ProN','Hiragino Sans',Meiryo,sans-serif;color:#3a3f46;-webkit-font-smoothing:antialiased}
#wrap{display:inline-block}
.scr-mock,.screen{background:#fff}
.le-cap{font-size:12px;font-weight:700;color:#16191d;margin:0 0 8px}
.screen{border:1px solid #e6e8eb;border-radius:12px;overflow:hidden;width:1024px}
.screen-header{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;background:#fbfbfc;border-bottom:1px solid #eef0f2;font-size:12px}
.scr-name{font-weight:700;color:#16191d}.scr-user{color:#8a9099;font-size:11px}
.modal-overlay{background:rgba(16,24,40,.35);padding:28px;display:flex;justify-content:center}
.modal-card{background:#fff;border-radius:12px;box-shadow:0 12px 40px rgba(16,24,40,.18);padding:22px}
.panel{border:1px solid #eef0f2;border-radius:9px;padding:12px;margin:10px 0;background:#fbfbfc}
.panel-title{font-weight:700;font-size:12px;margin-bottom:6px}
.field{margin:10px 0;font-size:12px}.req{color:#e5484d}
.btn{border:none;border-radius:9px;padding:9px 16px;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit}
.btn.primary{background:#5e6ad2;color:#fff}
.link{color:#5e6ad2;text-decoration:none}
input[type=checkbox]{transform:translateY(1px)}
table{border-collapse:collapse}
</style>
__LUCIDE__
</head><body><div id="wrap">"""
TAIL = "</div>__LUCIDEINIT__</body></html>"

def main():
    manifest = []
    files = sorted(f for f in os.listdir(BD) if f.startswith("SCR-") and f.endswith(".md"))
    for f in files:
        path = os.path.join(BD, f)
        s = open(path, encoding="utf-8").read()
        stem = f[:-3]
        # モック署名を持つ <div>(行頭に限らない)を全て検出し、入れ子を除外して最外ブロックのみ採用
        cands = []
        for m in re.finditer(r'<div\b[^>]*>', s):
            if SIG.search(m.group(0)):
                cands.append((m.start(), find_block_end(s, m.start())))
        cands = sorted(set(cands))
        blocks = [(st, en) for st, en in cands
                  if not any(a <= st and en <= b and (a, b) != (st, en) for a, b in cands)]
        if not blocks:
            continue
        # 画像化 HTML を書き出し + 置換テキスト準備
        repls = []
        for i, (a, b) in enumerate(blocks, 1):
            src = s[a:b]
            needs_lucide = "data-lucide" in src
            lucide = ('<script src="https://unpkg.com/lucide@0.460.0/dist/umd/lucide.min.js"></script>'
                      if needs_lucide else "")
            lucideinit = ('<script>lucide.createIcons();</script>' if needs_lucide else "")
            doc = HEAD.replace("__LUCIDE__", lucide) + src + TAIL.replace("__LUCIDEINIT__", lucideinit)
            hpath = os.path.join(WORK, f"{stem}-{i}.html")
            open(hpath, "w", encoding="utf-8").write(doc)
            png_rel = f"../{ASSETS}/{stem}-{i}.png"
            png_abs = os.path.join(ROOT, ASSETS, f"{stem}-{i}.png")
            manifest.append({"html": hpath, "png": png_abs, "lucide": needs_lucide})
            label = f"{stem} 画面レイアウト" + (f"({i})" if len(blocks) > 1 else "")
            repl = (f"\n\n![{label}]({png_rel})\n\n"
                    f"<details>\n<summary>画面モック HTML（ソース）</summary>\n\n"
                    f"```html\n{src}\n```\n\n</details>\n\n")
            repls.append((a, b, repl))
        # 後ろから置換(オフセット保持)
        for a, b, repl in sorted(repls, key=lambda x: -x[0]):
            s = s[:a] + repl + s[b:]
        s = re.sub(r'[ \t]+\n', '\n', s)      # 行末空白(連結部の空白行)を除去
        s = re.sub(r'\n{3,}', '\n\n', s)      # 余分な空行を圧縮
        open(path, "w", encoding="utf-8").write(s)
    json.dump(manifest, open(os.path.join(WORK, "manifest.json"), "w"), ensure_ascii=False, indent=1)
    print(f"prepared {len(manifest)} mock images across {len(set(m['html'].split('-')[0] for m in manifest))} stems")
    print(f"manifest: {os.path.join(WORK,'manifest.json')}")

if __name__ == "__main__":
    main()
