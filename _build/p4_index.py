#!/usr/bin/env python3
"""P4 API index generator.

Builds 02_basic_design/03_apis/index.md:
  - 方針 + 共通仕様 (conv anchor; folds key tables from the former API-common.md)
  - API 一覧(機能グループ別)
  - API <-> UC / EVT / TBL 対応表
  - 読み順

Deterministic. Reads each generated API-<NNN>.md for metadata and
_build/p4_reverse.json for結線.
"""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APIDIR = os.path.join(ROOT, '02_basic_design/03_apis')
apimap = json.load(open(os.path.join(ROOT, '99_management/crosswalk.json'), encoding='utf-8'))['apimap']
rev = json.load(open(os.path.join(ROOT, '_build/p4_reverse.json'), encoding='utf-8'))
old_by_new = {v: k for k, v in apimap.items()}

# Functional groups: (title, lead, [new ids...]) — order follows crosswalk.
GROUPS = [
    ("認証・セッション", "サインアップ / ログイン / 再認証 / メール確認 / 招待 / プロフィール / 契約設定。",
     [f"API-{i:03d}" for i in range(1, 16)]),
    ("プロジェクト", "プロジェクト CRUD とウィジェット鍵ローテーション。",
     [f"API-{i:03d}" for i in range(16, 20)]),
    ("メンバー", "プロジェクト単位のメンバー招待 / 情報更新 / 離脱 / 再送。",
     [f"API-{i:03d}" for i in range(20, 25)]),
    ("FAQ", "FAQ の CRUD・一括状態変更・CSV 入出力・全文検索・質問ログ検索。",
     [f"API-{i:03d}" for i in range(25, 34)]),
    ("未解決質問", "未解決質問の一覧・詳細・状況切替・CSV エクスポート。",
     [f"API-{i:03d}" for i in range(34, 37)]),
    ("ウィジェット配信", "エンドユーザー向けウィジェットの bootstrap / ask / 問い合わせ。",
     [f"API-{i:03d}" for i in range(37, 40)]),
    ("ダッシュボード", "概要画面向けの集計サマリー。",
     ["API-040"]),
    ("利用量・課金", "利用量・請求サマリー・請求書・支払方法・上限設定。",
     [f"API-{i:03d}" for i in range(41, 48)]),
    ("お知らせ受信箱", "受信箱の取得・既読化・未読件数。",
     [f"API-{i:03d}" for i in range(48, 52)]),
    ("規約・退会", "規約 / プライバシー取得・同意・退会申請。",
     [f"API-{i:03d}" for i in range(52, 57)]),
    ("AI 推論 IF", "AI 推論連携インターフェース(外部 LLM)。",
     ["API-057"]),
    ("メール配信 IF", "トランザクションメール送信インターフェース。",
     ["API-058"]),
    ("外部 Webhook", "メール配信プロバイダ(Resend)からの Webhook 受信。",
     ["API-059"]),
]


def meta(new_id):
    text = open(os.path.join(APIDIR, f'{new_id}.md'), encoding='utf-8').read()
    def row(label):
        m = re.search(r'\|\s*' + re.escape(label) + r'\s*\|\s*(.*?)\s*\|', text)
        return m.group(1) if m else '—'
    name = row('API名')
    endpoint = row('エンドポイント').strip('`').strip()
    method = row('HTTPメソッド')
    authz = row('認可')
    # 利用テーブル names
    tbls = re.findall(r'\[`([A-Z_]+)`\]\(\.\./04_database/', text)
    return {"name": name, "endpoint": endpoint, "method": method,
            "authz": authz, "tbls": tbls}


