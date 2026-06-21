<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ **API設計**
<!-- /portal-top -->

# API 設計書

**メインシステムが提供する全 51 の REST API を 14 機能グループに整理した独立設計書です。** 各 API の詳細(基本情報 / 処理概要 / I/O / リクエスト・レスポンス / エラー)は、旧設計書と同じ構成で **グループ別の個別ページ**に展開しています。画面からの呼び出しは [画面設計書](01_screen-design.md)、テーブルは [データベース設計書](03_database-design.md) を参照してください。

*版数 v2.2 ・ 更新 2026-06-21 ・ API数 53 ・ 独立設計書*

## <span id="ov"></span>0.API 設計の方針

<div class="card-grid cols-3">
<div class="card"><div class="lead-ico">/v1</div><h4>REST + JSON</h4><p>全エンドポイントを <code>/v1</code> 配下に統一。リソース指向の URL 設計。</p></div>
<div class="card"><div class="lead-ico">🔑</div><h4>認証 / 認可</h4><p>Cookie セッション + CSRF。オーナー境界とプロジェクト境界を全 API で二重検証。</p></div>
<div class="card"><div class="lead-ico">⇄</div><h4>I/O 明示</h4><p>各 API が触れるテーブルを CRUD で明示し、DB 設計と縦串で追跡可能にする。</p></div>
</div>

| 観点 | 方針 |
|----|----|
| ベースパス | `/v1` 配下に統一(ウィジェット系は `/widget/v1`) |
| 認証方式 | 管理 API は Cookie セッション、更新系は CSRF トークン併用。ウィジェットは公開鍵 + ドメイン検証 |
| ページング | カーソル方式に統一(`cursor` / `limit`、末尾 `nextCursor=null`) |
| エラー応答 | `E-AUTH-*` / `E-AUTHZ-*` / `E-BIZ-*` / `E-INPUT-*` の ID 体系 |
| オーナー境界 | 全 API で `contract_id` による契約分離を強制 |

## <span id="list"></span>1.API 一覧(機能グループ別)

全 51 エンドポイントを 14 グループに整理。グループ名の「詳細を開く →」または API ID から、旧フォーマットの個別ページへ移動します。

### <span id="g-1"></span>1.1 認証・セッション

