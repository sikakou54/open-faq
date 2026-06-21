<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ **DB設計**
<!-- /portal-top -->

# データベース設計書

**メインシステムのデータベース(Cloudflare D1 / SQLite)全 31 テーブルを機能ドメイン別に定義する設計書です。** 全ユーザーは `M_USER`、契約は `M_CONTRACT`(オーナー判定 + プロジェクトの親)で管理します。各テーブルの詳細はテーブル名のリンクから辿れます。

*版数 v3.6 ・ 更新 2026-06-21 ・ テーブル数 31 ・ 独立設計書*

## <span id="store"></span>1.データストア構成

<div class="card-grid cols-3">
<div class="card"><div class="lead-ico">D1</div><h4>Cloudflare D1(SQLite)</h4><p>全 31 テーブル。契約境界は <code>contract_id</code>(<code>M_CONTRACT.id</code>)で表す。</p></div>
<div class="card"><div class="lead-ico">KV</div><h4>Workers KV</h4><p>セッション / トークン / レート制限のキャッシュ。</p></div>
<div class="card"><div class="lead-ico">R2</div><h4>R2 オブジェクト</h4><p>CSV 添付・ウィジェット静的アセット。</p></div>
</div>

## <span id="map"></span>2.テーブル一覧

全 31 テーブルを 7 ドメインに分類しています。テーブル名は個別ページ(概要 / カラム定義 / インデックス / コード値)へのリンクです。

#### 認証・アカウント・契約 (7)

全ユーザーの認証(M_USER)、契約とオーナー判定(M_CONTRACT)、プロジェクトメンバー割当、セッション・トークン・規約。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-M-001"></span>[`M_USER`](TBL-M-001.md) | ユーザーマスタ | マスタ | オーナー・メンバーを含む全ユーザーの認証情報を一元保持。 |
| <span id="TBL-M-002"></span>[`M_CONTRACT`](TBL-M-002.md) | 契約マスタ | マスタ | 契約を管理。id が契約境界キー、user_id でオーナーを判定。プロジェクトの親。 |
| <span id="TBL-M-003"></span>[`M_PRJ_USERS`](TBL-M-003.md) | プロジェクトメンバー(割当) | マスタ | ユーザーをプロジェクトへ割り当て(役割差は持たない)。 |
| <span id="TBL-T-001"></span>[`T_SESSIONS`](TBL-T-001.md) | セッション | トランザクション | 複数デバイス対応のログインセッション。 |
| <span id="TBL-T-002"></span>[`T_ACCESS_TOKENS`](TBL-T-002.md) | アクセストークン | トランザクション | 招待・パスワード再設定・メール確認などの短期トークン。 |
| <span id="TBL-M-012"></span>[`M_TERMS_VER`](TBL-M-012.md) | 規約版数 | マスタ | 利用規約・プライバシーポリシーの版。 |
| <span id="TBL-T-012"></span>[`T_TERMS_AGREE`](TBL-T-012.md) | 規約同意 | トランザクション | 利用者ごとの規約同意履歴。 |

#### プロジェクト・ウィジェット (3)

FAQ プロジェクト本体(契約の子)、許可ドメイン、ウィジェット鍵。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-M-004"></span>[`M_PROJECTS`](TBL-M-004.md) | プロジェクト | マスタ | FAQ プロジェクトとウィジェット設定。契約(M_CONTRACT)の子テーブル。 |
| <span id="TBL-M-005"></span>[`M_ALLOWED_DOMAINS`](TBL-M-005.md) | 許可ドメイン | マスタ | ウィジェット埋め込みを許可するドメイン。 |
| <span id="TBL-T-003"></span>[`T_PRJ_LEGACY_KEYS`](TBL-T-003.md) | レガシー API キー | トランザクション | 鍵ローテーション時に旧キーを 24 時間だけ有効化。 |

#### FAQ・質問・未解決 (6)

