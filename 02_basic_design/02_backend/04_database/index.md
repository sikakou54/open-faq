# データベース設計書

**メインシステムのデータベース(Cloudflare D1 / SQLite)全 33 テーブルを機能ドメイン別に定義する設計書です。** 全ユーザーは `M_USER` で管理し、プロジェクトの所有(オーナー=作成者)は `M_PROJECTS.owner_user_id`、課金はユーザー単位の `M_BILLING_ACCOUNT` で管理します。立場(オーナー / メンバー)はプロジェクトごとに決まります。各テーブルの詳細はテーブル名のリンクから辿れます。

*版数 v3.8 ・ 更新 2026-06-26 ・ テーブル数 33 ・ 独立設計書*

## <span id="store"></span>1.データストア構成

<div class="card-grid cols-3">
<div class="card"><div class="lead-ico">D1</div><h4>Cloudflare D1(SQLite)</h4><p>全 33 テーブル。テナント境界は <code>project_id</code>(<code>M_PROJECTS.id</code>)、プロジェクト所有は <code>owner_user_id</code>、課金はユーザー単位の <code>M_BILLING_ACCOUNT</code> で表す。</p></div>
<div class="card"><div class="lead-ico">KV</div><h4>Workers KV</h4><p>セッション / トークン / レート制限のキャッシュ。</p></div>
<div class="card"><div class="lead-ico">R2</div><h4>R2 オブジェクト</h4><p>CSV 添付・ウィジェット静的アセット。</p></div>
</div>

## <span id="map"></span>2.テーブル一覧

全 33 テーブルを 7 ドメインに分類しています。テーブル名は個別ページ(概要 / カラム定義 / インデックス / コード値)へのリンクです。

#### 認証・アカウント・課金アカウント (7)

全ユーザーの認証(M_USER)、ユーザー単位の課金アカウント(M_BILLING_ACCOUNT)、プロジェクトメンバー割当、セッション・トークン・規約。プロジェクトの所有(オーナー=作成者)は `M_PROJECTS.owner_user_id` で表す。

| 物理名 | 論理名 | 分類 | 保持基準 | 概要 |
|----|----|----|----|----|
| <span id="TBL-001"></span>[`M_USER`](TBL-001.md) | ユーザーマスタ | マスタ | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | オーナー・メンバーを含む全ユーザーの認証情報を一元保持。 |
| <span id="TBL-002"></span>[`M_BILLING_ACCOUNT`](TBL-002.md) | 課金アカウントマスタ | マスタ | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | ユーザー単位の課金アカウント(user_id ごとに 1 件)。サブスク・支払方法・請求・課金状態を束ねる。所有・ロール判定には用いない。 |
| <span id="TBL-003"></span>[`M_PRJ_USERS`](TBL-003.md) | プロジェクトメンバー(割当) | マスタ | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | ユーザーをプロジェクトへ割り当て(役割差は持たない)。 |
| <span id="TBL-013"></span>[`T_SESSIONS`](TBL-013.md) | セッション | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 複数デバイス対応のログインセッション。 |
| <span id="TBL-014"></span>[`T_ACCESS_TOKENS`](TBL-014.md) | アクセストークン | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 招待・パスワード再設定・メール確認などの短期トークン。 |
| <span id="TBL-012"></span>[`M_TERMS_VER`](TBL-012.md) | 規約版数 | マスタ | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 利用規約・プライバシーポリシーの版。 |
| <span id="TBL-024"></span>[`T_TERMS_AGREE`](TBL-024.md) | 規約同意 | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 利用者ごとの規約同意履歴。 |
#### プロジェクト・ウィジェット (3)

FAQ プロジェクト本体(オーナー=作成者が所有)、許可ドメイン、ウィジェット鍵。