def main():
    out = []
    out.append('<!-- portal-top -->')
    out.append('[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ **API設計**')
    out.append('<!-- /portal-top -->\n')
    out.append('# API 設計書\n')
    out.append('> **このページは、メインシステムが提供する全 59 エンドポイントの REST / 内部 IF API を、'
               '1 エンドポイント = 1 ファイル(`API-001` 〜 `API-059`)でフラット採番し索引する設計書です。** '
               '各 API の詳細は個別ページ(基本情報 / 処理概要 / リクエスト / レスポンス / バリデーション / エラー / 利用テーブル)に展開しています。\n')
    out.append('*版数 v3.0 ・ 更新 2026-06-21 ・ API数 59 ・ 再構成 P4*\n')

    # 0. 方針 + 共通仕様
    out.append('## <span id="conv"></span>0. API 設計の方針・共通仕様\n')
    out.append('全 API に共通する基本ルール・認証ヘッダ・エラー体系を定義します。各 API ページは本節を前提とし、差分のみを各ページに記載します。\n')
    out.append('### <span id="conv-policy"></span>0.1 方針\n')
    out.append('| 観点 | 方針 |')
    out.append('|---|---|')
    out.append('| ベースパス | `/api/v1` 配下に統一(ウィジェット系は `/widget/v1`) |')
    out.append('| データ形式 | JSON。日時は ISO 8601 + 末尾 Z(UTC)。ID は ULID(26 文字、Stripe ID 例外) |')
    out.append('| 認証方式 | 管理 API は Cookie セッション、更新系は CSRF トークン併用。ウィジェットは公開鍵 + ドメイン検証 |')
    out.append('| ページング | カーソル方式に統一(`cursor` / `limit` 50〜200、末尾 `nextCursor=null`) |')
    out.append('| エラー応答 | RFC 7807(`application/problem+json`)。`E-AUTH-*` / `E-AUTHZ-*` / `E-BIZ-*` / `E-INPUT-*` の ID 体系 |')
    out.append('| オーナー境界 | 全 API で `contract_id` による契約分離を強制。違反時は 404 偽装で存在を秘匿 |')
    out.append('| 冪等性 | 書き込み系 API は `Idempotency-Key` ヘッダ(ULID 推奨、24h 保管)を受け付ける |')
    out.append('| 論理削除 | `valid` カラムを持つテーブルへの GET 系は `WHERE valid=1` を強制(監査ログは対象外) |')
    out.append('')
    out.append('### <span id="conv-headers"></span>0.2 認証ヘッダ\n')
    out.append('| ヘッダ | 用途 | 例 |')
    out.append('|---|---|---|')
    out.append('| `Cookie: session=<token>` | 利用者セッション | 管理 API |')
    out.append('| `Authorization: Bearer <wst_*>` | ウィジェットセッション | ウィジェット API |')
    out.append('| `X-CSRF-Token: <token>` | CSRF 対策 | 状態変更系 |')
    out.append('| `Idempotency-Key: <ULID>` | 冪等性 | 書き込み系 |')
    out.append('')
    out.append('> [!NOTE]')
    out.append('> **レート制限・キャパシティ** API 層の警告 / 拒否レベルと超過時の挙動は、'
               '業務正本である [課金・請求設計書](../05_billing-design.md) と各 FR / NFR を参照する'
               '(FAQ 件数 / 月間質問数 / 公開 API レート / ログイン失敗ロック 等)。\n')

    # 1. API 一覧(機能グループ別)
    out.append('## <span id="list"></span>1. API 一覧(機能グループ別)\n')
    out.append(f'全 59 エンドポイントを {len(GROUPS)} 機能グループに整理します。API ID から個別ページへ移動します。\n')
    gi = 0
    for title, lead, ids in GROUPS:
        gi += 1
        out.append(f'### <span id="g-{gi}"></span>1.{gi} {title}\n')
        out.append(lead + '\n')
        out.append('| API ID | API / エンドポイント | 認可 | 利用テーブル |')
        out.append('|---|---|---|---|')
        for nid in ids:
            m = meta(nid)
            ep = ''
            if m['method'] != '—' or m['endpoint'] != '—':
                ep = f" {m['method']} `{m['endpoint']}`" if m['endpoint'] != '—' else ''
            tbls = ' '.join(f'`{t}`' for t in m['tbls']) if m['tbls'] else '—'
            out.append(f"| <span id=\"{nid}\"></span>[`{nid}`]({nid}.md#{nid}) | **{m['name']}**{ep} | {m['authz']} | {tbls} |")
        out.append('')

    # 2. API <-> UC / EVT / TBL 対応表
    out.append('## <span id="trace"></span>2. API ↔ UC / EVT / TBL 対応表\n')
    out.append('各 API を呼び出す画面イベント(EVT)・業務ユースケース(UC)と、参照・更新するテーブル(TBL)の結線一覧です。'
               'EVT・UC から逆引きできない API は MVP では画面イベント層に直接の呼び出しを持たない(内部 / 検索系)ことを示します。\n')
    out.append('| API ID | API名 | 対応EVT | 対応UC | 利用テーブル |')
    out.append('|---|---|---|---|---|')
    for i in range(1, 60):
        nid = f'API-{i:03d}'
        old = old_by_new[nid]
        m = meta(nid)
        r = rev.get(old, {"evts": [], "ucs": [], "scrs": []})
        evts = ' '.join(f'[{e}](../02_screen_events/{e}.md#{e})' for e in r['evts']) if r['evts'] else '—'
        ucs = ' '.join(f'[{u}](../../01_requirements/02_business_usecases/{u}.md#{u})' for u in r['ucs']) if r['ucs'] else '—'
        tbls = ' '.join(f'`{t}`' for t in m['tbls']) if m['tbls'] else '—'
        out.append(f"| [`{nid}`]({nid}.md#{nid}) | {m['name']} | {evts} | {ucs} | {tbls} |")
    out.append('')

    # 3. 読み順
    out.append('## <span id="reading"></span>3. 読み順\n')
    out.append('1. 本ページ §0 で共通仕様(認証ヘッダ・エラー体系・境界判定)を把握する。')
    out.append('2. §1 の機能グループ一覧で対象 API を特定し、API ID から個別ページへ移動する。')
    out.append('3. 個別ページの「項目」表で対応画面・対応UC・対応EVT をたどり、画面設計 / ユースケース設計と縦串で確認する。')
    out.append('4. §2 の対応表で API ↔ EVT / UC / TBL の結線を俯瞰する。')
    out.append('')

    out.append('---\n')
    out.append('<!-- portal-bottom -->')
    out.append('[基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)')
    out.append('<!-- /portal-bottom -->')

    open(os.path.join(APIDIR, 'index.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print('wrote index.md')


if __name__ == '__main__':
    main()
