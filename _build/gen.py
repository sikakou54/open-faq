#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
new 形式ポータル ジェネレータ(統合版)
- 既存ページの <article class="content"> 本文を抽出し、new 形式の自己完結シェル
  (統一サイドバー / パンくず / 右TOC / フッター / mermaid・lucide・スクロールスパイ)で包む。
- 中身は保持し体裁のみ変換する。
対象:
  要件定義  01_メインシステム/01_要件定義/        -> new/01_要件定義/
  基本設計  01_メインシステム/02_基本設計/new/     -> new/02_基本設計/
基本設計のサイドバー構成は元データ(02_基本設計/new)のサイドバーから自動抽出する。
"""
import os, re, html

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NEW_ROOT   = os.path.dirname(SCRIPT_DIR)                       # .../new
SRC_ROOT   = os.path.join(SCRIPT_DIR, "src")                   # new/_build/src(自己完結ソース)
SRC_REQ    = os.path.join(SRC_ROOT, "requirements")
SRC_BD     = os.path.join(SRC_ROOT, "basic-design")
SRC_FUT    = os.path.join(SRC_ROOT, "future")
WEBHOOK_SRC = os.path.join(SRC_ROOT, "webhook.html")
REQ_PREFIX = "01_requirements/"                               # 配信ルートからの配置(ファイル名は英名・ラベルは日本語)
BD_PREFIX  = "02_basic-design/"
FUT_PREFIX = "03_future/"

def label_from_h1(path, fallback):
    s = open(path, encoding="utf-8").read()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else fallback

# ---------- 元データのサイドバーから基本設計ナビを抽出 ----------------------
def parse_source_nav():
    s = open(os.path.join(SRC_BD, "API-common.html"), encoding="utf-8").read()
    nav = re.search(r'<nav class="nav">(.*?)</nav>', s, re.S).group(1)
    parts, last = [], 0
    sec_re = re.compile(r'<div class="nav-sec"[^>]*>(.*?)</div></div>', re.S)
    top_re = re.compile(r'<a class="nav-top" href="([^"]+)"><span class="n">([^<]+)</span><span>([^<]+)</span></a>')
    hdr_re = re.compile(r'<a class="nav-top" href="([^"]+)"><span class="n">([^<]+)</span><span>([^<]+)</span>')
    chl_re = re.compile(r'<a href="([^"]+)">([^<]+)</a>')
    def grab_tops(seg):
        for m in top_re.finditer(seg):
            href, n, title = m.groups()
            if href != "index.html":
                parts.append(("top", n, title, href))
    for m in sec_re.finditer(nav):
        grab_tops(nav[last:m.start()])
        inner = m.group(1)
        h = hdr_re.search(inner)
        children = chl_re.findall(inner)
        parts.append(("sec", h.group(2), h.group(3), h.group(1), children))
        last = m.end()
    grab_tops(nav[last:])
    return parts

# ---------- 要件定義ナビ ----------------------------------------------------
def fr_children():
    files = sorted((f for f in os.listdir(SRC_REQ)
                    if f.startswith("FR") and f.endswith(".html")), key=lambda x: x[:-5])
    kids = [("概要", REQ_PREFIX + "index.html")]
    for f in files:
        kids.append((label_from_h1(os.path.join(SRC_REQ, f), f[:-5]), REQ_PREFIX + f))
    return kids

def fut_children():
    files = sorted((f for f in os.listdir(SRC_FUT)
                    if f.startswith("FUT") and f.endswith(".html")), key=lambda x: x[:-5])
    kids = [("概要", FUT_PREFIX + "index.html")]
    for f in files:
        kids.append((label_from_h1(os.path.join(SRC_FUT, f), f[:-5]), FUT_PREFIX + f))
    return kids

# ---------- 統合ナビ(トップ = 要件定義 / 基本設計 の2本。基本設計は入れ子) ----
# ノード表現: セクション = dict(n,title,url,children) / リーフ = (label, url)
def build_nav():
    bd_children = [("概要", BD_PREFIX + "index.html")]
    for p in parse_source_nav():
        if p[0] == "sec":
            _, n, title, hdr, children = p
            kids = [(lbl, BD_PREFIX + href) for href, lbl in children]
            bd_children.append({"n": n, "title": title, "url": BD_PREFIX + hdr, "children": kids})
        else:
            _, n, title, href = p
            bd_children.append((f"{n} {title}", BD_PREFIX + href))
    return [
        {"n": "要", "title": "要件定義", "url": REQ_PREFIX + "index.html", "children": fr_children()},
        {"n": "基", "title": "基本設計", "url": BD_PREFIX + "index.html", "children": bd_children},
        {"n": "将", "title": "将来対応", "url": FUT_PREFIX + "index.html", "children": fut_children()},
    ]

NAV = build_nav()

# ---------- ジョブ ----------------------------------------------------------
def bd_index(fname):
    if fname.startswith("SCR-"): return (BD_PREFIX + "01_screen-design.html", "画面設計")
    if fname.startswith("API-"): return (BD_PREFIX + "02_api-design.html", "API設計")
    if fname.startswith("TBL-"): return (BD_PREFIX + "03_database-design.html", "データベース設計")
    return (BD_PREFIX + "index.html", "基本設計")

def jobs():
    js = []
    for f in sorted(os.listdir(SRC_REQ)):
        if f.endswith(".html"):
            js.append(dict(src=os.path.join(SRC_REQ, f), out=REQ_PREFIX + f,
                           pill="要件定義", index_url=REQ_PREFIX + "index.html",
                           index_label="要件定義一覧"))
    for f in sorted(os.listdir(SRC_BD)):
        if f.endswith(".html"):
            iu, il = bd_index(f)
            js.append(dict(src=os.path.join(SRC_BD, f), out=BD_PREFIX + f,
                           pill="基本設計", index_url=iu, index_label=il))
    # API-webhook は元データに欠落しているが nav に存在するため 外部Webhook.html から補完
    if os.path.exists(WEBHOOK_SRC) and not os.path.exists(os.path.join(SRC_BD, "API-webhook.html")):
        js.append(dict(src=WEBHOOK_SRC, out=BD_PREFIX + "API-webhook.html", pill="基本設計",
                       index_url=BD_PREFIX + "02_api-design.html", index_label="API設計"))
    for f in sorted(os.listdir(SRC_FUT)):
        if f.endswith(".html"):
            js.append(dict(src=os.path.join(SRC_FUT, f), out=FUT_PREFIX + f,
                           pill="将来対応", index_url=FUT_PREFIX + "index.html",
                           index_label="将来対応一覧"))
    return js

# ---------- ユーティリティ --------------------------------------------------
def strip_tags(s): return re.sub(r"<[^>]+>", "", s).strip()

def extract_article(src):
    s = open(src, encoding="utf-8").read()
    m = re.search(r"<article[^>]*>(.*)</article>", s, re.S)
    body = (m.group(1) if m else s).strip()
    # 先頭のパンくず div(class="crumb" または inline-style + pill)を除去
    mm = re.match(r'<div\b[^>]*>.*?</div>\s*', body, re.S)
    if mm and 'class="pill"' in mm.group(0) and body[mm.end():].lstrip().startswith("<h1"):
        body = body[mm.end():].lstrip()
    # 末尾の footer div を除去
    body = re.sub(r'\s*<div class="footer">.*?</div>\s*$', "", body, flags=re.S)
    return body.strip()

def ensure_ids(body):
    seen = set(re.findall(r'id="([^"]+)"', body))
    cnt = [0]
    def repl(m):
        lvl, attrs = m.group(1), (m.group(2) or "")
        if "id=" in attrs:
            return m.group(0)
        cnt[0] += 1; hid = f"h{cnt[0]}"
        while hid in seen:
            cnt[0] += 1; hid = f"h{cnt[0]}"
        seen.add(hid)
        return f'<h{lvl}{attrs} id="{hid}">'
    return re.sub(r'<h([23])((?:\s[^>]*?)?)>', repl, body)

def build_toc(body):
    out = []
    for m in re.finditer(r'<h([23])\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h\1>', body, re.S):
        out.append((m.group(1), m.group(2), strip_tags(m.group(3))))
    return out

def page_title(body, src):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    if m: return strip_tags(m.group(1))
    s = open(src, encoding="utf-8").read()
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    return strip_tags(m.group(1)).split("|")[0].strip() if m else "ページ"

def depth_prefix(out_rel):
    d = out_rel.count("/")
    return "../" * d if d else ""

def node_contains(node, cur):
    if isinstance(node, tuple):
        return node[1] == cur
    if node["url"] == cur:
        return True
    return any(node_contains(c, cur) for c in node["children"])

def render_item(node, prefix, cur):
    if isinstance(node, tuple):
        lbl, u = node
        return f'<a class="{"cur active" if u == cur else ""}" href="{prefix + u}">{lbl}</a>'
    opened = node_contains(node, cur)
    hdr_active = " active" if node["url"] == cur else ""
    out = [f'<div class="nav-sec{" open" if opened else ""}" data-sec="{node["url"]}">'
           f'<a class="nav-top{hdr_active}" href="{prefix + node["url"]}">'
           f'<span class="n">{node["n"]}</span><span>{node["title"]}</span>'
           f'<span class="caret">&#9656;</span></a><div class="nav-children">']
    for c in node["children"]:
        out.append(render_item(c, prefix, cur))
    out.append('</div></div>')
    return "".join(out)

def render_sidebar(prefix, cur_url):
    P = [f'<aside class="sidebar"><a class="brand" href="{prefix}index.html">'
         '<div class="mark">FA</div><div><b>FAQ AI SaaS</b><span>設計ポータル</span></div></a>'
         '<nav class="nav"><div class="nav-group">ドキュメント</div>']
    for node in NAV:
        P.append(render_item(node, prefix, cur_url))
    P.append('</nav></aside>')
    return "".join(P)

def render_rightbar(prefix, toc, index_url, index_label):
    rows = [f'<a class="back" href="{prefix+index_url}">&larr; {index_label}へ</a>']
    for lvl, hid, txt in toc:
        rows.append(f'<a class="{"lvl3" if lvl=="3" else ""}" href="#{hid}">{html.escape(txt)}</a>')
    return ('<aside class="rightbar"><div class="rb-title">このページ</div>'
            '<nav class="toc">' + "".join(rows) + '</nav></aside>')

BI    = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800&display=swap" rel="stylesheet">')
LUCIDE_CDN  = '<script src="https://cdn.jsdelivr.net/npm/lucide@0.460.0/dist/umd/lucide.min.js"></script>'
LUCIDE_INIT = '<script>window.addEventListener("load",function(){try{window.lucide&&lucide.createIcons();}catch(e){}});</script>'
MERMAID = ('<script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";'
           'mermaid.initialize({startOnLoad:true,theme:"neutral",flowchart:{useMaxWidth:true},'
           'sequence:{useMaxWidth:true,wrap:true,actorMargin:60}});</script>')
SPY = '<script>(function(){function init(){var ls=[].slice.call(document.querySelectorAll(".rightbar .toc a[href^=\\"#\\"]"));if(!ls.length)return;var map=ls.map(function(a){var id=decodeURIComponent(a.getAttribute("href").slice(1));return{a:a,el:document.getElementById(id)};}).filter(function(x){return x.el;});function on(){var y=window.scrollY+130,cur=null;map.forEach(function(x){if(x.el.getBoundingClientRect().top+window.scrollY<=y)cur=x;});ls.forEach(function(a){a.classList.remove("active");});if(cur)cur.a.classList.add("active");}window.addEventListener("scroll",on,{passive:true});window.addEventListener("resize",on);on();}if(document.readyState!=="loading")init();else document.addEventListener("DOMContentLoaded",init);})();</script>'
# ナビ: caret 開閉トグル + 展開状態(localStorage)とスクロール位置(sessionStorage)をページ遷移後も保持
CARET = '<script>(function(){var K="portal-nav-open",S="portal-nav-scroll";var sb=document.querySelector(".sidebar");function sid(s){return s.getAttribute("data-sec")||"";}try{var o=JSON.parse(localStorage.getItem(K)||"[]");document.querySelectorAll(".nav-sec").forEach(function(s){if(o.indexOf(sid(s))>=0)s.classList.add("open");});}catch(e){}function save(){try{var o=[];document.querySelectorAll(".nav-sec.open").forEach(function(s){o.push(sid(s));});localStorage.setItem(K,JSON.stringify(o));}catch(e){}}document.querySelectorAll(".nav-sec > .nav-top .caret").forEach(function(c){c.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();c.closest(".nav-sec").classList.toggle("open");save();});});document.querySelectorAll(".nav a[href]").forEach(function(a){a.addEventListener("click",save);});try{var v=sessionStorage.getItem(S);if(v&&sb)sb.scrollTop=parseInt(v,10);}catch(e){}if(sb)sb.addEventListener("scroll",function(){try{sessionStorage.setItem(S,sb.scrollTop);}catch(e){}},{passive:true});})();</script>'

PAGE = """<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | FAQ 設計ポータル</title>
{fonts}{bi}{lucide_cdn}{mermaid}
<link rel="stylesheet" href="{css}?v=4">
</head><body><div class="layout">
{sidebar}
<main class="main"><article class="content">
<div class="crumb"><span class="pill">{pill}</span><a class="muted" href="{index_href}">{index_label}</a><span class="muted">/</span><span class="muted">{title}</span></div>
{body}
<div class="footer">FAQ AI ウィジェット SaaS / メインシステム &mdash; {pill} ・ new 形式ポータル</div>
</article></main>
{rightbar}
</div>
{lucide_init}{spy}{caret}
</body></html>
"""

def render_page(job):
    out_rel = job["out"]; prefix = depth_prefix(out_rel)
    body = ensure_ids(extract_article(job["src"]))
    title = page_title(body, job["src"])
    toc = build_toc(body)
    needs_mermaid = 'class="mermaid"' in body
    needs_lucide  = "data-lucide" in body
    return PAGE.format(
        title=html.escape(title), fonts=FONTS, bi=BI,
        lucide_cdn=(LUCIDE_CDN if needs_lucide else ""),
        mermaid=(MERMAID if needs_mermaid else ""),
        css=prefix + "style.css",
        sidebar=render_sidebar(prefix, out_rel),
        pill=job["pill"], index_href=prefix + job["index_url"], index_label=job["index_label"],
        body=body, rightbar=render_rightbar(prefix, toc, job["index_url"], job["index_label"]),
        lucide_init=(LUCIDE_INIT if needs_lucide else ""), spy=SPY, caret=CARET)

def render_portal_index():
    prefix = ""; cur = "index.html"
    body = """<div class="crumb"><span class="pill">ポータル</span><span class="muted">概要</span></div>