| 物理名 | 論理名 | 分類 | 保持基準 | 概要 |
|----|----|----|----|----|
| <span id="TBL-004"></span>[`M_PROJECTS`](TBL-004.md) | プロジェクト | マスタ | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | FAQ プロジェクトとウィジェット設定。owner_user_id でオーナー(作成者)を表す。 |
| <span id="TBL-005"></span>[`M_ALLOWED_DOMAINS`](TBL-005.md) | 許可ドメイン | マスタ | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | ウィジェット埋め込みを許可するドメイン。 |
| <span id="TBL-015"></span>[`T_PRJ_LEGACY_KEYS`](TBL-015.md) | レガシー API キー | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 鍵ローテーション時の旧キーを保持。具体値は [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) を参照。 |
#### FAQ・質問・未解決 (7)

FAQ 本体と全文検索、質問ログ、参照 FAQ、未解決質問、FAQ 化履歴、CSV 一括取込ジョブ。

| 物理名 | 論理名 | 分類 | 保持基準 | 概要 |
|----|----|----|----|----|
| <span id="TBL-006"></span>[`M_FAQS`](TBL-006.md) | FAQ | マスタ | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | FAQ 本体(質問・回答・公開状態)。テナント境界は project_id で表す。 |
| <span id="TBL-030"></span>[`TP_FAQ_FTS`](TBL-030.md) | FAQ 全文検索 | ワーク | —(M_FAQS派生) | FTS5 仮想テーブル(trigram)。 |
| <span id="TBL-025"></span>[`H_QUESTION_LOGS`](TBL-025.md) | 質問ログ | 履歴 | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | ウィジェット利用者の質問と AI 推論結果。 |
| <span id="TBL-016"></span>[`T_QLOG_FAQ_REFS`](TBL-016.md) | 参照 FAQ(M:N) | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 質問ログと参照 FAQ の中間テーブル。 |
| <span id="TBL-017"></span>[`T_INQUIRIES`](TBL-017.md) | 未解決質問 | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | FAQ 登録前の未解決質問。 |
| <span id="TBL-029"></span>[`H_INQUIRY_FAQ`](TBL-029.md) | 未解決質問 FAQ 化履歴 | 履歴 | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 未解決質問から FAQ への移行履歴(データコピー方式)。 |
| <span id="TBL-033"></span>[`TP_IMPORT_JOBS`](TBL-033.md) | FAQ取込ジョブ | ワーク | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | FAQ CSV 一括取込ジョブの状態・進捗・結果サマリ。 |
#### 利用量・課金・上限 (6)

利用量計測、サブスク・請求書、利用上限・無料枠、課金 Webhook 受信ログ。

| 物理名 | 論理名 | 分類 | 保持基準 | 概要 |
|----|----|----|----|----|
| <span id="TBL-020"></span>[`T_USAGE_METER`](TBL-020.md) | 利用量計測 | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 質問数・FAQ 件数をプロジェクト単位で計測しオーナー単位で集計。 |
| <span id="TBL-018"></span>[`T_BILL_SUBS`](TBL-018.md) | 課金サブスクリプション | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | Stripe サブスクと連動(課金アカウント単位)。 |
| <span id="TBL-019"></span>[`T_BILL_INVOICES`](TBL-019.md) | 請求書 | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 月次請求書。課金アカウント=オーナー単位、各プロジェクト内訳は明細で保持。 |
| <span id="TBL-032"></span>[`T_BILLING_WEBHOOK_LOG`](TBL-032.md) | 課金Webhook受信ログ | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 課金プロバイダ通知の受信・検証・取込状態を記録(重複検出・失敗再処理)。 |
| <span id="TBL-009"></span>[`M_PRJ_QUOTA_LIMITS`](TBL-009.md) | プロジェクト別利用設定 | マスタ | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 質問数の月次上限・無料枠・アラート。 |
| <span id="TBL-008"></span>[`M_OWNER_QUOTA_OVR`](TBL-008.md) | オーナー別レート上書き | マスタ | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | オーナー単位のレート制限上書き(owner_user_id 単位)。 |
#### お知らせ・通知 (5)

