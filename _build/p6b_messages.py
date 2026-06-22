#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P6b: メール設計書(06_mail-design.md)を MSG の個別 ID ファイル化する。
- 08_messages/MSG-NNN.md(メールテンプレート単位。件名・本文・変数・送信契機・対応SCR/EVT/ERR)
- 08_messages/index.md(メッセージ一覧 + メール共通基準 + 配信運用 + 画面メッセージ参照)
移管後 06_mail-design.md は別途削除する。冪等。ルートで実行する。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MSG_DIR = "02_basic_design/08_messages"
SRC = "02_basic_design/06_mail-design.md"
os.makedirs(MSG_DIR, exist_ok=True)

SCR = "../01_screens"

# TPL → 対応SCR / 対応ERR(発火条件・着地ページ・備考から手動結線)
TPL_TRACE = {
    "TPL-EMAIL_VERIFY":          {"scr": ["SCR-002", "SCR-018"], "err": ["ERR-008"]},
    "TPL-PASSWORD_RESET":        {"scr": ["SCR-003"], "err": ["ERR-008", "ERR-009"]},
    "TPL-ADMIN_USER_REGISTER":   {"scr": ["SCR-014", "SCR-023"], "err": []},
    "TPL-PROJECT_CONTACT_VERIFY":{"scr": ["SCR-005", "SCR-024"], "err": ["ERR-008", "ERR-009"]},
    "TPL-LOCKOUT_NOTIFY":        {"scr": ["SCR-001", "SCR-003"], "err": ["ERR-004"]},
    "TPL-DELETION_REMINDER":     {"scr": ["SCR-019"], "err": []},
    "TPL-BILLING_INVOICE_ISSUED":{"scr": ["SCR-028"], "err": []},
    "TPL-BILLING_PAYMENT_FAILED":{"scr": ["SCR-028"], "err": ["ERR-030"]},
    "TPL-BILLING_SUSPENSION":    {"scr": ["SCR-028"], "err": ["ERR-006"]},
    "TPL-PAYMENT_METHOD_REQUIRED":{"scr": ["SCR-028"], "err": []},
    "TPL-TERMS_REVISION":        {"scr": ["SCR-020"], "err": []},
    "TPL-SERVICE_ANNOUNCEMENT":  {"scr": ["SCR-016"], "err": []},
    "TPL-SYSTEM_NOTICE":         {"scr": ["SCR-026", "SCR-028", "SCR-022"], "err": []},
}

# §3 索引テーブルから TPL メタ(通知ID / 重要度 / 配信先 / 強制送信 / リンク有効期限)
def parse_index_table(txt):
    meta = {}
    m = re.search(r'## <span id="3-テンプレート一覧">.*?\n\n(.*?)\n\n', txt, re.S)
    block = re.search(r'\| \\# \| テンプレートID.*?\n(.*?)\n\n', txt, re.S).group(1)
    for line in block.splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 7 or cells[0] in ("\\#",) or set("".join(cells)) <= set("-: "):
            continue
        tpl = cells[1].strip()
        if not tpl.startswith("TPL-"):
            continue
        meta[tpl] = {
            "notif": cells[2], "sev": cells[3], "to": cells[4],
            "force": cells[5], "expire": cells[6],
        }
    return meta

# §4.x の本文を抽出(見出し行は除き、区切り線 ----- まで)
def parse_templates(txt):
    secs = []
    pat = re.compile(r'### <span id="4[^"]*"></span>(4\.\d+)\s+(TPL-[A-Z_]+)[^\n]*\n(.*?)(?=\n### <span id="4|\n## <span id="5)', re.S)
    for m in pat.finditer(txt):
        num, tpl, body = m.group(1), m.group(2), m.group(3)
        # 末尾の水平線群を除去
        body = re.sub(r'\n-{10,}\s*$', '', body.rstrip())
        secs.append((tpl, body.strip()))
    return secs

def linklist(items, base):
    if not items:
        return "—"
    return " ".join(f"[{x}]({base}/{x}.md#{x})" for x in items)

def errlist(items):
    if not items:
        return "—"
    return " ".join(f"[{x}](../07_errors/{x}.md#{x})" for x in items)

