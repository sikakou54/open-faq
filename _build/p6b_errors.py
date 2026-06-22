#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P6b: API の `## エラー` を正規化し ERR-NNN を採番、07_errors/ に個別 ID ファイル + index を生成する。
- 各 API の `## エラー` 表(全 59 ファイル)からエラー行を抽出。
- エラーコード(主コード)で正規化・統合し ERR-001.. を採番。
- ERR-NNN.md(エラーコード / HTTP ステータス / メッセージ / 対応EVT / 対応API)を生成。
- index.md(エラーコード一覧・EVT/API↔エラー 対応表)を生成。
- 各 API の `## エラー` 表に `ERR-NNN` 列を追記(最小改変)。
冪等。ルートで実行する。
"""
import re, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

API_DIR = "02_basic_design/03_apis"
ERR_DIR = "02_basic_design/07_errors"

# ---- API → EVT / 名称 マッピング(index.md の対応表から) ----
def load_api_evt():
    txt = open(f"{API_DIR}/index.md", encoding="utf-8").read()
    m = re.search(r'API ↔ UC.*?\n\n(.*?)\n\n##', txt, re.S)
    api_name, api_evt = {}, {}
    for line in m.group(1).splitlines():
        if not line.startswith("| ["):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        apiid = re.search(r'API-\d+', cells[0]).group(0)
        api_name[apiid] = cells[1]
        evts = []
        for e in re.findall(r'EVT-\d+', cells[2]):
            if e not in evts:
                evts.append(e)
        api_evt[apiid] = evts
    return api_name, api_evt

# ---- 各 API の `## エラー` 行を抽出 ----
def extract_rows():
    rows = []  # (apiid, http, code_cell, desc)
    for f in sorted(glob.glob(f"{API_DIR}/API-*.md")):
        apiid = os.path.basename(f)[:-3]
        txt = open(f, encoding="utf-8").read()
        m = re.search(r'\n## エラー\n(.*?)(\n## )', txt, re.S)
        if not m:
            continue
        for line in m.group(1).splitlines():
            line = line.rstrip()
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 3:
                continue
            if cells[0].replace(" ", "") in ("HTTPステータス",) or set(cells[0]) <= set("-: "):
                continue
            rows.append((apiid, cells[0], cells[1], cells[2] if len(cells) > 2 else ""))
    return rows

# ---- 主コード抽出: `CODE`(E-TAX) → (主コード, 分類コード) ----
def parse_code(cell):
    # バッククォート内の最初のトークンを主コード扱い
    bt = re.findall(r'`([^`]+)`', cell)
    paren = re.search(r'[\(（]\s*(E-[A-Z0-9_\-\\]+)\s*[\)）]', cell)
    taxonomy = paren.group(1).replace("\\", "") if paren else ""
    if bt:
        primary = bt[0]
        # 主コードがバッククォート内の E-* の場合はそれを主コードに
        if primary.startswith("E-"):
            taxonomy = primary
    else:
        # バッククォートなし: セル内の最初の語(E-* or 説明)
        t = cell.strip()
        stripped = re.sub(r'\s*[\(（].*$', '', t)
        # 丸括弧で始まる説明セル(例 (未サポート項目)/(冪等))はそのまま主コード扱い
        primary = t if stripped == "" else stripped
        if primary.startswith("E-"):
            taxonomy = primary
    # 主コードが (未サポート項目) 等の説明文の場合はそのまま
    primary = primary.replace("\\", "")
    return primary, taxonomy

# ---- 正規化キー: 主コード + taxonomy で統合 ----
def main():
    api_name, api_evt = load_api_evt()
    rows = extract_rows()

    # canonical key = (primary, taxonomy) だが、同一 primary が複数 taxonomy を持つ場合は分ける。
    # ただし汎用 VALIDATION_ERROR は taxonomy 有無で意味が同じ → primary に寄せる。
    catalog = {}  # key -> dict(primary, taxonomy, http set, descs set, apis [])
    order = []
    for apiid, http, codecell, desc in rows:
        primary, tax = parse_code(codecell)
        key = primary
        if key not in catalog:
            catalog[key] = {"primary": primary, "tax": set(), "http": [], "descs": [], "apis": []}
            order.append(key)
        c = catalog[key]
        if tax:
            c["tax"].add(tax)
        if http and http not in c["http"]:
            c["http"].append(http)
        if desc and desc not in c["descs"]:
            c["descs"].append(desc)
        if apiid not in c["apis"]:
            c["apis"].append(apiid)

    # ERR 採番(出現順)
    errid = {}
    for i, key in enumerate(order, 1):
        errid[key] = f"ERR-{i:03d}"

    # 分類(taxonomy 接頭辞 or 主コードから)
    def category(c):
        tx = " ".join(c["tax"])
        if "E-AUTH-" in tx or c["primary"] in ("INVALID_CREDENTIALS", "LOCKED_OUT", "INVALID_PASSWORD", "REAUTH_REQUIRED", "TOKEN_EXPIRED", "TOKEN_USED", "TOKEN_NOT_FOUND", "RATE_LIMITED", "WIDGET_KEY_INVALID", "SIGNATURE_INVALID"):
            return "認証"
        if "E-AUTHZ-" in tx or c["primary"] in ("PROJECT_ACCESS_DENIED", "PERMISSION_DENIED", "DOMAIN_NOT_ALLOWED", "NOT_FOUND"):
            return "認可"
        if "E-BILL-" in tx or c["primary"] in ("CONTRACT_SUSPENDED", "PAYMENT_METHOD_DECLINED"):
            return "業務(課金)"
        if "E-INPUT-" in tx or "VALIDATION" in c["primary"] or "CSV" in c["primary"] or c["primary"] in ("DUPLICATE_NAME", "EMAIL_ALREADY_USED", "EMAIL_ALREADY_EXISTS", "ALREADY_EXISTS_IN_PROJECT", "ALREADY_VERIFIED", "CONFLICT", "CONTACT_EMAIL_NOT_SET", "TURNSTILE_FAILED", "TURNSTILE_REQUIRED"):
            return "入力検証"
        return "業務"

    # ERR ファイル生成
    os.makedirs(ERR_DIR, exist_ok=True)
    for key in order:
        c = catalog[key]
        eid = errid[key]
        cat = category(c)
        tax = " / ".join(f"`{t}`" for t in sorted(c["tax"])) or "—"
        http = " / ".join(c["http"]) or "—"
        msg = c["descs"][0] if c["descs"] else "—"
        primary_disp = c["primary"]
        if not primary_disp.startswith("(") and not primary_disp.startswith("E-"):
            primary_code = f"`{primary_disp}`"
        else:
            primary_code = primary_disp if primary_disp.startswith("(") else f"`{primary_disp}`"
        # 対応 API / EVT
        apis = c["apis"]
        api_links = " ".join(f"[{a}](../03_apis/{a}.md#{a})" for a in apis)
        evts = []
        for a in apis:
            for e in api_evt.get(a, []):
                if e not in evts:
                    evts.append(e)
        evt_links = " ".join(f"[{e}](../02_screen_events/{e}.md#{e})" for e in evts) or "—"
        # 説明集約
        if len(c["descs"]) > 1:
            desc_block = "\n".join(f"- {d}(対応 API: {a})" for d, a in zip(c["descs"], apis)) if len(c["descs"]) == len(apis) else "\n".join(f"- {d}" for d in c["descs"])
        else:
            desc_block = msg

        body = f"""<!-- portal-top -->
