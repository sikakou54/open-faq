#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 設計書(_build/src/**.html の <article class="content"> 本文)を Markdown へ変換する。

方針:
  - 本文(article)のみ対象。共通シェル(サイドバー/パンくず/右TOC/フッター/スクリプト)は無視。
  - pandoc(html->gfm)を中核に、以下の特殊要素は前後処理で制御する:
      * 相互参照アンカー(td/tr/h2-4/span の id)→ <a id="X"></a> を注入し pandoc が <span id="X"></span> として保持
      * callout(補足/重要/注意/ヒント)→ GitHub Alert(> [!NOTE] 等)
      * mermaid(<pre class="mermaid">)→ ```mermaid フェンス
      * コード(<pre><code> / sourceCode)→ ```lang フェンス
      * 画面モック/カード等の視覚 HTML(scr-mock / layout-embed / tbl-card / card / inline背景)→ 生 HTML のまま埋め込み
      * doc-meta / page-summary / 装飾アンカー / アイコン / bare span を整形
  - 最後にリンク .html -> .md を一括置換(埋め込み HTML 内も含む)。

使い方: python3 html2md.py <in.html> <out.md>
"""
import os, re, sys, html, subprocess

# ---------- 本文抽出 ----------
def extract_article(s):
    m = re.search(r"<article[^>]*>(.*)</article>", s, re.S)
    body = (m.group(1) if m else s).strip()
    # 先頭のパンくず(crumb / pill 付き div)を除去
    mm = re.match(r'<div\b[^>]*>.*?</div>\s*', body, re.S)
    if mm and ('class="pill"' in mm.group(0) or 'class="crumb"' in mm.group(0)) \
       and body[mm.end():].lstrip().startswith(("<h1", "<div", "<span")):
        # h1 がすぐ後ろに来るパターンのみ除去(crumb 行)
        rest = body[mm.end():].lstrip()
        if rest.startswith("<h1") or '<h1' in body[mm.end():mm.end()+200]:
            body = body[mm.end():].lstrip()
    # 末尾 footer 除去
    body = re.sub(r'\s*<div class="footer">.*?</div>\s*$', "", body, flags=re.S)
    return body.strip()

# ---------- 平衡 div 抽出 ----------
def find_block_end(s, start):
    """s[start] は '<div' の '<'。対応する </div> の直後インデックスを返す。"""
    depth = 0
    i = start
    tag_re = re.compile(r'<(/?)div\b', re.I)
    while i < len(s):
        m = tag_re.search(s, i)
        if not m:
            return len(s)
        if m.group(1) == "":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = s.find(">", m.end())
                return end + 1 if end >= 0 else len(s)
        i = m.end()
    return len(s)

# ---------- 埋め込み(視覚 HTML)保護 ----------
EMBED_SIG = re.compile(
    r'<div\b[^>]*'
    r'(?:class="[^"]*\b(?:scr-mock|layout-embed|tbl-card|card|screen)\b[^"]*"'
    r'|style="[^"]*background:\s*#f5f6f8[^"]*")',
    re.I)

def protect_embeds(body, store):
    out = []
    i = 0
    while True:
        m = EMBED_SIG.search(body, i)
        if not m:
            out.append(body[i:]); break
        out.append(body[i:m.start()])
        end = find_block_end(body, m.start())
        raw = body[m.start():end]
        tok = f"\n\nPHX_EMBED_{len(store)}_PHX\n\n"
        store.append(raw)
        out.append(tok)
        i = end
    return "".join(out)

# ---------- callout 保護 ----------
CALLOUT_TYPE = {"note": "NOTE", "important": "IMPORTANT", "warning": "WARNING", "tip": "TIP"}
CALLOUT_SIG = re.compile(r'<div\b[^>]*class="callout\s+(\w+)"', re.I)

def protect_callouts(body, store):
    out = []
    i = 0
    while True:
        m = CALLOUT_SIG.search(body, i)
        if not m:
            out.append(body[i:]); break
        out.append(body[i:m.start()])
        end = find_block_end(body, m.start())
        raw = body[m.start():end]
        ctype = CALLOUT_TYPE.get(m.group(1).lower(), "NOTE")
        # アイコン <i> を除去
        inner = re.sub(r'<i\b[^>]*></i>', '', raw)
        # タイトル <span class="c-title">X</span>
        tm = re.search(r'<span class="c-title">(.*?)</span>', inner, re.S)
        title = tm.group(1).strip() if tm else ""
        # 本文 = c-title 以降の内側 div テキスト(タグはそのまま pandoc 変換へ回す)
        if tm:
            after = inner[tm.end():]
        else:
            after = inner
        # 外殻 div を剥がす(最初と最後の div)
        after = re.sub(r'</div>\s*</div>\s*$', '', after)
        after = re.sub(r'^\s*<div[^>]*>', '', after)
        tok = f"PHX_CALLOUT_{len(store)}_PHX"
        store.append((ctype, title, after.strip()))
        out.append(f"\n\n{tok}\n\n")
        i = end
    return "".join(out)

# ---------- mermaid 保護 ----------
def protect_mermaid(body, store):
    def repl(m):
        content = html.unescape(m.group(1)).strip("\n")
        tok = f"PHX_MERMAID_{len(store)}_PHX"
        store.append(content)
        return f"\n\n{tok}\n\n"
    return re.sub(r'<pre class="mermaid">(.*?)</pre>', repl, body, flags=re.S)

# ---------- コード保護 ----------
def detect_lang(cls, content):
    if cls and "sql" in cls.lower():
        return "sql"
    c = content.strip()
    if c[:1] in "{[":
        return "json"
    if re.match(r'(?is)\s*(create|select|insert|update|delete|alter|with)\b', c):
        return "sql"
    return ""

def protect_code(body, store):
    # <pre ...><code ...>...</code></pre>
    return re.sub(r'<pre\b([^>]*)>\s*<code\b[^>]*>(.*?)</code>\s*</pre>',
                  lambda m: repl_pre(m, store), body, flags=re.S)

def repl_pre(m, store):
    pre_attrs = m.group(1) or ""
    raw = m.group(2)
    raw = re.sub(r'<[^>]+>', '', raw)      # ハイライト span / 行番号アンカーを除去
    content = html.unescape(raw).strip("\n")
    lang = detect_lang(pre_attrs, content)
    tok = f"PHX_CODE_{len(store)}_PHX"
    store.append((lang, content))
    return f"\n\n{tok}\n\n"

# ---------- アンカー注入 ----------
def inject_anchors(body):
    # 見出し(h2-h4): id を見出し本文先頭の <a id="X"></a> に変換(直前ブロックへの吸着を防ぐ)
    body = re.sub(r'<h([2-4])((?:\s[^>]*?)?)\sid="([^"]+)"((?:\s[^>]*?)?)>',
                  lambda m: f'<h{m.group(1)}{m.group(2)}{m.group(4)}><a id="{m.group(3)}"></a>',
                  body)
    # td: <td ... id="X" ...>CONTENT -> <td ...(id除去)><a id="X"></a>CONTENT
    body = re.sub(r'<td((?:\s[^>]*?)?)\sid="([^"]+)"((?:\s[^>]*?)?)>',
                  lambda m: f'<td{m.group(1)}{m.group(3)}><a id="{m.group(2)}"></a>',
                  body)
    # tr: <tr ... id="X" ...><td...> -> <tr ...(id除去)><td...><a id="X"></a>
    body = re.sub(r'<tr((?:\s[^>]*?)?)\sid="([^"]+)"((?:\s[^>]*?)?)>\s*<td((?:\s[^>]*?)?)>',
                  lambda m: f'<tr{m.group(1)}{m.group(3)}><td{m.group(4)}><a id="{m.group(2)}"></a>',
                  body)
    # span id(既存の空アンカー等)-> a id
    body = re.sub(r'<span((?:\s[^>]*?)?)\sid="([^"]+)"((?:\s[^>]*?)?)>(.*?)</span>',
                  lambda m: f'<a id="{m.group(2)}"></a>{m.group(4)}', body, flags=re.S)
    return body

# ---------- doc-meta / page-summary / 装飾整形 ----------
def transform_docmeta(body):
    def repl(m):
        inner = m.group(1)
        parts = []
        for sm in re.finditer(r'<span[^>]*>(.*?)</span>', inner, re.S):
            t = re.sub(r'<[^>]+>', '', sm.group(1))
            t = re.sub(r'\s+', ' ', t).strip()
            if t:
                parts.append(t)
        line = " ・ ".join(parts)
        return f'<p><em>{line}</em></p>'
    return re.sub(r'<p class="doc-meta">(.*?)</p>', repl, body, flags=re.S)

def transform_summary(body):
    body = body.replace('<aside class="page-summary">', '<blockquote>')
    # page-summary を閉じる </aside> のみ blockquote へ(他に aside は無い想定)
    body = body.replace('</aside>', '</blockquote>')
    body = re.sub(r'<p class="ps-label">(.*?)</p>',
                  r'<p><strong>\1</strong></p>', body, flags=re.S)
    return body

def strip_decoration(body):
    body = re.sub(r'<a class="anchor"[^>]*>.*?</a>', '', body, flags=re.S)  # 見出しの ¶ リンク
    body = re.sub(r'<i\b[^>]*>\s*</i>', '', body)                          # bi / lucide アイコン
    body = re.sub(r'<i\b[^>]*></i>', '', body)
    # CRUD バッジ(on-* が有効)→ 有効文字は大文字、無効は - の 4 文字表記(例 CR--)
    # 内側は必ず C, R, U, D の順の子 span。各 class に on- があれば有効。
    def crud_repl(m):
        return "".join(L if "on-" in m.group(i + 1) else "-"
                       for i, L in enumerate("CRUD"))
    cell = (r'<span\b[^>]*class="crud"[^>]*>\s*'
            r'<span\b[^>]*class="([^"]*)"[^>]*>\s*C\s*</span>\s*'
            r'<span\b[^>]*class="([^"]*)"[^>]*>\s*R\s*</span>\s*'
            r'<span\b[^>]*class="([^"]*)"[^>]*>\s*U\s*</span>\s*'
            r'<span\b[^>]*class="([^"]*)"[^>]*>\s*D\s*</span>\s*</span>')
    body = re.sub(cell, crud_repl, body, flags=re.S)
    # pill / badge span(分類・優先度・SCR/API バッジ)は密着するので末尾に空白を補い中身を残す
    body = re.sub(r'<span\b[^>]*class="[^"]*\b(?:pill|badge)\b[^"]*"[^>]*>(.*?)</span>',
                  r'\1 ', body, flags=re.S)
    # pill リンク(使用元の SCR/API バッジ)も末尾に空白を補う
    body = re.sub(r'(<a\b[^>]*class="[^"]*\bpill\b[^"]*"[^>]*>.*?</a>)', r'\1 ',
                  body, flags=re.S)
    body = body.replace('</b>', '</b> ')                                   # ラベル(<b>画面</b>)と後続の分離
    # class 属性を除去(残すと pandoc がリンク等を生 HTML で温存する)
    # ※ 埋め込み・callout・mermaid・コードは既にプレースホルダ化済みなので影響しない
    body = re.sub(r'\sclass="[^"]*"', '', body)
    # 残存する装飾 div(table-scroll / tbl-scroll / diagram / kv / usedby / flex 等)を unwrap
    # 縦積みの行 div は分離のため終了タグを空白に置換する
    body = re.sub(r'<div\b[^>]*>', '', body)
    body = body.replace('</div>', ' ')
    return body

def unwrap_spans(body):
    # 残存 span(id 無し)を中身だけ残して除去。多重対応のため繰り返す。
    prev = None
    while prev != body:
        prev = body
        body = re.sub(r'<span\b[^>]*>(.*?)</span>', r'\1', body, flags=re.S)
    return body

# ---------- pandoc ----------
def pandoc(htmltext):
    p = subprocess.run(["pandoc", "-f", "html", "-t", "gfm", "--wrap=none"],
                       input=htmltext.encode("utf-8"),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf-8"))
    return p.stdout.decode("utf-8")

def pandoc_inline(htmltext):
    """callout 本文用: ブロックを 1 つの段落群へ。"""
    md = pandoc(htmltext).strip()
    return md

# ---------- 復元 ----------
def restore(md, embeds, callouts, mermaids, codes):
    def mermaid_block(i):
        return f"```mermaid\n{mermaids[i]}\n```"
    def code_block(i):
        lang, content = codes[i]
        return f"```{lang}\n{content}\n```"
    def callout_block(i):
        ctype, title, body_html = callouts[i]
        inner_md = pandoc_inline(body_html) if body_html else ""
        lines = [f"> [!{ctype}]"]
        head = f"> **{title}**" if title else None
        # タイトルと本文を 1 段落にまとめる
        body_lines = inner_md.split("\n") if inner_md else []
        if title and body_lines:
            # 先頭行へタイトルを結合
            first = body_lines[0]
            merged = [f"> **{title}** {first}".rstrip()] + [f"> {l}" if l else ">" for l in body_lines[1:]]
            lines += merged
        elif title:
            lines.append(f"> **{title}**")
        else:
            lines += [f"> {l}" if l else ">" for l in body_lines]
        return "\n".join(lines)

    md = re.sub(r'PHX_MERMAID_(\d+)_PHX', lambda m: mermaid_block(int(m.group(1))), md)
    md = re.sub(r'PHX_CODE_(\d+)_PHX', lambda m: code_block(int(m.group(1))), md)
    md = re.sub(r'PHX_CALLOUT_(\d+)_PHX', lambda m: callout_block(int(m.group(1))), md)
    md = re.sub(r'PHX_EMBED_(\d+)_PHX', lambda m: embeds[int(m.group(1))], md)
    return md

# ---------- リンク .html -> .md ----------
def rewrite_links(md):
    # Markdown リンク ](xxx.html...) と HTML href="xxx.html..."(外部 http は除外)
    md = re.sub(r'(\]\()(?!https?:)([^)\s]+?)\.html(#[^)\s]*)?\)',
                lambda m: f'{m.group(1)}{m.group(2)}.md{m.group(3) or ""})', md)
    md = re.sub(r'(href=")(?!https?:)([^"\s]+?)\.html(#[^"]*)?(")',
                lambda m: f'{m.group(1)}{m.group(2)}.md{m.group(3) or ""}{m.group(4)}', md)
    # リンク表示テキストに残る .html(例 [FUT06.html](FUT06.md))も .md へ
    md = re.sub(r'\[([^\]]*?)\.html(#[^\]]*)?\](?=\()',
                lambda m: f'[{m.group(1)}.md{m.group(2) or ""}]', md)
    return md

# ---------- 後始末 ----------
def cleanup(md):
    md = re.sub(r'(?m)^``` +(\w+)$', r'```\1', md)     # 念のため ``` lang のスペース除去
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip() + "\n"

# ---------- メイン ----------
def convert(src_html):
    body = extract_article(src_html)
    embeds, callouts, mermaids, codes = [], [], [], []
    body = protect_embeds(body, embeds)
    body = protect_mermaid(body, mermaids)
    body = protect_code(body, codes)
    body = protect_callouts(body, callouts)
    body = transform_docmeta(body)
    body = transform_summary(body)
    body = strip_decoration(body)
    body = inject_anchors(body)
    body = unwrap_spans(body)
    md = pandoc(body)
    md = restore(md, embeds, callouts, mermaids, codes)
    md = rewrite_links(md)
    md = cleanup(md)
    return md

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    s = open(inp, encoding="utf-8").read()
    md = convert(s)
    open(outp, "w", encoding="utf-8").write(md)

if __name__ == "__main__":
    main()