<h1>FAQ AI ウィジェット SaaS / 設計ポータル（new 形式）</h1>
<aside class="page-summary"><p class="ps-lead"><strong>このポータルは、メインシステムの設計ドキュメントを new 形式（自己完結ページ）で集約します。</strong> 要件定義と基本設計を移行済みです。</p></aside>
<h2 id="docs">収録ドキュメント</h2>
<ul>
<li><a href="01_requirements/index.html">要件定義</a> — FR01〜FR21 + 一覧</li>
<li><a href="02_basic-design/index.html">基本設計</a> — 画面設計 / API設計 / データベース設計 / ユースケース / 課金請求 / メール / 認証認可</li>
<li><a href="03_future/index.html">将来対応</a> — FUT01〜FUT06 + 一覧</li>
</ul>
<div class="callout note"><i class="bi bi-info-circle"></i><div><span class="c-title">移行ステータス</span>既存の中身を保持したまま体裁のみ new 形式へ変換しています。要件定義本文に含まれる一部の旧基本設計参照（エラー設計・トレーサビリティ等、new では別構成）は未到達となる場合があります。</div></div>
"""
    toc = build_toc(ensure_ids(body))
    page = PAGE.format(title="ポータル概要", fonts=FONTS, bi=BI, lucide_cdn="", mermaid="",
        css="style.css", sidebar=render_sidebar(prefix, cur),
        pill="ポータル", index_href=REQ_PREFIX + "index.html", index_label="要件定義一覧",
        body=re.sub(r'^<div class="crumb">.*?</div>\s*', "", body, flags=re.S),
        rightbar=render_rightbar(prefix, toc, REQ_PREFIX + "index.html", "要件定義一覧"),
        lucide_init="", spy=SPY, caret=CARET)
    open(os.path.join(NEW_ROOT, "index.html"), "w", encoding="utf-8").write(page)

def main():
    n = 0
    for job in jobs():
        out_path = os.path.join(NEW_ROOT, *job["out"].split("/"))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        open(out_path, "w", encoding="utf-8").write(render_page(job))
        n += 1
    render_portal_index()
    print(f"--- {n} ページ + portal index 生成 ---")

if __name__ == "__main__":
    main()