<!-- /portal-top -->

# <span id="{eid}"></span>{eid}: {primary_disp}

> **このページは API レスポンスで返すエラー `{primary_disp}` の HTTP ステータス・分類・メッセージ・対応 API / EVT を定義します。**

*種別 エラー定義 ・ 分類 {cat} ・ ステータス ドラフト*

## <span id="def"></span>1. 定義

| 項目 | 値 |
|----|----|
| エラーコード | {primary_code} |
| 分類コード(taxonomy) | {tax} |
| HTTP ステータス | {http} |
| エラー分類 | {cat} |

## <span id="msg"></span>2. メッセージ

{desc_block}

## <span id="trace"></span>3. 対応 API / EVT

| 観点 | 結線 |
|----|----|
| 対応 API | {api_links} |
| 対応 EVT | {evt_links} |

---

<!-- portal-bottom -->
<!-- /portal-bottom -->
"""
        open(f"{ERR_DIR}/{eid}.md", "w", encoding="utf-8").write(body)

    # index 生成
    lines = []
    lines.append("<!-- portal-top -->")
    lines.append("<!-- /portal-top -->")
    lines.append("")
    lines.append("# エラー設計")
    lines.append("")
    lines.append("> **このページは、API レスポンスで返すエラーコードの一覧と、EVT / API からエラーへの対応表です。** 各エラーは HTTP ステータス・分類・メッセージ・対応 API / EVT を `ERR-NNN.md` で個別定義します。エラーの正本は各 ERR ファイル、認証・認可の判定段との対応は [権限設計](../06_permissions/index.md) を参照します。")
    lines.append("")
    lines.append("*ステータス ドラフト ・ 再構成 P6b*")
    lines.append("")
    lines.append("## <span id=\"reading\"></span>読み順")
    lines.append("")
    lines.append("API設計 ＞ 本エラー設計 ＞ メッセージ設計。各 API の `## エラー` 表から本 ERR を参照する。")
    lines.append("")
    lines.append(f"## <span id=\"list\"></span>1. エラーコード一覧({len(order)})")
    lines.append("")
    lines.append("分類・HTTP ステータス・主エラーコードの索引です。各 ERR の定義は個別ファイルが正本です。")
    lines.append("")
    lines.append("| ERR ID | 分類 | HTTP | エラーコード | 分類コード | メッセージ |")
    lines.append("|----|----|----|----|----|----|")
    for key in order:
        c = catalog[key]
        eid = errid[key]
        cat = category(c)
        tax = " / ".join(f"`{t}`" for t in sorted(c["tax"])) or "—"
        http = " / ".join(c["http"]) or "—"
        primary = c["primary"]
        pcode = primary if primary.startswith("(") else f"`{primary}`"
        msg = c["descs"][0] if c["descs"] else "—"
        lines.append(f"| <span id=\"{eid}\"></span>[{eid}]({eid}.md#{eid}) | {cat} | {http} | {pcode} | {tax} | {msg} |")
    lines.append("")

    # EVT/API ↔ エラー 対応表
    lines.append("## <span id=\"trace\"></span>2. EVT / API ↔ エラー 対応表")
    lines.append("")
    lines.append("各 API(と対応 EVT)が返しうるエラーの結線一覧です。EVT を持たない内部 / IF 系 API は EVT 欄を `—` とします。")
    lines.append("")
    lines.append("| API ID | API名 | 対応EVT | 返しうるエラー |")
    lines.append("|----|----|----|----|")
    # API ごとにエラーを集約
    api_errs = {}
    for key in order:
        for a in catalog[key]["apis"]:
            api_errs.setdefault(a, []).append(errid[key])
    for a in sorted(api_errs):
        evts = api_evt.get(a, [])
        evt_links = " ".join(f"[{e}](../02_screen_events/{e}.md#{e})" for e in evts) or "—"
        err_links = " ".join(f"[{e}]({e}.md#{e})" for e in api_errs[a])
        lines.append(f"| [{a}](../03_apis/{a}.md#{a}) | {api_name.get(a, '')} | {evt_links} | {err_links} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("<!-- portal-bottom -->")
    lines.append("<!-- /portal-bottom -->")
    open(f"{ERR_DIR}/index.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")

    # API の `## エラー` 表に ERR ID 列を追記
    annotate_apis(errid, catalog, order)

    print(f"ERR files: {len(order)}")
    print(f"API rows parsed: {len(rows)}")
    return errid, catalog, order

# ---- API エラー表のエラーコードセルへ ERR-NNN をインライン併記(最小改変) ----
def annotate_apis(errid, catalog, order):
    # primary -> errid 逆引き
    prim2err = {catalog[k]["primary"]: errid[k] for k in order}
    for f in sorted(glob.glob(f"{API_DIR}/API-*.md")):
        txt = open(f, encoding="utf-8").read()
        m = re.search(r'(\n## エラー\n)(.*?)(\n## )', txt, re.S)
        if not m:
            continue
        sec = m.group(2)
        changed = False
        newlines = []
        for line in sec.splitlines():
            if not line.startswith("|"):
                newlines.append(line); continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            # ヘッダ行 / セパレータ行はそのまま
            if cells and ("ステータス" in cells[0] or set("".join(cells)) <= set("-: ")):
                newlines.append(line); continue
            if len(cells) >= 3:
                primary, tax = parse_code(cells[1])
                eid = prim2err.get(primary, "")
                if eid and "07_errors" not in cells[1]:
                    # エラーコードセル末尾へ → ERR-NNN を併記
                    newcell = cells[1] + f" → [{eid}](../07_errors/{eid}.md#{eid})"
                    cells2 = list(cells); cells2[1] = newcell
                    newlines.append("| " + " | ".join(cells2) + " |")
                    changed = True
                else:
                    newlines.append(line)
            else:
                newlines.append(line)
        if not changed:
            continue  # 実データ行の併記が無ければ書き換えない(空行等を保全)
        newsec = "\n".join(newlines)
        txt = txt[:m.start(2)] + newsec + txt[m.end(2):]
        open(f, "w", encoding="utf-8").write(txt)

if __name__ == "__main__":
    main()