FAQ 本体と全文検索、質問ログ、参照 FAQ、未解決質問、FAQ 化履歴。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-M-006"></span>[`M_FAQS`](TBL-M-006.md) | FAQ | マスタ | FAQ 本体(質問・回答・公開状態)。契約境界は project_id で導出。 |
| <span id="TBL-TP-001"></span>[`TP_FAQ_FTS`](TBL-TP-001.md) | FAQ 全文検索 | ワーク | FTS5 仮想テーブル(trigram)。 |
| <span id="TBL-H-001"></span>[`H_QUESTION_LOGS`](TBL-H-001.md) | 質問ログ | 履歴 | ウィジェット利用者の質問と AI 推論結果。 |
| <span id="TBL-T-004"></span>[`T_QLOG_FAQ_REFS`](TBL-T-004.md) | 参照 FAQ(M:N) | トランザクション | 質問ログと参照 FAQ の中間テーブル。 |
| <span id="TBL-T-005"></span>[`T_INQUIRIES`](TBL-T-005.md) | 未解決質問 | トランザクション | FAQ 登録前の未解決質問。 |
| <span id="TBL-H-005"></span>[`H_INQUIRY_FAQ`](TBL-H-005.md) | 未解決質問 FAQ 化履歴 | 履歴 | 未解決質問から FAQ への移行履歴(データコピー方式)。 |

#### 利用量・課金・上限 (5)

利用量計測、サブスク・請求書(7 年保持)、利用上限・無料枠。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-T-008"></span>[`T_USAGE_METER`](TBL-T-008.md) | 利用量計測 | トランザクション 課金7年 | 質問数・FAQ 件数をプロジェクト単位で計測し契約単位で集計。 |
| <span id="TBL-T-006"></span>[`T_BILL_SUBS`](TBL-T-006.md) | 課金サブスクリプション | トランザクション 課金7年 | Stripe サブスクと連動。 |
| <span id="TBL-T-007"></span>[`T_BILL_INVOICES`](TBL-T-007.md) | 請求書 | トランザクション 課金7年 | 月次請求書(電子帳簿保存法 7 年)。 |
| <span id="TBL-M-009"></span>[`M_PRJ_QUOTA_LIMITS`](TBL-M-009.md) | プロジェクト別利用設定 | マスタ | 質問数の月次上限・無料枠・アラート。 |
| <span id="TBL-M-008"></span>[`M_OWNER_QUOTA_OVR`](TBL-M-008.md) | 契約別レート上書き | マスタ | 契約単位のレート制限上書き(contract 単位)。 |

#### お知らせ・通知 (5)

運営お知らせ、配信対象、受信者集計、受信箱、メール通知ログ。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-M-010"></span>[`M_SERVICE_ANNOUNCE`](TBL-M-010.md) | お知らせ(Control Plane) | マスタ | お知らせ本体。 |
| <span id="TBL-M-011"></span>[`M_ANNOUNCE_AUD`](TBL-M-011.md) | お知らせ配信対象(M:N) | マスタ | 配信先を限定指定。 |
| <span id="TBL-T-009"></span>[`T_ANNOUNCE_RCPT`](TBL-T-009.md) | お知らせ受信者 | トランザクション | 実配信先・配信集計・監査。 |
| <span id="TBL-T-010"></span>[`T_INBOX_MSG`](TBL-T-010.md) | 受信箱(Tenant Plane) | トランザクション | 利用者が受け取る通知の既読状態。 |
| <span id="TBL-H-002"></span>[`H_NOTIF_LOGS`](TBL-H-002.md) | 通知ログ | 履歴 | メール通知の送信履歴。 |

#### 退会・データ管理 (1)

退会申請(90 日猶予)とデータ削除モード。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-T-011"></span>[`T_WITHDRAW_REQ`](TBL-T-011.md) | 退会申請 | トランザクション | 退会申請レコード(90 日猶予)。 |

#### システム・ログ・運用 (4)

監査ログ、エラーログ、メールサプレス、AI しきい値キャッシュ。

| 物理名 | 論理名 | 分類 / 保持 | 概要 |
|----|----|----|----|
| <span id="TBL-H-003"></span>[`H_AUDIT_LOGS`](TBL-H-003.md) | 監査ログ | 履歴 一部課金 | メイン側 API 操作ログ。 |
| <span id="TBL-H-004"></span>[`H_ERROR_LOGS`](TBL-H-004.md) | エラーログ | 履歴 | サーバーエラー記録。 |
| <span id="TBL-M-007"></span>[`M_EMAIL_SUPPRESS`](TBL-M-007.md) | メールサプレスリスト | マスタ | バウンス・苦情アドレス(全契約横断)。 |
| <span id="TBL-TP-002"></span>[`TP_AI_THRESH_CACHE`](TBL-TP-002.md) | AI しきい値キャッシュ | ワーク | 3 階層しきい値の永続キャッシュ。 |

