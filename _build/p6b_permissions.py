#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P6b: 認証・認可設計書(07_auth-design.md)を権限の個別 ID ファイル化する。
- 06_permissions/PERM-NNN.md(ロール別操作権限。ロール×操作可否 + 対応業務UC/対応SCR/対応EVT/対応API)
- 06_permissions/index.md(ロール別操作権限一覧 + UC/画面/EVT/API↔権限 対応表 + 認可判定段・認証フロー)
移管後 07_auth-design.md は別途削除する。冪等。ルートで実行する。
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
PERM_DIR = "02_basic_design/06_permissions"
os.makedirs(PERM_DIR, exist_ok=True)

REQ = "../../01_requirements/01_specifications"   # RULE / FR / BR
ERR = "../07_errors"
API = "../03_apis"
SCR = "../01_screens"
EVT = "../02_screen_events"
UCB = "../../01_requirements/02_business_usecases"

# PERM 定義: (slug, タイトル, 要約, 本文セクション list of (h2, lead, body_md))
# 各 PERM はロール×操作可否表と対応結線(UC/SCR/EVT/API)を持つ。
# ロール: オーナー / メンバー(割当あり) / メンバー(割当なし) / 未認証 / ウィジェット利用者

PERMS = [
    {
        "title": "ユーザー種別とオーナー判定",
        "summary": "認可の起点となるユーザー種別(オーナー / メンバー / ウィジェット利用者)の判定方法と権限の表し方を定義します。",
        "lead": "認証主体は全ユーザー共通の `M_USER` で、セッション / トークンは `user_id` で `M_USER` を指します。種別は導出で判定し、オーナーは `M_CONTRACT.user_id` 一致(`isOwner`)、メンバーは `M_PRJ_USERS` の有効割当(`valid=1`)で導出します。",
        "matrix": [
            ("自契約配下の全プロジェクト操作", "可(isOwner bypass)", "—", "—", "不可", "不可"),
            ("割当プロジェクト内の全操作", "可", "可", "不可", "不可", "不可"),
            ("オーナー専有機能", "可", "不可", "不可", "不可", "不可"),
            ("ウィジェットへの質問送信", "—", "—", "—", "—", "可(公開キー)"),
        ],
        "extra": "> [!IMPORTANT]\n> **オーナー判定 = isOwner bypass を先頭に** 認可権威は `M_CONTRACT.user_id` がセッションの `user_id` と一致すること(`isOwner=true`)による bypass を最優先とし、`M_PRJ_USERS` の owner 行は一覧表示・通知宛先の網羅用で専有判定には用いません。メンバー権限は `M_PRJ_USERS` の有効割当(`valid=1`)でのみ付与されます。オーナーは役割変更・降格・譲渡なし。プロジェクト内の役割差は持ちません。",
        "rules": ["FR-013", "FR-014", "FR-016", "FR-035", "FR-186"],
        "scr": ["SCR-013"], "evt": [], "api": ["API-002"], "uc": [],
    },
    {
        "title": "認可判定の順序",
        "summary": "1 リクエストを許可するまでに通す認可判定の段(セッション → 契約状態 → オーナー判定 → 境界 → 専有 → 再認証 → 利用上限)と、各段の拒否時エラーを定義します。",
        "lead": "判定段は上から評価します。各段は拒否時に対応するエラー分類へ落とし、エラー定義の正本は [エラー設計](../07_errors/index.md) です。",
        "stage": True,
        "rules": ["FR-188", "FR-189", "FR-191"],
        "scr": [], "evt": [], "api": [], "uc": [],
    },
    {
        "title": "オーナー専有機能",
        "summary": "非オーナーに付与してはならないオーナー専有機能(課金・契約設定・プロジェクト CRUD・退会・規約再同意)と、その判定段を定義します。",
        "lead": "課金情報・支払方法・請求履歴・退会・規約再同意・契約設定、プロジェクトの作成・編集・削除はオーナー専有です。メンバーには付与しません。非オーナーが要求した場合は §認可判定の \\#8 で 403(`E-AUTHZ-OWNER-ONLY`)に落とします。",
        "matrix": [
            ("契約設定の取得・更新", "可", "不可", "不可", "不可", "不可"),
            ("支払方法の登録・更新", "可", "不可", "不可", "不可", "不可"),
            ("プロジェクトの作成・編集・削除", "可", "不可", "不可", "不可", "不可"),
            ("退会申請", "可", "不可", "不可", "不可", "不可"),
            ("規約再同意の同意 / 不同意", "可", "不可", "不可", "不可", "不可"),
            ("プロジェクト単位の上限・無料枠の変更", "可", "可(当該PJ)", "不可", "不可", "不可"),
        ],
        "extra": "> [!NOTE]\n> **上限・無料枠はメンバーも変更可** プロジェクト単位の利用上限・無料枠は、オーナーまたは当該プロジェクトのメンバーが変更できます(BR-017)。",
        "rules": ["FR-015", "BR-017"],
        "scr": ["SCR-005", "SCR-019", "SCR-028"], "evt": [],
        "api": ["API-014", "API-015", "API-017", "API-018", "API-045", "API-056"], "uc": [],
    },
    {
        "title": "オーナー保護・自己操作禁止",
        "summary": "運用が止まらないための保護制約(オーナーへの退会・停止・削除・降格・譲渡の禁止、自己操作の禁止)を定義します。",
        "lead": "オーナーに対する退会・停止・削除・降格・譲渡を一切受け付けません。自分自身の利用状態変更・削除もできません。該当操作は §認可判定の \\#9 で拒否されます。",
        "matrix": [
            ("オーナーの割当解除・降格・削除", "不可", "不可", "不可", "不可", "不可"),
            ("自分自身の割当解除・削除", "不可", "不可", "不可", "不可", "不可"),
            ("他メンバーの割当解除・削除", "可", "可(当該PJ)", "不可", "不可", "不可"),
        ],
        "extra": "> [!IMPORTANT]\n> **構造的に孤立しない** 1 契約 = 1 オーナーのためオーナーの孤立状態は構造的に発生しません。自身のアカウント削除は常に不可で、他人を経由して自身を削除する経路も設けません。拒否時は `E-AUTHZ-OWNER-PROTECTED` / `E-AUTHZ-SELF-MUTATION`。",
        "rules": ["FR-183", "FR-184"],
        "scr": ["SCR-013"], "evt": [], "api": ["API-023", "API-024"], "uc": [],
    },
    {
        "title": "オーナー境界・プロジェクト境界判定",
        "summary": "他契約・他プロジェクトのデータへ越境させない境界チェック(契約境界キー一致・プロジェクト割当)と、404 偽装による拒否を定義します。",
        "lead": "操作者の契約境界キーと対象リソースの `contract_id` の一致を要求し、非オーナーは対象プロジェクトへの割当も要求します。いずれも不一致は相手リソースの存在を漏らさないため 404 偽装で拒否します。",
        "matrix": [
            ("自契約リソースへのアクセス", "可", "可(割当PJ)", "不可(404偽装)", "不可", "不可"),
            ("他契約リソースへのアクセス", "不可(404偽装)", "不可(404偽装)", "不可(404偽装)", "不可", "不可"),
            ("割当の無いプロジェクトへの直アクセス", "可(isOwner)", "不可(404偽装)", "不可(404偽装)", "不可", "不可"),
        ],
        "extra": "> [!NOTE]\n> **メンバーは 1 オーナー固定** メールは `M_USER` で一意(1 メール = 1 アカウント)。メンバーは 1 オーナー配下に固定し、別オーナーへの重複所属は招待時に拒否します(FR-185)。拒否時は `E-AUTHZ-OWNER-BOUNDARY` / `E-AUTHZ-PROJECT-DENIED` / `E-AUTHZ-FORBIDDEN`。",
        "rules": ["FR-185", "FR-189"],
        "scr": ["SCR-013"], "evt": [], "api": ["API-018", "API-021", "API-047"], "uc": [],
    },
    {
        "title": "重要操作の再認証",
        "summary": "不可逆・高リスクな操作の直前に求める再認証(当該操作 1 回 + 15 分以内)と、対象 5 操作を定義します。",
        "lead": "ログイン済みでも、重要操作の直前に改めて本人確認(再認証)を求めます。再認証は「当該操作 1 回かつ 15 分以内」でのみ有効で、未充足のまま対象 API に到達した場合は `E-AUTH-REAUTH-REQUIRED` に落とします。",
        "matrix": [
            ("パスワード変更", "再認証必須", "再認証必須", "—", "—", "—"),
            ("退会", "再認証必須", "—", "—", "—", "—"),
            ("課金情報変更", "再認証必須", "—", "—", "—", "—"),
            ("メンバーの登録・停止・削除", "再認証必須", "再認証必須", "—", "—", "—"),
            ("月次上限件数の変更", "再認証必須", "再認証必須", "—", "—", "—"),
        ],
        "extra": "> [!IMPORTANT]\n> **対象範囲は要件で固定** 再認証の対象は上記 5 種に固定します(FR-005 / BR-002)。再認証はセッションの寿命判定(無操作 30 分 / 絶対 12 時間)とは別軸で働きます。",
        "rules": ["FR-005", "BR-002"],
        "scr": ["SCR-019"], "evt": [], "api": ["API-005", "API-012", "API-013", "API-045", "API-056"], "uc": [],
    },
    {
        "title": "セッションとログイン失敗ロックアウト",
        "summary": "セッションの寿命(無操作 30 分・絶対 12 時間)・複数デバイス同時ログイン・失効優先順位と、5 回連続失敗による 15 分ロックアウトを定義します。",
        "lead": "セッションは無操作 30 分・絶対 12 時間で失効させ、強制ログアウトを最優先に評価します。ログインが 5 回連続失敗したら当該アカウントを 15 分ロックし、ロック中の到達は `E-AUTH-LOCKED` に落とします。",
        "matrix": [
            ("複数デバイス同時ログイン", "可", "可", "—", "—", "—"),
            ("自身のアクティブセッション一覧・終了", "不可(MVP対象外)", "不可(MVP対象外)", "—", "—", "—"),
            ("ロック中のログイン", "不可(15分)", "不可(15分)", "—", "不可", "—"),
            ("ロック解除", "可", "可(当該PJ)", "—", "時間経過のみ", "—"),
        ],
        "extra": "> [!NOTE]\n> **失効の優先順位** 強制ログアウト > 絶対タイムアウト(12h) > 無操作タイムアウト(30分) > 通常セッション の順で評価します。割当変更は既存セッションを即時失効させず、次回認可チェック時(キャッシュ TTL 60 秒以内)に反映します(FR-188)。",
        "rules": ["FR-007", "FR-008", "FR-011", "FR-182", "FR-188", "BR-004", "BR-005", "BR-006"],
        "scr": ["SCR-001"], "evt": ["EVT-004"], "api": ["API-002", "API-003"], "uc": [],
    },
    {
        "title": "アカウント状態と利用可否",
        "summary": "アカウント状態(有効 / 招待中 / メール未確認 / ロック中 / 無効化)ごとのログイン可否と利用範囲を定義します。",
        "lead": "アカウント状態は §認可判定の \\#2 で評価します。招待中・メール未確認は利用を限定し、最後の割当解除による無効化では全セッション・未使用招待を失効させます。",
        "matrix": [
            ("有効", "全操作", "割当に応じた操作", "—", "—", "—"),
            ("招待中(有効化前)", "—", "—", "—", "招待リンクからの有効化のみ", "—"),
            ("メール未確認", "メール確認のみ", "メール確認のみ", "—", "—", "—"),
            ("ロック中", "不可(15分)", "不可(15分)", "—", "不可", "—"),
            ("無効化(最後の割当解除)", "—", "—", "不可", "不可", "—"),
        ],
        "extra": "> [!IMPORTANT]\n> **最後の割当解除による自動無効化** メンバーの最後の有効割当が解除されたとき、対象アカウントを自動で無効化し、全セッション・未使用招待を失効させます(FR-031 / FR-189)。一定期間(90 日)経過後にデータが消去される旨は割当解除の確認時に明示します。",
        "rules": ["FR-003", "FR-021", "FR-031", "FR-189"],
        "scr": ["SCR-018", "SCR-023"], "evt": ["EVT-151", "EVT-190"], "api": ["API-006", "API-008", "API-023"], "uc": [],
    },
    {
        "title": "契約状態によるアクセス制限",
        "summary": "契約状態(停止中 / 退会申請中 / 退会済み)ごとに管理画面で許す操作とセッションの扱いを定義します。",
        "lead": "契約状態は §認可判定の \\#4 で評価し、`suspended` / `deleted_pending` / `deleted` のときアクセスを制限します。支払方法ゲートはこの契約停止とは別経路です。",
        "matrix": [
            ("停止中(suspended): 課金・退会", "可", "不可", "—", "—", "—"),
            ("停止中(suspended): その他操作", "不可(403)", "不可(403)", "—", "—", "—"),
            ("退会申請中(deleted_pending): 参照", "可", "不可", "—", "—", "—"),
            ("退会申請中(deleted_pending): 新規書込", "不可", "不可", "—", "—", "—"),
            ("退会済み(deleted): ログイン", "不可", "不可", "—", "不可", "—"),
        ],
        "extra": "> [!NOTE]\n> **支払方法ゲートは契約停止ではない** 支払方法未登録 + 無料枠超過によるウィジェット受付停止は契約サスペンションではありません(`status` は `active` のまま)。本制限の対象外で管理画面は通常どおり利用できます。拒否時は `E-BIZ-CONTRACT-SUSPENDED` / `E-BIZ-CONTRACT-DELETED`。契約状態遷移は [課金・請求設計書](../05_billing-design.md) が正本。",
        "rules": ["FR-098"],
        "scr": [], "evt": [], "api": ["API-002", "API-037"], "uc": [],
    },
    {
        "title": "規約再同意の認可割込み",
        "summary": "規約・プライバシーポリシー改定時に、ログイン後の認可フローへ再同意画面を割り込ませる発火条件と段階適用を定義します。",
        "lead": "改定済みで未同意の文書があれば §認可判定の \\#3 で SCR-020 へ割込み、割込み中は他画面の操作を許しません。発効 30 日前に予告し、同意期限は発効日 + 14 日です。",
        "matrix": [
            ("規約再同意の同意 / 不同意", "可", "不可", "不可", "—", "—"),
            ("再同意未完了の契約での通常操作", "不可(割込み)", "不可(契約側ゲートの影響)", "—", "—", "—"),
        ],
        "extra": "> [!IMPORTANT]\n> **同意・割込みはオーナー専有** 規約再同意の同意 / 不同意操作はオーナー専有機能です(FR-015)。再同意未完了の契約に属するメンバーは、契約側の同意完了までゲートの影響を受けます。拒否時は `E-AUTHZ-TERMS`。",
        "rules": ["FR-010", "FR-015"],
        "scr": ["SCR-020"], "evt": ["EVT-135", "EVT-169"], "api": ["API-052", "API-054", "API-055"], "uc": [],
    },
    {
        "title": "critical 通知の宛先解決",
        "summary": "critical 通知を「誰に送るか」を決める宛先解決(オーナー + 当該プロジェクトの有効メンバーの 2 マスタ合算・重複排除)を定義します。",
        "lead": "宛先はオーナー(`M_CONTRACT` 由来)と当該プロジェクトの有効メンバー(`M_PRJ_USERS valid=1`)の 2 マスタを合算し、認証主体(`M_USER` の `user_id`)で重複排除します。配信契機・文面は [メッセージ設計](../08_messages/index.md) が正本です。",
        "matrix": [
            ("契約横断 critical 通知の受信", "受信(網羅)", "受信(当該PJ)", "—", "—", "—"),
            ("プロジェクト限定通知(上限アラート等)の受信", "受信(対象PJ)", "受信(対象PJのvalid=1)", "—", "—", "—"),
        ],
        "extra": "> [!NOTE]\n> **宛先解決ロジックの正本** 「誰が宛先か」を決める解決ロジックは本ページが正本です。配信契機・件名・本文テンプレートは [メッセージ設計](../08_messages/index.md) が正本です。",
        "rules": ["FR-034", "FR-185"],
        "scr": [], "evt": [], "api": ["API-021", "API-024"], "uc": [],
    },
]


