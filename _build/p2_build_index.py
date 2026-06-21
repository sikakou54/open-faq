#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2: 業務ユースケース index.md(アクター別索引 + UC一覧 + 要件↔UC対応表)を生成する。
入力: 生成済み UC-NNN.md / uc_crosswalk.json。決定論的。
"""
import glob, re, os, json

BIZUC = "01_requirements/02_business_usecases"


def load_ucs():
    """新 UC-NNN ごとに (uc, name, old_id, kind, primary_scr_or_sys) を返す。"""
    rows = []
    files = sorted(
        glob.glob(f"{BIZUC}/UC-[0-9][0-9][0-9].md"),
        key=lambda p: int(re.search(r"UC-(\d+)", os.path.basename(p)).group(1)),
    )
    for f in files:
        s = open(f, encoding="utf-8").read()
        uc = re.search(r'# <span id="(UC-\d+)"', s).group(1)
        name = re.search(r"業務ユースケース名 \| (.+?) \|", s).group(1)
        remark = re.search(r"## 備考\n\n(.+)", s).group(1)
        old = re.search(r"旧 `([^`]+)`", remark).group(1)
        if old.startswith("UC-SYSTEM"):
            kind = "system"
            key = old  # UC-SYSTEM-0nn
        else:
            kind = "screen"
            key = re.search(r"UC-(SCR-[A-Z0-9-]+?)-EV\d+$", old).group(1)  # SCR-xxx
        frs = re.findall(r"FR-\d+", re.search(r"対応要件ID \| (.+?) \|", s).group(1))
        rows.append(dict(uc=uc, name=name, old=old, kind=kind, key=key, frs=frs))
    return rows


def scr_anchor(scr):
    return "WIDGET" if scr == "SCR-WIDGET" else scr


def scr_link(scr):
    return f"[{scr}](../../02_basic_design/01_screens/{scr}.md#{scr_anchor(scr)})"


def uc_link(uc):
    return f"[{uc}]({uc}.md#{uc})"


def uc_range(ucs):
    """連続 UC のリストを 'UC-001〜UC-006' 等に圧縮(リンク無しの表示用)。"""
    if not ucs:
        return "—"
    nums = sorted(int(u.split("-")[1]) for u in ucs)
    parts = []
    start = prev = nums[0]
    for n in nums[1:]:
        if n == prev + 1:
            prev = n
            continue
        parts.append((start, prev))
        start = prev = n
    parts.append((start, prev))
    out = []
    for a, b in parts:
        if a == b:
            out.append(f"[UC-{a:03d}](UC-{a:03d}.md#UC-{a:03d})")
        else:
            out.append(f"UC-{a:03d}〜UC-{b:03d}")
    return " ・ ".join(out)


# 画面のワークスペース分類(現行 index 準拠)
WS = [
    ("ws-auth", "認証・規約フロー",
     ["SCR-001", "SCR-002", "SCR-003", "SCR-013", "SCR-015", "SCR-018", "SCR-019"]),
    ("ws-owner", "契約ワークスペース",
     ["SCR-004", "SCR-004-001", "SCR-014", "SCR-016", "SCR-022", "SCR-023"]),
    ("ws-project", "プロジェクトワークスペース",
     ["SCR-005", "SCR-005-001", "SCR-006", "SCR-006-001", "SCR-006-002",
      "SCR-007", "SCR-008", "SCR-009", "SCR-009-001", "SCR-021", "SCR-021-001"]),
    ("ws-common", "共通領域",
     ["SCR-010", "SCR-011", "SCR-012", "SCR-017", "SCR-020"]),
    ("ws-widget", "ウィジェット", ["SCR-WIDGET"]),
]

SCR_NAMES = {
    "SCR-001": "ログイン", "SCR-002": "アカウント登録", "SCR-003": "パスワード再設定",
    "SCR-013": "メール確認", "SCR-015": "規約再同意割込み",
    "SCR-018": "メンバーアカウント有効化", "SCR-019": "プロジェクト連絡先メール確認完了",
    "SCR-004": "プロジェクト", "SCR-004-001": "プロジェクト作成・編集モーダル",
    "SCR-014": "退会申請", "SCR-016": "利用状況", "SCR-022": "請求", "SCR-023": "設定",
    "SCR-005": "要対応の質問一覧", "SCR-005-001": "要対応の質問詳細",
    "SCR-006": "FAQ 一覧", "SCR-006-001": "FAQ 編集",
    "SCR-006-002": "FAQ CSV インポートモーダル", "SCR-007": "ウィジェット設定",
    "SCR-008": "概要(プロジェクト)", "SCR-009": "メンバー(プロジェクト)",
    "SCR-009-001": "メンバー招待 / 編集モーダル", "SCR-021": "利用量と上限(プロジェクト単位)",
    "SCR-021-001": "質問数上限設定モーダル", "SCR-010": "利用規約閲覧",
    "SCR-011": "お知らせ一覧", "SCR-012": "お知らせ詳細", "SCR-017": "個人設定",
    "SCR-020": "プライバシーポリシー閲覧", "SCR-WIDGET": "エンドユーザー向け FAQ ウィジェット",
}

# システム UC: トリガー種別 / 機能グループ(現行 index 準拠)
SYS_META = {
    "UC-SYSTEM-001": ("非同期ジョブ", "FR17 インポート・エクスポート"),
    "UC-SYSTEM-002": ("Webhook 受信", "FR11 通知"),
    "UC-SYSTEM-003": ("定期バッチ", "FR13 プライバシー・データ管理"),
    "UC-SYSTEM-004": ("定期バッチ(月次)", "FR09 利用量・課金"),
    "UC-SYSTEM-005": ("スケジュール/イベント", "FR15 お知らせ"),
    "UC-SYSTEM-006": ("イベントドリブン", "FR11 通知"),
    "UC-SYSTEM-007": ("イベントドリブン", "FR02 ユーザー管理"),
    "UC-SYSTEM-008": ("イベントドリブン", "FR09 利用量・課金"),
    "UC-SYSTEM-009": ("定期バッチ(失敗検出)", "FR11 通知"),
    "UC-SYSTEM-010": ("同期内部処理", "FR09 / FR10"),
    "UC-SYSTEM-011": ("同期内部処理", "FR09 / FR12"),
    "UC-SYSTEM-012": ("イベント+定期", "FR09 利用量・課金"),
    "UC-SYSTEM-013": ("定期/検証時", "FR01 / FR14"),
    "UC-SYSTEM-014": ("イベント+時間", "FR14 セキュリティ"),
    "UC-SYSTEM-015": ("イベント(状態遷移)", "FR01 / FR14"),
    "UC-SYSTEM-016": ("イベント", "FR20 AI 推論動作"),
    "UC-SYSTEM-017": ("定期/集約", "FR11 / FR15"),
    "UC-SYSTEM-018": ("定期バッチ(日次)", "NFR(監査)"),
}

# アクター別 業務目的 -> 関連画面 / 関連システムUC(現行 UC-BIZ 準拠)
ACTORS = [
    ("act-account", "アカウント利用者(共通)", [
        ("サービスにアクセスする(ログイン・規約同意)",
         ["SCR-001", "SCR-003", "SCR-015"], ["UC-SYSTEM-013", "UC-SYSTEM-014"]),
        ("アカウント設定と通知を管理する",
         ["SCR-010", "SCR-011", "SCR-012", "SCR-013", "SCR-017", "SCR-020"], []),
    ]),
    ("act-owner", "契約オーナー", [
        ("サービス利用を開始する(契約開設・本人確認)",
         ["SCR-002", "SCR-013", "SCR-019"], []),
        ("FAQ 提供基盤を構築する(プロジェクト・ウィジェット設置)",
         ["SCR-004", "SCR-004-001", "SCR-007", "SCR-008"], []),
        ("チームを編成して共同運用する(メンバー招待・権限)",
         ["SCR-009", "SCR-009-001", "SCR-018"], ["UC-SYSTEM-007"]),
        ("利用量と費用を管理する(利用状況・上限・請求)",
         ["SCR-016", "SCR-021", "SCR-021-001", "SCR-022"],
         ["UC-SYSTEM-004", "UC-SYSTEM-008", "UC-SYSTEM-010", "UC-SYSTEM-011", "UC-SYSTEM-012"]),
        ("サービス利用を終了する(退会・データ消去)",
         ["SCR-014", "SCR-023"], ["UC-SYSTEM-003"]),
    ]),
    ("act-member", "プロジェクトメンバー", [
        ("FAQ を整備して公開する(作成・編集・一括・CSV)",
         ["SCR-006", "SCR-006-001", "SCR-006-002"], ["UC-SYSTEM-001"]),
        ("問い合わせから FAQ を改善する(未解決→FAQ化)",
         ["SCR-005", "SCR-005-001", "SCR-006-001"], []),
        ("ウィジェットの応答を最適化する(設定・しきい値・許可ドメイン)",
         ["SCR-004", "SCR-007", "SCR-021-001"], ["UC-SYSTEM-016"]),
    ]),
    ("act-widget", "ウィジェット利用者", [
        ("疑問をその場で自己解決する", ["SCR-WIDGET"], ["UC-SYSTEM-011"]),
    ]),
    ("act-ops", "運営", [
        ("利用者へ重要連絡を届ける(お知らせ配信・通知・再送)",
         ["SCR-011", "SCR-012"],
         ["UC-SYSTEM-002", "UC-SYSTEM-005", "UC-SYSTEM-006", "UC-SYSTEM-009", "UC-SYSTEM-017"]),
        ("データ保護と健全性を維持する(削除・監査・アクセス制御)",
         [], ["UC-SYSTEM-003", "UC-SYSTEM-012", "UC-SYSTEM-013",
              "UC-SYSTEM-014", "UC-SYSTEM-015", "UC-SYSTEM-018"]),
    ]),
]

# 機能グループ別トレーサビリティ(現行 index §4 準拠: 画面 / システム の旧キー)
TRACE = [
    ("FR01 アカウント管理", ["SCR-001", "SCR-002", "SCR-003", "SCR-013", "SCR-014", "SCR-023"],
     ["UC-SYSTEM-003", "UC-SYSTEM-013", "UC-SYSTEM-015"]),
    ("FR02 ユーザー管理", ["SCR-009", "SCR-009-001", "SCR-018"], ["UC-SYSTEM-007"]),
    ("FR03 プロジェクト管理", ["SCR-004", "SCR-004-001"], []),
    ("FR04 FAQ 管理", ["SCR-006", "SCR-006-001"], []),
    ("FR05 AI 回答", ["SCR-WIDGET"], ["UC-SYSTEM-016"]),
    ("FR06 未解決質問登録", ["SCR-WIDGET", "SCR-005", "SCR-005-001"], []),
    ("FR07 未解決質問から FAQ 登録", ["SCR-005-001", "SCR-006-001"], []),
    ("FR08 処理エラー", [], ["UC-SYSTEM-009"]),
    ("FR09 利用量・課金", ["SCR-016", "SCR-021", "SCR-021-001", "SCR-022"],
     ["UC-SYSTEM-004", "UC-SYSTEM-008", "UC-SYSTEM-010", "UC-SYSTEM-011", "UC-SYSTEM-012"]),
    ("FR10 管理ダッシュボード", ["SCR-008", "SCR-016"], ["UC-SYSTEM-010"]),
    ("FR11 通知", ["SCR-011", "SCR-012"],
     ["UC-SYSTEM-002", "UC-SYSTEM-006", "UC-SYSTEM-007", "UC-SYSTEM-009", "UC-SYSTEM-017"]),
    ("FR12 ウィジェット", ["SCR-007", "SCR-WIDGET"], ["UC-SYSTEM-011"]),
    ("FR13 プライバシー・データ管理", ["SCR-014", "SCR-017", "SCR-020"], ["UC-SYSTEM-003"]),
    ("FR14 セキュリティ", ["SCR-001"], ["UC-SYSTEM-013", "UC-SYSTEM-014", "UC-SYSTEM-015"]),
    ("FR15 お知らせ", ["SCR-010", "SCR-011", "SCR-012", "SCR-020"],
     ["UC-SYSTEM-005", "UC-SYSTEM-017"]),
    ("FR16 検索エンジン・全文検索", ["SCR-005", "SCR-006"], []),
    ("FR17 インポート・エクスポート", ["SCR-006", "SCR-006-002"], ["UC-SYSTEM-001"]),
    ("FR18 UX 細部・データ運用", ["SCR-006", "SCR-006-001"], []),
    ("FR19 アクセス制御細部", ["SCR-007", "SCR-009-001", "SCR-021"], ["UC-SYSTEM-015"]),
    ("FR20 AI 推論動作", ["SCR-WIDGET"], ["UC-SYSTEM-016"]),
    ("FR21 画面・機能要件一覧", ["__ALL__"], []),
]


def main():
    rows = load_ucs()
    by_scr = {}
    by_sys = {}
    for r in rows:
        if r["kind"] == "screen":
            by_scr.setdefault(r["key"], []).append(r["uc"])
        else:
            by_sys[r["old"]] = r["uc"]

    L = []
    L.append("# 業務ユースケース一覧")
    L.append("")
    L.append(
        "> **このページは、操作粒度の業務ユースケース(UC-001〜)を一元的に索引する正本カタログです。** 各 UC は「1 画面イベント = 1 UC」または「1 システム処理 = 1 UC」の操作粒度で、`UC-NNN.md`(1 UC = 1 ファイル・フラット連番)に定義します。"
    )
    L.append("")
    n_scr = sum(len(v) for v in by_scr.values())
    n_sys = len(by_sys)
    L.append(
        f"*版数 v1.0 ・ 更新 2026-06-21 ・ 総数 {len(rows)}(画面起点 {n_scr} ・ システム起点 {n_sys})・ ステータス ドラフト ・ 再構成 P2*"
    )
    L.append("")
    L.append("> [!NOTE]")
    L.append(
        f"> **採番** 画面順(自然順)×イベント順で UC-001〜UC-{n_scr:03d}、続いてシステム起点を UC-{n_scr+1:03d}〜UC-{len(rows):03d} に割り当てます(ゼロ詰め3桁・欠番なし)。旧 ID(`UC-SCR-*-EV*` / `UC-SYSTEM-*`)との対応は `99_management/uc_crosswalk.json` を正本とします。下流の画面・API・テーブル ID(`SCR-*` / `API-*` / `TBL-*`)は現行のままで、後続フェーズ(P3〜P5)でリナンバします。画面イベント ID(`EVT-*`)は P3 で付与します。"
    )
    L.append("")

    # アクター別索引
    L.append('## <span id="actors"></span>1. アクター別索引')
    L.append("")
    L.append(
        "アクター(役割)が達成する業務目的ごとに、対応する操作粒度 UC(UC-NNN)群へリンクします。業務目的の単位は、旧業務ユースケース(UC-BIZ)の括りを踏襲します。"
    )
    L.append("")
    for aid, aname, goals in ACTORS:
        L.append(f'### <span id="{aid}"></span>{aname}')
        L.append("")
        L.append("| 業務目的 | 対応する操作粒度 UC |")
        L.append("|---|---|")
        for goal, scrs, syss in goals:
            ucs = []
            for s in scrs:
                ucs += by_scr.get(s, [])
            for sy in syss:
                if sy in by_sys:
                    ucs.append(by_sys[sy])
            L.append(f"| {goal} | {uc_range(ucs)} |")
        L.append("")

    # 画面起点 UC 一覧
    L.append('## <span id="screen"></span>2. 画面起点ユースケース(画面別)')
    L.append("")
    L.append(
        "全 30 画面の画面イベントを操作粒度 UC として索引します。各画面の UC は当該画面の `EV-xx` と 1 対 1 で対応します(現行 EV 番号は各 UC の備考・関連欄に注記)。"
    )
    L.append("")
    for wid, wname, scrs in WS:
        L.append(f'### <span id="{wid}"></span>{wname}')
        L.append("")
        L.append("| 画面 | 画面名 | UC 数 | 操作粒度 UC |")
        L.append("|---|---|---|---|")
        for scr in scrs:
            ucs = by_scr.get(scr, [])
            L.append(
                f"| {scr_link(scr)} | {SCR_NAMES.get(scr, scr)} | {len(ucs)} | {uc_range(ucs)} |"
            )
        L.append("")

    # システム起点 UC 一覧
    L.append('## <span id="system"></span>3. システム起点ユースケース')
    L.append("")
    L.append(
        "画面操作を伴わず、定期・イベント駆動・非同期・Webhook 受信で実行する処理です。1 処理 = 1 UC で索引します。"
    )
    L.append("")
    L.append("| UC | 名称 | トリガー種別 | 関連(機能グループ) |")
    L.append("|---|---|---|---|")
    for r in rows:
        if r["kind"] != "system":
            continue
        trg, grp = SYS_META.get(r["old"], ("—", "—"))
        L.append(f"| {uc_link(r['uc'])} | {r['name']} | {trg} | {grp} |")
    L.append("")

    # 要件トレーサビリティ
    L.append('## <span id="trace"></span>4. 要件トレーサビリティ(機能グループ別)')
    L.append("")
    L.append(
        "各機能要件グループ(FR01〜FR21)が、少なくとも 1 つ以上の操作粒度 UC に対応していることを示します。UC は新フラット ID(UC-NNN)で表記します。"
    )
    L.append("")
    L.append("| 機能グループ | 対応する画面起点 UC | 対応するシステム起点 UC |")
    L.append("|---|---|---|")
    for grp, scrs, syss in TRACE:
        if scrs == ["__ALL__"]:
            scr_cell = f"全 30 画面の UC 群(本 §2 ・ UC-001〜UC-{n_scr:03d})"
        else:
            ucs = []
            for s in scrs:
                ucs += by_scr.get(s, [])
            scr_cell = uc_range(ucs) if ucs else "—"
        sys_ucs = [by_sys[sy] for sy in syss if sy in by_sys]
        sys_cell = " ・ ".join(uc_link(u) for u in sys_ucs) if sys_ucs else "—"
        L.append(f"| {grp} | {scr_cell} | {sys_cell} |")
    L.append("")
    L.append("> [!NOTE]")
    L.append(
        f"> **監査・整合性** 監査ログの整合性検証(NFR 監査要件)は {uc_link(by_sys['UC-SYSTEM-018'])}(旧 UC-SYSTEM-018)が担います。各操作の監査記録は対応する画面起点・システム起点 UC の事後条件に記載します。"
    )
    L.append("")

    open(f"{BIZUC}/index.md", "w", encoding="utf-8").write("\n".join(L))
    print("index.md generated")

    fix_basic_design_index()


# UC-BIZ-NNN -> (業務目的ラベル, アクター索引アンカー)。基本設計 index の UC 列リライト用。
BIZ_REMAP = {
    "UC-BIZ-001": ("サービスにアクセスする", "act-account"),
    "UC-BIZ-002": ("アカウント設定と通知を管理する", "act-account"),
    "UC-BIZ-003": ("サービス利用を開始する", "act-owner"),
    "UC-BIZ-004": ("FAQ 提供基盤を構築する", "act-owner"),
    "UC-BIZ-005": ("チームを編成して共同運用する", "act-owner"),
    "UC-BIZ-006": ("利用量と費用を管理する", "act-owner"),
    "UC-BIZ-007": ("サービス利用を終了する", "act-owner"),
    "UC-BIZ-008": ("FAQ を整備して公開する", "act-member"),
    "UC-BIZ-009": ("問い合わせから FAQ を改善する", "act-member"),
    "UC-BIZ-010": ("ウィジェットの応答を最適化する", "act-member"),
    "UC-BIZ-011": ("疑問をその場で自己解決する", "act-widget"),
    "UC-BIZ-012": ("利用者へ重要連絡を届ける", "act-ops"),
    "UC-BIZ-013": ("データ保護と健全性を維持する", "act-ops"),
}


def fix_basic_design_index():
    """02_basic_design/index.md の UC 列に残る旧 UC-BIZ リンクを、
    新しい業務ユースケース index(アクター別索引)へリライトする(決定論)。"""
    p = "02_basic_design/index.md"
    if not os.path.exists(p):
        return
    s = open(p, encoding="utf-8").read()
    pat = re.compile(
        r"\[UC-BIZ-(\d+)\]\(\.\./01_requirements/02_business_usecases/UC-BIZ-\d+\.md(?:#UC-BIZ-\d+)?\)"
    )

    def repl(m):
        bid = f"UC-BIZ-{m.group(1)}"
        label, anchor = BIZ_REMAP.get(bid, (bid, "actors"))
        return f"[{label}](../01_requirements/02_business_usecases/index.md#{anchor})"

    ns = pat.sub(repl, s)
    if ns != s:
        open(p, "w", encoding="utf-8").write(ns)
        print("02_basic_design/index.md UC column rewritten")


if __name__ == "__main__":
    main()