サインアップ / ログイン / 再認証 / メール確認 / 招待。

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-AUTH-001"></span>[`API-AUTH-001`](API-auth.md#API-AUTH-001) | **新規登録** POST `/auth/signup` | —(公開) | [`M_USER`](TBL-M-001.md)C--- [`M_CONTRACT`](TBL-M-002.md)CR-- [`T_TERMS_AGREE`](TBL-T-012.md)C--- [`T_ACCESS_TOKENS`](TBL-T-002.md)C--- |
| <span id="API-AUTH-002"></span>[`API-AUTH-002`](API-auth.md#API-AUTH-002) | **ログイン** POST `/auth/login` | —(公開) | [`M_CONTRACT`](TBL-M-002.md)-RU- [`M_PRJ_USERS`](TBL-M-003.md)-RU- [`T_SESSIONS`](TBL-T-001.md)C--- |
| <span id="API-AUTH-003"></span>[`API-AUTH-003`](API-auth.md#API-AUTH-003) | **ログアウト** POST `/auth/logout` | 認証済み | [`T_SESSIONS`](TBL-T-001.md)--U- |
| <span id="API-AUTH-004"></span>[`API-AUTH-004`](API-auth.md#API-AUTH-004) | **パスワード再設定要求** POST `/auth/password-reset-request` | —(公開) | [`M_CONTRACT`](TBL-M-002.md)-R-- [`M_PRJ_USERS`](TBL-M-003.md)-R-- [`T_ACCESS_TOKENS`](TBL-T-002.md)C--- |
| <span id="API-AUTH-005"></span>[`API-AUTH-005`](API-auth.md#API-AUTH-005) | **再認証** POST `/auth/re-auth` | 認証済み | [`M_CONTRACT`](TBL-M-002.md)-R-- [`M_PRJ_USERS`](TBL-M-003.md)-R-- [`T_ACCESS_TOKENS`](TBL-T-002.md)C--- |
| <span id="API-AUTH-006"></span>[`API-AUTH-006`](API-auth.md#API-AUTH-006) | **メール確認** POST `/auth/email-verifications/{token}` | — | [`T_ACCESS_TOKENS`](TBL-T-002.md)-RU- [`M_CONTRACT`](TBL-M-002.md)--U- |
| <span id="API-AUTH-007"></span>[`API-AUTH-007`](API-auth.md#API-AUTH-007) | **招待トークン検証・プレビュー** POST `/auth/invitations/{token}/preview` | — | [`T_ACCESS_TOKENS`](TBL-T-002.md)-R-- [`M_PROJECTS`](TBL-M-004.md)-R-- [`M_PRJ_USERS`](TBL-M-003.md)-R-- [`M_PRJ_USERS`](TBL-M-003.md)-R-- [`M_CONTRACT`](TBL-M-002.md)-R-- |
| <span id="API-AUTH-008"></span>[`API-AUTH-008`](API-auth.md#API-AUTH-008) | **メンバーアカウント有効化** POST `/auth/invitations/{token}/activate` | — | [`T_ACCESS_TOKENS`](TBL-T-002.md)-RU- [`M_USER`](TBL-M-001.md)--U- [`M_PRJ_USERS`](TBL-M-003.md)--U- [`T_TERMS_AGREE`](TBL-T-012.md)C--- [`H_AUDIT_LOGS`](TBL-H-003.md)C--- |
| <span id="API-AUTH-009"></span>[`API-AUTH-009`](API-auth.md#API-AUTH-009) | **プロジェクト連絡先メール確認** POST `/auth/contact-verifications/{token}` | — | [`T_ACCESS_TOKENS`](TBL-T-002.md)-RU- [`M_PROJECTS`](TBL-M-004.md)-RU- [`H_AUDIT_LOGS`](TBL-H-003.md)C--- |
| <span id="API-AUTH-010"></span>[`API-AUTH-010`](API-auth.md#API-AUTH-010) | **パスワード再設定確定** POST `/auth/password-reset` | —(公開) | [`T_ACCESS_TOKENS`](TBL-T-002.md)-RU- [`M_CONTRACT`](TBL-M-002.md)-RU- [`M_PRJ_USERS`](TBL-M-003.md)-RU- [`T_SESSIONS`](TBL-T-001.md)--U- |
| <span id="API-AUTH-011"></span>[`API-AUTH-011`](API-auth.md#API-AUTH-011) | **連絡先確認メール再送** POST `/auth/contact-verifications/resend` | オーナー専有 | [`M_PROJECTS`](TBL-M-004.md)-R-- [`T_ACCESS_TOKENS`](TBL-T-002.md)C-U- [`H_NOTIF_LOGS`](TBL-H-002.md)C--- |
| <span id="API-AUTH-012"></span>[`API-AUTH-012`](API-auth.md#API-AUTH-012) | **自己プロフィール更新** PATCH `/me/profile` | 認証済み | [`M_CONTRACT`](TBL-M-002.md)-RU- [`M_PRJ_USERS`](TBL-M-003.md)-RU- [`T_ACCESS_TOKENS`](TBL-T-002.md)C-R- |
| <span id="API-AUTH-013"></span>[`API-AUTH-013`](API-auth.md#API-AUTH-013) | **自己パスワード変更** PATCH `/me/password` | 認証済み | [`T_ACCESS_TOKENS`](TBL-T-002.md)-R-- [`M_CONTRACT`](TBL-M-002.md)-RU- [`M_PRJ_USERS`](TBL-M-003.md)-RU- |
| <span id="API-AUTH-014"></span>[`API-AUTH-014`](API-auth.md#API-AUTH-014) | **契約設定取得** GET `/owner/settings` | オーナー専有 | [`M_CONTRACT`](TBL-M-002.md)-R-- |
| <span id="API-AUTH-015"></span>[`API-AUTH-015`](API-auth.md#API-AUTH-015) | **契約設定更新** PATCH `/owner/settings` | オーナー専有 | [`M_CONTRACT`](TBL-M-002.md)-RU- |

### <span id="g-2"></span>1.2 プロジェクト

プロジェクト CRUD とウィジェット鍵ローテーション。

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-PRJ-001"></span>[`API-PRJ-001`](API-project.md#API-PRJ-001) | **プロジェクト一覧** GET `/projects` | オーナー専有 | [`M_PROJECTS`](TBL-M-004.md)-R-- [`M_FAQS`](TBL-M-006.md)-R-- [`M_ALLOWED_DOMAINS`](TBL-M-005.md)-R-- |
| <span id="API-PRJ-002"></span>[`API-PRJ-002`](API-project.md#API-PRJ-002) | **プロジェクト新規作成** POST `/projects` | オーナー専有(プロジェクト設定全般を含めオーナーのみ実行可) | [`M_PROJECTS`](TBL-M-004.md)CR-- [`M_ALLOWED_DOMAINS`](TBL-M-005.md)C--- |
| <span id="API-PRJ-003"></span>[`API-PRJ-003`](API-project.md#API-PRJ-003) | **プロジェクト更新・削除** PATCH DELETE `/projects/{id}` | オーナー専有 | [`M_PROJECTS`](TBL-M-004.md)-RU- [`M_ALLOWED_DOMAINS`](TBL-M-005.md)--U- [`M_PRJ_USERS`](TBL-M-003.md)--U- [`M_PRJ_USERS`](TBL-M-003.md)--U- [`T_SESSIONS`](TBL-T-001.md)--U- [`T_ACCESS_TOKENS`](TBL-T-002.md)--U- [`M_FAQS`](TBL-M-006.md)--U- [`H_QUESTION_LOGS`](TBL-H-001.md)--U- [`T_INQUIRIES`](TBL-T-005.md)--U- [`H_AUDIT_LOGS`](TBL-H-003.md)C--- |
| <span id="API-PRJ-004"></span>[`API-PRJ-004`](API-project.md#API-PRJ-004) | **ウィジェット鍵ローテーション** POST `/projects/{id}/widget-key/rotate` | オーナー専有 | [`M_PROJECTS`](TBL-M-004.md)--U- |

### <span id="g-3"></span>1.3 メンバー

プロジェクト単位のメンバー招待 / 情報更新 / 離脱。

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-MBR-001"></span>[`API-MBR-001`](API-member.md#API-MBR-001) | **メンバー一覧** GET `/projects/{id}/members` | オーナー / 当該プロジェクトのメンバー | [`M_PRJ_USERS`](TBL-M-003.md)-R-- [`M_PRJ_USERS`](TBL-M-003.md)-R-- |
| <span id="API-MBR-002"></span>[`API-MBR-002`](API-member.md#API-MBR-002) | **メンバー招待** POST `/projects/{id}/members` | オーナー / 当該プロジェクトのメンバー | [`M_USER`](TBL-M-001.md)CR-- [`M_PRJ_USERS`](TBL-M-003.md)CR-- [`T_ACCESS_TOKENS`](TBL-T-002.md)C--- [`H_NOTIF_LOGS`](TBL-H-002.md)C--- |
| <span id="API-MBR-003"></span>[`API-MBR-003`](API-member.md#API-MBR-003) | **メンバー情報更新** PATCH `/projects/{id}/members/{userId}` | オーナー / 当該プロジェクトのメンバー | [`M_PRJ_USERS`](TBL-M-003.md)-RU- |
| <span id="API-MBR-004"></span>[`API-MBR-004`](API-member.md#API-MBR-004) | **プロジェクト割当解除** DELETE `/projects/{id}/members/{userId}` | オーナー / 当該プロジェクトのメンバー | [`M_PRJ_USERS`](TBL-M-003.md)-RU- [`M_PRJ_USERS`](TBL-M-003.md)--U- [`T_SESSIONS`](TBL-T-001.md)--U- [`T_ACCESS_TOKENS`](TBL-T-002.md)--U- |
| <span id="API-MBR-005"></span>[`API-MBR-005`](API-member.md#API-MBR-005) | **招待メール再送** POST `/members/{id}/resend-invitation` | オーナー / 当該プロジェクトのメンバー | [`M_PRJ_USERS`](TBL-M-003.md)-R-- [`M_PRJ_USERS`](TBL-M-003.md)-R-- [`T_ACCESS_TOKENS`](TBL-T-002.md)C-U- [`H_NOTIF_LOGS`](TBL-H-002.md)C--- |

### <span id="g-4"></span>1.4 FAQ

FAQ の CRUD・一括状態変更・CSV 入出力・全文検索・質問ログ検索。

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-FAQ-001"></span>[`API-FAQ-001`](API-faq.md#API-FAQ-001) | **FAQ 一覧** GET `/faqs` | オーナー / 当該プロジェクトのメンバー | [`M_FAQS`](TBL-M-006.md)-R-- |
| <span id="API-FAQ-002"></span>[`API-FAQ-002`](API-faq.md#API-FAQ-002) | **FAQ 作成・更新・削除** POST PATCH DELETE `/faqs, /faqs/{id}` | オーナー / 当該プロジェクトのメンバー | [`M_FAQS`](TBL-M-006.md)CRU- |
| <span id="API-FAQ-003"></span>[`API-FAQ-003`](API-faq.md#API-FAQ-003) | **FAQ 一括状態変更** POST `/faqs/bulk-status` | オーナー / 当該プロジェクトのメンバー | [`M_FAQS`](TBL-M-006.md)-RU- |
| <span id="API-FAQ-004"></span>[`API-FAQ-004`](API-faq.md#API-FAQ-004) | **FAQ CSV インポート** POST `/faqs/import` | オーナー / 当該プロジェクトのメンバー | [`M_FAQS`](TBL-M-006.md)CRU- |
| <span id="API-FAQ-005"></span>[`API-FAQ-005`](API-faq.md#API-FAQ-005) | **FAQ インポートテンプレート** GET `/faqs/import/template` | オーナー / 当該プロジェクトのメンバー(API-022 と同一) | — |
| <span id="API-FAQ-006"></span>[`API-FAQ-006`](API-faq.md#API-FAQ-006) | **FAQ CSV エクスポート** GET `/faqs/export` | オーナー / 当該プロジェクトのメンバー | [`M_FAQS`](TBL-M-006.md)-R-- |
| <span id="API-FAQ-007"></span>[`API-FAQ-007`](API-faq.md#API-FAQ-007) | **FAQ 全文検索** GET `/projects/{id}/faqs/search` | オーナー / 当該プロジェクトのメンバー | [`M_FAQS`](TBL-M-006.md)-R-- [`TP_FAQ_FTS`](TBL-TP-001.md)-R-- |
| <span id="API-FAQ-008"></span>[`API-FAQ-008`](API-faq.md#API-FAQ-008) | **質問ログ検索** GET `/projects/{id}/question-logs/search` | オーナー / 当該プロジェクトのメンバー | [`H_QUESTION_LOGS`](TBL-H-001.md)-R-- |
| <span id="API-FAQ-009"></span>[`API-FAQ-009`](API-faq.md#API-FAQ-009) | **FAQ 個別取得** GET `/faqs/{id}` | オーナー / 当該プロジェクトのメンバー | [`M_FAQS`](TBL-M-006.md)-R-- |

### <span id="g-5"></span>1.5 未解決質問

未解決質問の一覧・詳細・ステータス更新。

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-INQ-001"></span>[`API-INQ-001`](API-inquiry.md#API-INQ-001) | **未解決質問一覧** GET `/inquiries` | オーナー / 当該プロジェクトのメンバー | [`T_INQUIRIES`](TBL-T-005.md)-R-- |
| <span id="API-INQ-002"></span>[`API-INQ-002`](API-inquiry.md#API-INQ-002) | **未解決質問詳細・状況切替** GET PATCH `/inquiries/{id}` | オーナー / 当該プロジェクトのメンバー | [`T_INQUIRIES`](TBL-T-005.md)-RU- |
| <span id="API-INQ-003"></span>[`API-INQ-003`](API-inquiry.md#API-INQ-003) | **未解決質問 CSV エクスポート** GET `/inquiries/export` | オーナー / 当該プロジェクトのメンバー | [`T_INQUIRIES`](TBL-T-005.md)-R-- |

### <span id="g-6"></span>1.6 ウィジェット配信

エンドユーザー向けウィジェットの bootstrap / ask / 問い合わせ。

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-WGT-001"></span>[`API-WGT-001`](API-widget.md#API-WGT-001) | **ウィジェット起動** POST `/widget/v1/bootstrap` | end_user(公開キー) | [`M_PROJECTS`](TBL-M-004.md)-R-- [`M_ALLOWED_DOMAINS`](TBL-M-005.md)-R-- [`M_CONTRACT`](TBL-M-002.md)-R-- |
| <span id="API-WGT-002"></span>[`API-WGT-002`](API-widget.md#API-WGT-002) | **ウィジェット質問送信** POST `/widget/v1/ask` | end_user(セッション) | [`H_QUESTION_LOGS`](TBL-H-001.md)C--- [`M_FAQS`](TBL-M-006.md)-R-- [`T_USAGE_METER`](TBL-T-008.md)C-U- [`T_INQUIRIES`](TBL-T-005.md)C--- |
| <span id="API-WGT-003"></span>[`API-WGT-003`](API-widget.md#API-WGT-003) | **ウィジェット未解決質問登録** POST `/widget/v1/inquiries` | end_user(セッション) | [`T_INQUIRIES`](TBL-T-005.md)C--- [`H_QUESTION_LOGS`](TBL-H-001.md)-R-- |

### <span id="g-7"></span>1.7 ダッシュボード

概要画面向けの集計サマリー。

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-DASH-001"></span>[`API-DASH-001`](API-dashboard.md#API-DASH-001) | **ダッシュボードサマリ** GET `/dashboard/summary` | オーナー / 当該プロジェクトのメンバー(notification ブロックの配信失敗・バウンス件数はオーナー専有) | [`T_USAGE_METER`](TBL-T-008.md)-R-- [`H_QUESTION_LOGS`](TBL-H-001.md)-R-- [`T_INQUIRIES`](TBL-T-005.md)-R-- [`H_NOTIF_LOGS`](TBL-H-002.md)-R-- |

### <span id="g-8"></span>1.8 利用量・課金

利用量・請求サマリー・請求書・支払方法・上限設定。

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-BIL-001"></span>[`API-BIL-001`](API-billing.md#API-BIL-001) | **利用量サマリ(プロジェクト)** GET `/usage` | オーナー / 当該プロジェクトのメンバー | [`T_USAGE_METER`](TBL-T-008.md)-R-- [`M_FAQS`](TBL-M-006.md)-R-- |
| <span id="API-BIL-002"></span>[`API-BIL-002`](API-billing.md#API-BIL-002) | **利用量サマリ(契約)** GET `/owner/projects/usage` | オーナー専有 | [`T_USAGE_METER`](TBL-T-008.md)-R-- [`M_FAQS`](TBL-M-006.md)-R-- |
| <span id="API-BIL-003"></span>[`API-BIL-003`](API-billing.md#API-BIL-003) | **請求サマリ** GET `/billing/summary` | オーナー専有 | [`T_BILL_SUBS`](TBL-T-006.md)-R-- [`T_USAGE_METER`](TBL-T-008.md)-R-- |
| <span id="API-BIL-004"></span>[`API-BIL-004`](API-billing.md#API-BIL-004) | **請求書一覧** GET `/billing/invoices` | オーナー専有 | [`T_BILL_INVOICES`](TBL-T-007.md)-R-- |
| <span id="API-BIL-005"></span>[`API-BIL-005`](API-billing.md#API-BIL-005) | **支払方法 取得・登録・更新** GET PUT `/billing/payment-method` | オーナー専有 | [`T_BILL_SUBS`](TBL-T-006.md)-RU- |
| <span id="API-BIL-006"></span>[`API-BIL-006`](API-billing.md#API-BIL-006) | **プロジェクト上限・アラート取得** GET `/projects/{id}/quota-limits` | オーナー / 当該プロジェクトのメンバー(閲覧) | [`M_PRJ_QUOTA_LIMITS`](TBL-M-009.md)-R-- [`T_USAGE_METER`](TBL-T-008.md)-R-- |
| <span id="API-BIL-007"></span>[`API-BIL-007`](API-billing.md#API-BIL-007) | **プロジェクト上限・アラート更新** PATCH `/projects/{id}/quota-limits/questions` | オーナー / 当該プロジェクトのメンバー | [`M_PRJ_QUOTA_LIMITS`](TBL-M-009.md)--U- |

### <span id="g-9"></span>1.9 お知らせ受信箱

受信箱の取得・既読化。

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-ANN-001"></span>[`API-ANN-001`](API-inbox.md#API-ANN-001) | **お知らせ一覧** GET `/me/announcements` | オーナー / メンバー | [`T_INBOX_MSG`](TBL-T-010.md)-R-- |
| <span id="API-ANN-002"></span>[`API-ANN-002`](API-inbox.md#API-ANN-002) | **お知らせ個別既読** POST `/me/announcements/{id}/read` | オーナー / メンバー | [`T_INBOX_MSG`](TBL-T-010.md)--U- |
| <span id="API-ANN-003"></span>[`API-ANN-003`](API-inbox.md#API-ANN-003) | **お知らせ一括既読** POST `/me/announcements/read` | オーナー / メンバー | [`T_INBOX_MSG`](TBL-T-010.md)--U- [`H_AUDIT_LOGS`](TBL-H-003.md)C--- |
| <span id="API-ANN-004"></span>[`API-ANN-004`](API-inbox.md#API-ANN-004) | **お知らせ未読件数** GET `/me/announcements/unread-summary` | オーナー / メンバー | [`T_INBOX_MSG`](TBL-T-010.md)-R-- |

### <span id="g-10"></span>1.10 規約・退会

規約 / プライバシー取得・同意・退会申請。

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-TRM-001"></span>[`API-TRM-001`](API-terms.md#API-TRM-001) | **利用規約 最新版取得** GET `/terms/current` | —(公開) | [`M_TERMS_VER`](TBL-M-012.md)-R-- |
| <span id="API-TRM-002"></span>[`API-TRM-002`](API-terms.md#API-TRM-002) | **プライバシーポリシー 最新版取得** GET `/privacy/current` | —(公開) | [`M_TERMS_VER`](TBL-M-012.md)-R-- |
| <span id="API-TRM-003"></span>[`API-TRM-003`](API-terms.md#API-TRM-003) | **利用規約 同意** POST `/terms/agree` | オーナー / メンバー | [`T_TERMS_AGREE`](TBL-T-012.md)CR-- |
| <span id="API-TRM-004"></span>[`API-TRM-004`](API-terms.md#API-TRM-004) | **プライバシーポリシー 同意** POST `/privacy/agree` | オーナー / メンバー | [`T_TERMS_AGREE`](TBL-T-012.md)CR-- |
| <span id="API-TRM-005"></span>[`API-TRM-005`](API-terms.md#API-TRM-005) | **退会申請** POST `/withdrawal-requests` | オーナー専有 | [`T_WITHDRAW_REQ`](TBL-T-011.md)C--- [`M_CONTRACT`](TBL-M-002.md)-RU- |

### <span id="g-11"></span>1.11 AI 推論 IF

AI 推論連携インターフェース(外部 LLM)。

> [!NOTE]
> <span class="c-ic">ℹ</span>
>
> <div>
>
> 外部サービス連携インターフェース。DB を直接読み書きせず呼び出し側 API を経由します。
>
> </div>

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-AI-001"></span>[`API-AI-001`](API-ai.md#API-AI-001) | **AI 推論 IF(AnswerProvider)** | — | — |

### <span id="g-12"></span>1.12 メール配信 IF

トランザクションメール送信インターフェース。

> [!NOTE]
> <span class="c-ic">ℹ</span>
>
> <div>
>
> 外部サービス連携インターフェース。DB を直接読み書きせず呼び出し側 API を経由します。
>
> </div>

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-MAIL-001"></span>[`API-MAIL-001`](API-mail.md#API-MAIL-001) | **メール配信 IF(EmailProvider)** | — | — |

### <span id="g-13"></span>1.13 外部 Webhook

Stripe / Resend からの Webhook 受信。

| API ID | API / エンドポイント | 権限 | I/O(テーブル・CRUD) |
|----|----|----|----|
| <span id="API-WHK-001"></span>[`API-WHK-001`](API-webhook.md#API-WHK-001) | **外部 Webhook(Resend)** POST `/webhooks/resend` | —(署名検証のみ) | [`H_NOTIF_LOGS`](TBL-H-002.md)--U- [`M_EMAIL_SUPPRESS`](TBL-M-007.md)C--- [`H_AUDIT_LOGS`](TBL-H-003.md)C--- |

---

<!-- portal-bottom -->
[基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