## <span id="er"></span>3.ER 図(親子関係)

全 31 テーブルの親子関係を、機能ドメイン別の ER 図で示します。

**(1) アカウント・契約・メンバー**

```mermaid
erDiagram
  M_USER {
    TEXT id PK
  }
  M_CONTRACT {
    TEXT id PK
    TEXT user_id FK "→M_USER.id"
  }
  M_PROJECTS {
    TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id"
  }
  M_PRJ_USERS {
    TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id"
    TEXT user_id FK "→M_USER.id"
  }
  M_USER ||--o| M_CONTRACT : "オーナー"
  M_USER ||--o{ M_PRJ_USERS : "参加"
  M_CONTRACT ||--o{ M_PROJECTS : "保有"
  M_PROJECTS ||--o{ M_PRJ_USERS : "割当先"
```

**(2) 認証 — セッション**

```mermaid
erDiagram
  M_USER { TEXT id PK }
  T_SESSIONS {
    TEXT id PK
    TEXT user_id FK "→M_USER.id"
  }
  M_USER ||--o{ T_SESSIONS : "ユーザー"
```

**(3) 認証 — トークン**

```mermaid
erDiagram
  M_USER { TEXT id PK }
  T_ACCESS_TOKENS {
    TEXT id PK
    TEXT user_id FK "→M_USER.id"
  }
  M_USER ||--o{ T_ACCESS_TOKENS : "ユーザー"
```

**(4) 認証 — 規約同意**

```mermaid
erDiagram
  M_USER { TEXT id PK }
  M_TERMS_VER {
    TEXT doc_type PK
    TEXT version PK
  }
  T_TERMS_AGREE {
    TEXT id PK
    TEXT user_id FK "→M_USER.id"
    TEXT terms_version FK "→M_TERMS_VER"
  }
  M_USER ||--o{ T_TERMS_AGREE : "ユーザー"
  M_TERMS_VER ||--o{ T_TERMS_AGREE : "版"
```

**(5) プロジェクト・ウィジェット**

```mermaid
erDiagram
  M_CONTRACT { TEXT id PK }
  M_PROJECTS { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id" }
  M_ALLOWED_DOMAINS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  T_PRJ_LEGACY_KEYS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  M_CONTRACT ||--o{ M_PROJECTS : "保有"
  M_PROJECTS ||--o{ M_ALLOWED_DOMAINS : "許可ドメイン"
  M_PROJECTS ||--o{ T_PRJ_LEGACY_KEYS : "旧鍵"
```

**(6) FAQ**

```mermaid
erDiagram
  M_FAQS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  H_INQUIRY_FAQ { TEXT id PK
    TEXT inquiry_id FK "→T_INQUIRIES.id"
    TEXT faq_id FK "→M_FAQS.id" }
  M_PROJECTS { TEXT id PK }
  T_INQUIRIES { TEXT id PK }
  M_PROJECTS ||--o{ M_FAQS : "FAQ"
  T_INQUIRIES ||--o{ H_INQUIRY_FAQ : "FAQ化"
  M_FAQS ||--o{ H_INQUIRY_FAQ : "FAQ化履歴"
```

**(7) 質問ログ・参照 FAQ**

```mermaid
erDiagram
  H_QUESTION_LOGS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  T_QLOG_FAQ_REFS { TEXT id PK
    TEXT question_log_id FK "→H_QUESTION_LOGS.id"
    TEXT faq_id FK "→M_FAQS.id" }
  M_PROJECTS { TEXT id PK }
  M_FAQS { TEXT id PK }
  T_INQUIRIES { TEXT id PK
    TEXT question_log_id FK "→H_QUESTION_LOGS.id" }
  M_PROJECTS ||--o{ H_QUESTION_LOGS : "質問ログ"
  H_QUESTION_LOGS ||--o{ T_QLOG_FAQ_REFS : "参照FAQ"
  M_FAQS ||--o{ T_QLOG_FAQ_REFS : "被参照"
  H_QUESTION_LOGS ||--o| T_INQUIRIES : "未解決化"
```

**(8) 未解決質問**