def linkrule(r):
    return f"[{r}]({REQ}/{r}.md#{r})"


def linklist(items, base, fmt="{0}"):
    if not items:
        return "—"
    return " ".join(f"[{x}]({base}/{x}.md#{x})" for x in items)


STAGE_TABLE = """| \\# | 判定段 | 内容 | 拒否時のエラー |
|----|----|----|----|
| 1 | セッション検証 | 無操作 30 分 / 絶対 12 時間を満たす有効セッションか | [`E-AUTH-SESSION-EXPIRED`](../07_errors/index.md) |
| 2 | アカウント有効性 | アカウントが利用可能状態か(無効化済みなら再ログインへ誘導) | — |
| 3 | 規約再同意ゲート | 改定済みで未同意の文書があれば SCR-020 割込みへ | `E-AUTHZ-TERMS` |
| 4 | 契約状態ゲート | `suspended` / `deleted_pending` / `deleted` 時はアクセス制限を適用 | [ERR-006](../07_errors/ERR-006.md#ERR-006) 等 |
| 5 | オーナー判定(isOwner bypass) | `M_CONTRACT.user_id` 一致で自契約配下を無条件許可 | — |
| 6 | オーナー境界判定 | 非オーナーは契約境界キー一致を要求。不一致は 404 偽装 | `E-AUTHZ-OWNER-BOUNDARY` |
| 7 | プロジェクト境界判定 | 対象プロジェクトへの割当があること。割当なしは 404 偽装 | [ERR-021](../07_errors/ERR-021.md#ERR-021) / [ERR-032](../07_errors/ERR-032.md#ERR-032) |
| 8 | オーナー専有機能判定 | 専有機能を非オーナーが要求した場合は 403 | [ERR-017](../07_errors/ERR-017.md#ERR-017) |
| 9 | オーナー保護・自己操作禁止 | 不可制約に該当すれば拒否 | [ERR-023](../07_errors/ERR-023.md#ERR-023) / [ERR-024](../07_errors/ERR-024.md#ERR-024) |
| 10 | 再認証判定 | 重要操作で再認証が「当該操作 1 回 + 15 分以内」を満たすか | `E-AUTH-REAUTH-REQUIRED` |
| 11 | 利用上限判定 | 認可通過後に上限を確認(レート = 契約単位、上限・無料枠 = プロジェクト単位) | [課金・請求設計書](../05_billing-design.md) |"""