def build():
    txt = open(SRC, encoding="utf-8").read()
    meta = parse_index_table(txt)
    templates = parse_templates(txt)

    msgids = []
    for i, (tpl, body) in enumerate(templates, 1):
        mid = f"MSG-{i:03d}"
        m = meta.get(tpl, {})
        tr = TPL_TRACE.get(tpl, {"scr": [], "err": []})
        # 件名抽出(本文から **件名**: 行)
        sm = re.search(r'\*\*件名\*\*[:：]\s*(.+)', body)
        subject = sm.group(1).strip() if sm else "—"
        # タイトル: テンプレ説明(本文1段落)を簡約
        title = tpl
        out = []
        out.append("<!-- portal-top -->")
        out.append("<!-- /portal-top -->")
        out.append("")
        out.append(f"# <span id=\"{mid}\"></span>{mid}: {tpl}")
        out.append("")
        out.append(f"> **このページは、メールテンプレート `{tpl}` の送信契機・件名・本文・テンプレート変数を定義する正本です。**")
        out.append("")
        out.append("*種別 メッセージ(メール)・ ステータス ドラフト ・ 再構成 P6b*")
        out.append("")
        out.append("## <span id=\"meta\"></span>1. テンプレートメタ")
        out.append("")
        out.append("配信先・重要度・強制送信可否・リンク有効期限の索引です。共通基準は [メッセージ設計 index §共通基準](index.md#common) が正本です。")
        out.append("")
        out.append("| 項目 | 値 |")
        out.append("|----|----|")
        out.append(f"| テンプレートID | `{tpl}` |")
        out.append(f"| 通知ID | {m.get('notif','—')} |")
        out.append(f"| 重要度 | {m.get('sev','—')} |")
        out.append(f"| 配信先 | {m.get('to','—')} |")
        out.append(f"| 強制送信 | {m.get('force','—')} |")
        out.append(f"| リンク有効期限 | {m.get('expire','—')} |")
        out.append(f"| 件名 | {subject} |")
        out.append("")
        out.append("## <span id=\"trace\"></span>2. 対応画面 / EVT / ERR")
        out.append("")
        out.append("本メッセージに関連する画面・エラーの結線です。EVT は対応画面の §6 画面イベント一覧を参照します。")
        out.append("")
        out.append("| 観点 | 結線 |")
        out.append("|----|----|")
        out.append(f"| 対応画面SCR | {linklist(tr['scr'], SCR)} |")
        out.append(f"| 対応ERR | {errlist(tr['err'])} |")
        out.append("")
        out.append("## <span id=\"body\"></span>3. テンプレート定義")
        out.append("")
        out.append("発火条件・テンプレート変数・件名・本文(テキスト / HTML 版)です。本文の件名・テキストは送信される文言そのものの正本です。")
        out.append("")
        # 本文をそのまま転記(画面設計参照の相対パスを修正: 01_screens は同階層へ ../01_screens)
        moved = body
        moved = moved.replace("01_screens/index.md", "../01_screens/index.md")
        moved = moved.replace("](04_database/", "](../04_database/")
        out.append(moved)
        out.append("")
        out.append("---")
        out.append("")
        out.append("<!-- portal-bottom -->")
        out.append("<!-- /portal-bottom -->")
        open(f"{MSG_DIR}/{mid}.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
        msgids.append((mid, tpl, m, subject))

    build_index(txt, msgids)
    print(f"MSG files: {len(msgids)}")
    return msgids

# 共通基準(§2)・配信運用(§5)・開発フロー(§6)を index へ転記
def extract_section(txt, start_anchor, end_anchor):
    m = re.search(re.escape(start_anchor) + r'(.*?)' + re.escape(end_anchor), txt, re.S)
    return m.group(1) if m else ""

def build_index(txt, msgids):
    # §2 共通基準
    common = extract_section(txt, '## <span id="2-共通基準"></span>2. 共通基準\n', '## <span id="3-テンプレート一覧">')
    # §5 配信運用
    ops = extract_section(txt, '## <span id="5-配信運用"></span>5. 配信運用\n', '## <span id="6-テンプレート開発運用フロー">')
    # §6 開発フロー
    devflow = extract_section(txt, '## <span id="6-テンプレート開発運用フロー"></span>6. テンプレート開発・運用フロー\n', '## <span id="更新履歴">')

    def fixrel(s):
        s = s.replace("01_screens/index.md", "../01_screens/index.md")
        s = s.replace("](04_database/", "](../04_database/")
        s = s.replace("[メール設計書](06_mail-design.md)", "本書")
        s = s.replace("[データベース設計.md](../04_database/index.md)", "[データベース設計.md](../04_database/index.md)")
        s = s.replace("[`M_CONTRACT`](../04_database/TBL-002.md)", "[`M_CONTRACT`](../04_database/TBL-002.md#TBL-002)")
        return s

    L = []
    L.append("<!-- portal-top -->")
    L.append("<!-- /portal-top -->")
    L.append("")
    L.append("# メッセージ設計")
    L.append("")
    L.append("> **このページは、メインシステムが送信する全メールテンプレート(`MSG-NNN`)の一覧と、メール共通基準・配信運用ルールの正本です。** 各テンプレートの件名・本文・変数・送信契機は個別 `MSG-NNN.md` が正本です。画面に表示する確認・完了・エラーメッセージの文言は各 [画面設計](../01_screens/index.md)(SCR の §4 / §6)、拒否時のエラーコードは [エラー設計](../07_errors/index.md) が正本です。")
    L.append("")
    L.append("*ステータス ドラフト ・ 再構成 P6b*")
    L.append("")
    L.append("## <span id=\"reading\"></span>読み順")
    L.append("")
    L.append("画面設計(画面文言)/ API設計 / エラー設計 ＞ 本メッセージ設計(メールテンプレート)。配信宛先解決ロジックは [権限設計 PERM-011](../06_permissions/PERM-011.md#PERM-011) が正本です。")
    L.append("")
    L.append(f"## <span id=\"list\"></span>1. メッセージ(メールテンプレート)一覧({len(msgids)})")
    L.append("")
    L.append("メール送信を含む全テンプレートの索引です。件名 + 本文の全文は各 MSG ファイルを参照します。")
    L.append("")
    L.append("| MSG ID | テンプレートID | 通知ID | 重要度 | 配信先 | 強制送信 | リンク有効期限 |")
    L.append("|----|----|----|----|----|----|----|")
    for mid, tpl, m, subject in msgids:
        L.append(f"| <span id=\"{mid}\"></span>[{mid}]({mid}.md#{mid}) | `{tpl}` | {m.get('notif','—')} | {m.get('sev','—')} | {m.get('to','—')} | {m.get('force','—')} | {m.get('expire','—')} |")
    L.append("")
    L.append("> [!NOTE]")
    L.append("> **本書の範囲と対象外** 本書は `MSG-*`(= `TPL-*`)各件の件名 / テキスト本文 / HTML 本文・送信契機(`NOTIF-*`)・配信先 / 重要度 / 添付 / リンク有効期限・メール共通要件(送信元・i18n・サニタイズ・配信信頼性)を扱います。`NOTIF-CHAT_HOLD_CHECK` はチャネルが `inbox` 限定(メール送信なし)のため対象外、画面文言は [画面設計](../01_screens/index.md) が正本です。")
    L.append("")
    # 共通基準・配信運用・開発フローを転記
    L.append("## <span id=\"common\"></span>2. メール共通基準")
    L.append("")
    L.append(fixrel(common).strip())
    L.append("")
    L.append("## <span id=\"ops\"></span>3. 配信運用")
    L.append("")
    L.append(fixrel(ops).strip())
    L.append("")
    L.append("## <span id=\"devflow\"></span>4. テンプレート開発・運用フロー")
    L.append("")
    L.append(fixrel(devflow).strip())
    L.append("")
    L.append("## <span id=\"screen-msg\"></span>5. 画面メッセージ(参照)")
    L.append("")
    L.append("画面に表示する確認・完了・エラーメッセージ(`MSG-SCR-*` 相当)の文言は各画面設計が正本です。本書はメール文言の正本に限定します。")
    L.append("")
    L.append("| メッセージ種別 | 正本 |")
    L.append("|----|----|")
    L.append("| 画面の入力検証・エラー表示文言 | 各 [画面設計](../01_screens/index.md) SCR の §4 画面項目定義 |")
    L.append("| 確認ダイアログ・完了トースト文言 | 各 [画面設計](../01_screens/index.md) SCR の §6 画面イベント一覧 |")
    L.append("| API エラーコード(HTTP / 分類) | [エラー設計](../07_errors/index.md) |")
    L.append("| お知らせ受信箱(`inbox`)メッセージ | 本書 `TPL-SYSTEM_NOTICE`([MSG-013](MSG-013.md#MSG-013))の `inbox` 生成 |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("<!-- portal-bottom -->")
    L.append("<!-- /portal-bottom -->")
    open(f"{MSG_DIR}/index.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

if __name__ == "__main__":
    build()