運営お知らせ、配信対象、受信者集計、受信箱、メール通知ログ。

| 物理名 | 論理名 | 分類 | 保持基準 | 概要 |
|----|----|----|----|----|
| <span id="TBL-010"></span>[`M_SERVICE_ANNOUNCE`](TBL-010.md) | お知らせ(Control Plane) | マスタ | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | お知らせ本体。 |
| <span id="TBL-011"></span>[`M_ANNOUNCE_AUD`](TBL-011.md) | お知らせ配信対象(M:N) | マスタ | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 配信先を限定指定(対象ユーザー)。 |
| <span id="TBL-021"></span>[`T_ANNOUNCE_RCPT`](TBL-021.md) | お知らせ受信者 | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 実配信先・配信集計・監査。 |
| <span id="TBL-022"></span>[`T_INBOX_MSG`](TBL-022.md) | 受信箱(Tenant Plane) | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 利用者が受け取る通知の既読状態。 |
| <span id="TBL-026"></span>[`H_NOTIF_LOGS`](TBL-026.md) | 通知ログ | 履歴 | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | メール通知の送信履歴。 |
#### 退会・データ管理 (1)

即時退会の実行記録とデータ削除モード。

| 物理名 | 論理名 | 分類 | 保持基準 | 概要 |
|----|----|----|----|----|
| <span id="TBL-023"></span>[`T_WITHDRAW_REQ`](TBL-023.md) | 退会記録 | トランザクション | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | 即時退会(アカウント単位)の実行記録(退会日時・退会者・理由・削除予定日)。 |
#### システム・ログ・運用 (4)

監査ログ、エラーログ、メールサプレス、AI しきい値キャッシュ。

| 物理名 | 論理名 | 分類 | 保持基準 | 概要 |
|----|----|----|----|----|
| <span id="TBL-027"></span>[`H_AUDIT_LOGS`](TBL-027.md) | 監査ログ | 履歴 | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | メイン側 API 操作ログ。 |
| <span id="TBL-028"></span>[`H_ERROR_LOGS`](TBL-028.md) | エラーログ | 履歴 | [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) | サーバーエラー記録。 |
| <span id="TBL-007"></span>[`M_EMAIL_SUPPRESS`](TBL-007.md) | メールサプレスリスト | マスタ | 恒久(抑制継続) | バウンス・苦情アドレス(全アカウント横断)。 |
| <span id="TBL-031"></span>[`TP_AI_THRESH_CACHE`](TBL-031.md) | AI しきい値キャッシュ | ワーク | 短期(キャッシュ) | プロジェクトごとの AI しきい値設定値の永続キャッシュ。 |