def build():
    permids = []
    for i, p in enumerate(PERMS, 1):
        pid = f"PERM-{i:03d}"
        permids.append((pid, p))
        body = []
        body.append("<!-- portal-top -->")
        body.append("<!-- /portal-top -->")
        body.append("")
        body.append(f"# <span id=\"{pid}\"></span>{pid}: {p['title']}")
        body.append("")
        body.append(f"> **このページは{p['summary']}**")
        body.append("")
        body.append("*種別 権限定義 ・ ステータス ドラフト ・ 再構成 P6b*")
        body.append("")
        body.append("## <span id=\"perm\"></span>1. ロール別操作可否")
        body.append("")
        body.append(p["lead"])
        body.append("")
        if p.get("stage"):
            body.append(STAGE_TABLE)
        else:
            body.append("| 操作 | オーナー | メンバー(割当あり) | メンバー(割当なし) | 未認証 | ウィジェット利用者 |")
            body.append("|----|----|----|----|----|----|")
            for row in p["matrix"]:
                body.append("| " + " | ".join(row) + " |")
        body.append("")
        if p.get("extra"):
            body.append(p["extra"])
            body.append("")
        body.append("## <span id=\"trace\"></span>2. 対応 UC / SCR / EVT / API")
        body.append("")
        body.append("本権限が適用される画面・イベント・API・業務ユースケースの結線です。")
        body.append("")
        body.append("| 観点 | 結線 |")
        body.append("|----|----|")
        body.append(f"| 対応業務UC | {linklist(p['uc'], UCB)} |")
        body.append(f"| 対応画面SCR | {linklist(p['scr'], SCR)} |")
        body.append(f"| 対応EVT | {linklist(p['evt'], EVT)} |")
        body.append(f"| 対応API | {linklist(p['api'], API)} |")
        body.append("")
        body.append("## <span id=\"src\"></span>3. 由来要件")
        body.append("")
        body.append("| 由来要件 |")
        body.append("|----|")
        body.append("| " + " ".join(linkrule(r) for r in p["rules"]) + " |")
        body.append("")
        body.append("---")
        body.append("")
        body.append("<!-- portal-bottom -->")
        body.append("<!-- /portal-bottom -->")
        open(f"{PERM_DIR}/{pid}.md", "w", encoding="utf-8").write("\n".join(body) + "\n")

    build_index(permids)
    print(f"PERM files: {len(permids)}")
    return permids