```mermaid
erDiagram
  T_INQUIRIES { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id"
    TEXT question_log_id FK "→H_QUESTION_LOGS.id" }
  M_PROJECTS { TEXT id PK }
  H_QUESTION_LOGS { TEXT id PK }
  M_FAQS { TEXT id PK }
  H_INQUIRY_FAQ { TEXT id PK
    TEXT inquiry_id FK "→T_INQUIRIES.id"
    TEXT faq_id FK "→M_FAQS.id" }
  M_PROJECTS ||--o{ T_INQUIRIES : "未解決"
  H_QUESTION_LOGS ||--o| T_INQUIRIES : "未解決化"
  T_INQUIRIES ||--o{ H_INQUIRY_FAQ : "FAQ化"
  M_FAQS ||--o{ H_INQUIRY_FAQ : "FAQ化履歴"
```

**(9) 利用量・課金・上限**

```mermaid
erDiagram
  M_CONTRACT { TEXT id PK }
  M_PROJECTS { TEXT id PK }
  T_BILL_SUBS { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id" }
  T_BILL_INVOICES { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id" }
  T_USAGE_METER { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  M_PRJ_QUOTA_LIMITS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  M_OWNER_QUOTA_OVR { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id" }
  M_CONTRACT ||--o{ T_BILL_SUBS : "サブスク"
  M_CONTRACT ||--o{ T_BILL_INVOICES : "請求書"
  M_PROJECTS ||--o{ T_USAGE_METER : "計測"
  M_PROJECTS ||--o{ M_PRJ_QUOTA_LIMITS : "上限設定"
  M_CONTRACT ||--o| M_OWNER_QUOTA_OVR : "レート上書き"
```

**(10) お知らせ・通知**

```mermaid
erDiagram
  M_CONTRACT { TEXT id PK }
  M_SERVICE_ANNOUNCE { TEXT id PK }
  M_ANNOUNCE_AUD { TEXT announcement_id FK "→M_SERVICE_ANNOUNCE.id"
    TEXT contract_id FK "→M_CONTRACT.id" }
  T_ANNOUNCE_RCPT { TEXT id PK
    TEXT announcement_id FK "→M_SERVICE_ANNOUNCE.id" }
  T_INBOX_MSG { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id"
    TEXT recipient_id FK "→M_CONTRACT/M_PRJ_USERS" }
  H_NOTIF_LOGS { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id"
    TEXT inquiry_id FK "→T_INQUIRIES.id" }
  T_INQUIRIES { TEXT id PK }
  M_SERVICE_ANNOUNCE ||--o{ M_ANNOUNCE_AUD : "配信対象"
  M_CONTRACT ||--o{ M_ANNOUNCE_AUD : "対象契約"
  M_SERVICE_ANNOUNCE ||--o{ T_ANNOUNCE_RCPT : "fan-out"
  M_CONTRACT ||--o{ T_INBOX_MSG : "受信箱"
  M_CONTRACT ||--o{ H_NOTIF_LOGS : "通知ログ"
  T_INQUIRIES ||--o{ H_NOTIF_LOGS : "問合せ通知"
```

**(11) 退会・データ管理**

```mermaid
erDiagram
  M_CONTRACT { TEXT id PK }
  T_WITHDRAW_REQ { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id"
    TEXT applied_by_id FK "→M_CONTRACT/M_PRJ_USERS" }
  M_CONTRACT ||--o{ T_WITHDRAW_REQ : "退会申請"
```

**(12) システム・ログ・運用**

```mermaid
erDiagram
  M_CONTRACT { TEXT id PK }
  M_PROJECTS { TEXT id PK }
  H_AUDIT_LOGS { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id"
    TEXT actor_id FK "→M_CONTRACT/M_PRJ_USERS" }
  TP_AI_THRESH_CACHE { TEXT id PK
    TEXT contract_id FK "→M_CONTRACT.id"
    TEXT project_id FK "→M_PROJECTS.id" }
  M_CONTRACT ||--o{ H_AUDIT_LOGS : "監査"
  M_CONTRACT ||--o{ TP_AI_THRESH_CACHE : "しきい値"
  M_PROJECTS ||--o{ TP_AI_THRESH_CACHE : "PJしきい値"
```

## <span id="rule"></span>4.命名・分類規約

| 接頭辞 | 分類             | 用途                 |
|--------|------------------|----------------------|
| `M_`   | マスタ           | マスタ・設定         |
| `T_`   | トランザクション | トランザクション     |
| `H_`   | 履歴             | 履歴・ログ(追記専用) |
| `TP_`  | ワーク           | ワーク・派生         |

---

<!-- portal-bottom -->
[基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