> [!NOTE]
> **保持期間**は論理削除(ログ系は記録)から物理削除までの保持基準です。具体値と区分の正本は [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) とし、本一覧では値を持ちません。物理削除は [SYS-027](../01_system/SYS-027.md#SYS-027)・[SYS-032](../01_system/SYS-032.md#SYS-032)・[SYS-034](../01_system/SYS-034.md#SYS-034) が保持期間を判定して実施します。

> [!NOTE]
> **退会時の扱い(2 区分)** アカウント退会時の運用データとアカウント・課金・請求データの扱いは [システム仕様書 §4](../../07_system-spec.md#4-データ保持期間削除猶予) を正本とします。本一覧では各テーブルが参照すべき保持基準のみを示し、具体的な保持値は記載しません。

## <span id="er"></span>3.ER 図(親子関係)

全 33 テーブルの親子関係を、機能ドメイン別の ER 図で示します。

**(1) アカウント・所有・メンバー**

```mermaid
erDiagram
  M_USER {
    TEXT id PK
  }
  M_BILLING_ACCOUNT {
    TEXT id PK
    TEXT user_id FK "→M_USER.id"
  }
  M_PROJECTS {
    TEXT id PK
    TEXT owner_user_id FK "→M_USER.id"
  }
  M_PRJ_USERS {
    TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id"
    TEXT user_id FK "→M_USER.id"
  }
  M_USER ||--o| M_BILLING_ACCOUNT : "課金アカウント"
  M_USER ||--o{ M_PROJECTS : "オーナー(作成者)"
  M_USER ||--o{ M_PRJ_USERS : "参加"
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
  M_USER { TEXT id PK }
  M_PROJECTS { TEXT id PK
    TEXT owner_user_id FK "→M_USER.id" }
  M_ALLOWED_DOMAINS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  T_PRJ_LEGACY_KEYS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  M_USER ||--o{ M_PROJECTS : "オーナー(作成者)"
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
  TP_IMPORT_JOBS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  M_PROJECTS ||--o{ M_FAQS : "FAQ"
  T_INQUIRIES ||--o{ H_INQUIRY_FAQ : "FAQ化"
  M_FAQS ||--o{ H_INQUIRY_FAQ : "FAQ化履歴"
  M_PROJECTS ||--o{ TP_IMPORT_JOBS : "取込ジョブ"
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
  M_USER { TEXT id PK }
  M_BILLING_ACCOUNT { TEXT id PK
    TEXT user_id FK "→M_USER.id" }
  M_PROJECTS { TEXT id PK }
  T_BILL_SUBS { TEXT id PK
    TEXT billing_account_id FK "→M_BILLING_ACCOUNT.id" }
  T_BILL_INVOICES { TEXT id PK
    TEXT billing_account_id FK "→M_BILLING_ACCOUNT.id" }
  T_USAGE_METER { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  M_PRJ_QUOTA_LIMITS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id" }
  M_OWNER_QUOTA_OVR { TEXT id PK
    TEXT owner_user_id FK "→M_USER.id" }
  M_BILLING_ACCOUNT ||--o{ T_BILL_SUBS : "サブスク"
  M_BILLING_ACCOUNT ||--o{ T_BILL_INVOICES : "請求書"
  M_PROJECTS ||--o{ T_USAGE_METER : "計測"
  M_PROJECTS ||--o{ M_PRJ_QUOTA_LIMITS : "上限設定"
  M_USER ||--o| M_OWNER_QUOTA_OVR : "レート上書き"
```

**(10) お知らせ・通知**

```mermaid
erDiagram
  M_USER { TEXT id PK }
  M_PROJECTS { TEXT id PK }
  M_SERVICE_ANNOUNCE { TEXT id PK }
  M_ANNOUNCE_AUD { TEXT announcement_id FK "→M_SERVICE_ANNOUNCE.id"
    TEXT user_id FK "→M_USER.id" }
  T_ANNOUNCE_RCPT { TEXT id PK
    TEXT announcement_id FK "→M_SERVICE_ANNOUNCE.id"
    TEXT user_id FK "→M_USER.id" }
  T_INBOX_MSG { TEXT id PK
    TEXT user_id FK "→M_USER.id" }
  H_NOTIF_LOGS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id"
    TEXT inquiry_id FK "→T_INQUIRIES.id" }
  T_INQUIRIES { TEXT id PK }
  M_SERVICE_ANNOUNCE ||--o{ M_ANNOUNCE_AUD : "配信対象"
  M_USER ||--o{ M_ANNOUNCE_AUD : "対象ユーザー"
  M_SERVICE_ANNOUNCE ||--o{ T_ANNOUNCE_RCPT : "fan-out"
  M_USER ||--o{ T_INBOX_MSG : "受信箱"
  M_PROJECTS ||--o{ H_NOTIF_LOGS : "通知ログ"
  T_INQUIRIES ||--o{ H_NOTIF_LOGS : "問合せ通知"
```

**(11) 退会・データ管理**

```mermaid
erDiagram
  M_USER { TEXT id PK }
  T_WITHDRAW_REQ { TEXT id PK
    TEXT user_id FK "→M_USER.id"
    TEXT applied_by_id FK "→M_USER.id(本人)" }
  M_USER ||--o{ T_WITHDRAW_REQ : "退会記録"
```

**(12) システム・ログ・運用**

```mermaid
erDiagram
  M_USER { TEXT id PK }
  M_PROJECTS { TEXT id PK }
  H_AUDIT_LOGS { TEXT id PK
    TEXT project_id FK "→M_PROJECTS.id"
    TEXT actor_id FK "→M_USER.id" }
  TP_AI_THRESH_CACHE { TEXT id PK
    TEXT owner_user_id FK "→M_USER.id"
    TEXT project_id FK "→M_PROJECTS.id" }
  M_PROJECTS ||--o{ H_AUDIT_LOGS : "監査"
  M_USER ||--o{ H_AUDIT_LOGS : "操作者"
  M_USER ||--o{ TP_AI_THRESH_CACHE : "しきい値"
  M_PROJECTS ||--o{ TP_AI_THRESH_CACHE : "PJしきい値"
```

## <span id="cross"></span>4.テーブル↔API / 業務UC 対応

テーブルを読み書きする API と参照する業務ユースケースの対応は [トレーサビリティ一覧](../../00_traceability/index.md#matrix-main) の「データベース」列に一元化しました。各テーブルページの「トレーサビリティ」節からも該当 TR を辿れます。

## <span id="readorder"></span>5.読み順

1. 本ページ §2 テーブル一覧でドメイン全体像を把握する。
2. §3 ER 図で親子(オーナー `M_USER` → `M_PROJECTS`(owner_user_id) → 各テーブル、課金は `M_USER` → `M_BILLING_ACCOUNT`)を確認する。
3. テーブルの利用 API / 業務UC は [トレーサビリティ一覧](../../00_traceability/index.md#matrix-main) で確認する。
4. 各テーブルページ(`TBL-NNN.md`)で 項目 / カラム定義 / 制約 / インデックス / コード値 を確認する。
<!-- /p5-cross -->

## <span id="rule"></span>6.命名・分類規約

| 接頭辞 | 分類             | 用途                 |
|--------|------------------|----------------------|
| `M_`   | マスタ           | マスタ・設定         |
| `T_`   | トランザクション | トランザクション     |
| `H_`   | 履歴             | 履歴・ログ(追記専用) |
| `TP_`  | ワーク           | ワーク・派生         |

### <span id="datarule"></span>6.1 共通データ規約(全テーブル共通)

各テーブルのカラム定義は本規約に従う。各テーブルページの「桁数」「制約」欄では、本規約と異なる場合のみ個別に明記する。

| 区分 | 規約 |
|---|---|
| 識別子(`id` / `*_id` の主キー・外部キー) | ULID(26 文字・Crockford Base32 の `TEXT`)。桁数欄は `26`。 |
| 日時(`*_at`) | ISO 8601 拡張形式・UTC・秒精度の文字列(例 `2026-06-24T08:00:00Z`)を `TEXT` で保持。表示時に JST へ変換(NFR 準拠)。 |
| 真偽 | `INTEGER` の `0` / `1`(`valid` など)。 |
| 文字列の桁 | 桁数欄に上限文字数を明記する。可変テキストは対応するバリデーション・業務ルール(RULE)に準拠(例: FAQ は質問 500 / 回答 5,000 文字 = [RULE-011](../../../01_requirements/01_business_requirement/08_rule.md#RULE-011))。 |
| パスワードハッシュ(`password_hash`) | Argon2id のエンコード文字列(`TEXT`・最大 255 文字)。平文は保持しない。 |
| メール HMAC(`email_hmac`) | HMAC-SHA256 の Hex 表現(`TEXT`・64 文字)。 |
| JSON カラム(`settings` / `meta` / `metadata` / `alert_thresholds` 等) | JSON 文字列を `TEXT` に格納し、内部のキー・型・既定値・制約を当該テーブルページで定義する。 |
| コード値カラム(`status` / `*_code` / `*_type` 等) | 取りうる値を当該テーブルページの「コード値・区分値」で列挙する。 |