def build_index(permids):
    L = []
    L.append("<!-- portal-top -->")
    L.append("<!-- /portal-top -->")
    L.append("")
    L.append("# 権限設計")
    L.append("")
    L.append("> **このページは、ロール別操作権限の一覧と、UC / 画面(SCR)/ 画面イベント(EVT)/ API から権限への対応表です。** 認証主体は全ユーザー共通の `M_USER` で、オーナー(`M_CONTRACT.user_id` 一致)/ メンバー(`M_PRJ_USERS` 有効割当)を導出します。各権限ルールは `PERM-NNN.md` で個別定義し、拒否時のエラーは [エラー設計](../07_errors/index.md)、画面文言・メールは [メッセージ設計](../08_messages/index.md) を参照します。")
    L.append("")
    L.append("*ステータス ドラフト ・ 再構成 P6b*")
    L.append("")
    L.append("## <span id=\"reading\"></span>読み順")
    L.append("")
    L.append("要件定義(FR / BR / RULE)＞ 本権限設計 ＞ API設計 / エラー設計 / メッセージ設計。認可判定の各段は [PERM-002](PERM-002.md#PERM-002) を参照する。")
    L.append("")
    L.append(f"## <span id=\"list\"></span>1. ロール別操作権限一覧({len(permids)})")
    L.append("")
    L.append("権限ルールの索引です。各 PERM の定義(ロール×操作可否表・結線)は個別ファイルが正本です。ロールはオーナー / メンバー(割当あり)/ メンバー(割当なし)/ 未認証 / ウィジェット利用者の 5 区分です。")
    L.append("")
    L.append("| PERM ID | 権限ルール | 概要 | 由来要件 |")
    L.append("|----|----|----|----|")
    for pid, p in permids:
        rules = " ".join(linkrule(r) for r in p["rules"])
        L.append(f"| <span id=\"{pid}\"></span>[{pid}]({pid}.md#{pid}) | {p['title']} | {p['summary']} | {rules} |")
    L.append("")
    # 認可判定段
    L.append("## <span id=\"stages\"></span>2. 認可判定の順序(正本)")
    L.append("")
    L.append("1 リクエストを許可するまでに通す認可判定の段です。上から評価し、各段の拒否時エラーは [エラー設計](../07_errors/index.md) が正本です。詳細は [PERM-002](PERM-002.md#PERM-002)。")
    L.append("")
    L.append(STAGE_TABLE)
    L.append("")
    # UC/SCR/EVT/API ↔ 権限 対応表
    L.append("## <span id=\"trace\"></span>3. UC / 画面 / EVT / API ↔ 権限 対応表")
    L.append("")
    L.append("各権限ルールが適用される画面・イベント・API・業務ユースケースの結線一覧です。結線の無い欄は `—` とします。")
    L.append("")
    L.append("| PERM ID | 対応業務UC | 対応画面SCR | 対応EVT | 対応API |")
    L.append("|----|----|----|----|----|")
    for pid, p in permids:
        L.append(f"| [{pid}]({pid}.md#{pid}) | {linklist(p['uc'], UCB)} | {linklist(p['scr'], SCR)} | {linklist(p['evt'], EVT)} | {linklist(p['api'], API)} |")
    L.append("")
    L.append("## <span id=\"flow\"></span>4. 認証フロー(参照)")
    L.append("")
    L.append("認証(本人確認)の各フロー — ログイン / ログアウト / パスワード再設定 / 招待受諾(メンバー有効化)/ メール確認 / 強制ログアウト — のシーケンスは、各画面起点の業務ユースケース([業務ユースケース設計](../../01_requirements/02_business_usecases/index.md))のシーケンス図が正本です。本権限設計は判定段とロール別可否を正本化します。")
    L.append("")
    L.append("| 認証フロー | 主な根拠要件 | 関連 PERM |")
    L.append("|----|----|----|")
    L.append("| ログイン | [FR-001](../../01_requirements/01_specifications/FR-001.md#FR-001) | [PERM-007](PERM-007.md#PERM-007) |")
    L.append("| ログイン失敗ロックアウト | [RULE-001](../../01_requirements/01_specifications/RULE-001.md#RULE-001) | [PERM-007](PERM-007.md#PERM-007) |")
    L.append("| パスワード再設定 | [RULE-003](../../01_requirements/01_specifications/RULE-003.md#RULE-003) | [PERM-008](PERM-008.md#PERM-008) |")
    L.append("| 招待受諾(メンバー有効化) | [RULE-007](../../01_requirements/01_specifications/RULE-007.md#RULE-007) | [PERM-008](PERM-008.md#PERM-008) |")
    L.append("| メール確認 | [FR-003](../../01_requirements/01_specifications/FR-003.md#FR-003) | [PERM-008](PERM-008.md#PERM-008) |")
    L.append("| 強制ログアウト(契約停止時) | [RULE-016](../../01_requirements/01_specifications/RULE-016.md#RULE-016) | [PERM-007](PERM-007.md#PERM-007) [PERM-009](PERM-009.md#PERM-009) |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("<!-- portal-bottom -->")
    L.append("<!-- /portal-bottom -->")
    open(f"{PERM_DIR}/index.md", "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    build()
