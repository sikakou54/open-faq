# 基本設計 index(メインシステム)

## 0. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | 基本設計 index(メインシステム) |
| 対象システム名 | FAQ AI ウィジェット SaaS / メインシステム(利用者向け) |
| 作成日 | 2026-05-17 |
| 作成者 | プロジェクト設計チーム |
| 版数 | v1.2 |
| ステータス | 承認済(v1.0 初版) |

## 1. 目的・対象範囲

| 項目 | 内容 |
|---|---|
| 目的 | メインシステム(利用者向け FAQ ウィジェット SaaS)の全体方針 + 設計方針 + 個別設計書への索引を示す。詳細仕様は本ディレクトリ配下の 10 個別設計書を正本とする。 |
| 対象範囲 | 利用者(オーナー / プロジェクト管理者 / メンバー)向け管理SaaSと公開FAQウィジェットのシステム全体方針 |
| 対象外 | 運営者システム([../../02_運営者システム/02_基本設計/](../../02_運営者システム/02_基本設計/))、実装ディレクトリ構成(詳細設計)、デプロイ詳細(運用設計) |
| 想定読者 | 設計レビュアー / 実装担当者 / AI 駆動開発担当 |

## 2. 設計方針(全体像)

| # | 方針 | 概要 | 詳細 |
|---|---|---|---|
| 1 | 画面設計方針 | SaaS 標準 SPA + サーバーサイドルーティング併用。SCR-001〜024(モーダル含む)を網羅。 | [01_画面設計.md](01_画面設計.md) |
| 2 | API 設計方針 | REST + JSON。`/v1` 配下に統一。`Authorization` ヘッダ。連携 IF #1〜#12(送信側)。 | [02_API設計.md](02_API設計.md) |
| 3 | データ設計方針 | RDB(マルチオーナーは `contract_owner_user_id` 列で分離)+ KV(セッション / トークン / レート制限)+ R2(添付・ウィジェット静的)。 | [03_テーブル設計.md](03_テーブル設計.md) |
| 4 | 権限設計方針 | オーナー専有機能 + プロジェクト別ロール(`project_users.role` = `admin` / `member`) + 契約状態による利用上書き。 | [04_権限設計.md](04_権限設計.md) |
| 5 | エラー設計方針 | `E-AUTH-*` / `E-AUTHZ-*` / `E-BIZ-*` / `E-INPUT-*` / `E-IF-*` の ID 体系。ステータスコード対応表。 | [05_エラー設計.md](05_エラー設計.md) |
| 6 | メッセージ設計方針 | `MSG-SCR-*` の ID 体系。通知契機 + テンプレート。重要度 `critical` はメール強制送信。 | [06_メッセージ一覧.md](06_メッセージ一覧.md) |
| 7 | トレーサビリティ方針 | 要件 → 機能 → 画面 → API → DB → 権限 → エラー → メッセージ → テスト観点を縦串で追跡。 | [07_トレーサビリティマトリクス.md](07_トレーサビリティマトリクス.md) |
| 8 | 認証・認可設計方針 | ID/PW + メール確認 + 規約同意。セッション + アクセストークン + リフレッシュトークン。オーナー境界 + Principal。 | [08_認証・認可設計.md](08_認証・認可設計.md) |
| 9 | セキュリティ設計方針 | PII 列単位暗号化 + 鍵管理 + 監査ログ + 不正利用検知 + メール配信信頼性 + Web 脆弱性対策。 | [09_セキュリティ設計.md](09_セキュリティ設計.md) |
| 10 | 課金・請求設計方針 | MVP 単一プラン(完全従量課金 + 月次無料枠、無料トライアル期間なし)+ 支払方法ゲート + Stripe Smart Retries + 契約状態 4 値。 | [10_課金・請求設計.md](10_課金・請求設計.md) |
| 11 | メール設計方針 | システムが送信する全 `TPL-*` テンプレートの件名・本文・送信契機の正本。共通基準(送信元・i18n・サニタイズ・配信信頼性)+ テンプレート詳細 + 配信運用。 | [11_メール設計.md](11_メール設計.md) |

## 3. システム構成(全体像)

| レイヤ | 構成要素 | 補足 |
|---|---|---|
| フロントエンド | SPA(Web)+ ウィジェット(エンドユーザー側 JS) | 認証画面 / 管理画面 / エンドユーザー画面 |
| API バックエンド | Cloudflare Workers + REST API | `/v1` 配下に統一 |
| データストア | D1(SQLite ベース)+ KV + R2 | RDB + キャッシュ + オブジェクト |
| 外部連携 | Stripe / Resend / OpenAI / 運営者システム / メール SMTP | 連携 IF #1〜#12 で明文化 |
| インフラ | Cloudflare Workers + Cron Triggers + Queues | サーバーレス前提 |

詳細構成図と利用技術一覧は [../03_詳細設計/index.md](../03_詳細設計/index.md) §2 を参照。

## 4. 機能一覧(FRxx_*.md と基本設計成果物の対応)

| FRxx ファイル | 概要 | 主関連画面 | 主関連 API |
|---|---|---|---|
| [../01_要件定義/FR01_アカウント管理.md](../01_要件定義/FR01_アカウント管理.md) | 新規登録 / ログイン / 再認証 / ログアウト | SCR-001〜003 | `POST /v1/sessions`, `POST /v1/accounts` |
| [../01_要件定義/FR02_ユーザー管理.md](../01_要件定義/FR02_ユーザー管理.md) | プロジェクト単位のメンバー管理 | SCR-009 / SCR-009-M1 | プロジェクト割当API |
| [../01_要件定義/FR03_プロジェクト管理.md](../01_要件定義/FR03_プロジェクト管理.md) | プロジェクト作成 / 編集 / 削除 | SCR-004 / SCR-004-M1 | `GET/POST/PATCH/DELETE /v1/projects` |
| [../01_要件定義/FR04_FAQ管理.md](../01_要件定義/FR04_FAQ管理.md) | FAQ CRUD + 公開 + 改版 | SCR-006 | `GET /v1/faqs` ほか |
| [../01_要件定義/FR05_AI回答.md](../01_要件定義/FR05_AI回答.md) | AI 推論 + 信頼度しきい値判定 | ウィジェット | `POST /v1/widget/ai-reply` |
| [../01_要件定義/FR06_未解決質問登録.md](../01_要件定義/FR06_未解決質問登録.md) | 未解決質問の登録 / 一覧 | SCR-005 | `GET /v1/inquiries` ほか |
| [../01_要件定義/FR07_未解決質問からFAQ登録.md](../01_要件定義/FR07_未解決質問からFAQ登録.md) | 未解決 → FAQ 候補化 / 公開 | SCR-005 / SCR-006 | `POST /v1/faqs/from-inquiry` |
| [../01_要件定義/FR08_処理エラー.md](../01_要件定義/FR08_処理エラー.md) | エラー一覧 / 再実行 | SCR-019 | `GET /v1/errors` |
| [../01_要件定義/FR09_利用量・課金.md](../01_要件定義/FR09_利用量・課金.md) | 利用量メータリング / 請求 | SCR-016 / SCR-021 / SCR-022 | `GET /v1/usage`, `GET /owner/projects/usage`, `GET /billing/summary`, `GET /v1/invoices` |
| [../01_要件定義/FR10_管理ダッシュボード.md](../01_要件定義/FR10_管理ダッシュボード.md) | 利用状況 / プロジェクト概要 | SCR-016 / SCR-008 | `GET /owner/projects/usage`, `GET /v1/usage` |
| [../01_要件定義/FR11_通知.md](../01_要件定義/FR11_通知.md) | 通知 / インボックス / メール | SCR-011 / SCR-012 | `GET /v1/inbox-messages` |
| [../01_要件定義/FR12_ウィジェット.md](../01_要件定義/FR12_ウィジェット.md) | ウィジェット配信 + 設定 + 許可ドメイン | SCR-007 | `GET /v1/widget-config` ほか |
| [../01_要件定義/FR13_プライバシー・データ管理.md](../01_要件定義/FR13_プライバシー・データ管理.md) | プライバシー / データ削除 | SCR-010 / SCR-020 / SCR-014 | `POST /v1/withdrawal-requests` |
| [../01_要件定義/FR14_セキュリティ.md](../01_要件定義/FR14_セキュリティ.md) | 不正利用検知 / 鍵管理 / 監査 | — | — |
| [../01_要件定義/FR15_お知らせ.md](../01_要件定義/FR15_お知らせ.md) | お知らせ配信 / 既読 | SCR-011 / SCR-012 | `GET /v1/inbox-messages` |
| [../01_要件定義/FR16_検索・全文検索.md](../01_要件定義/FR16_検索・全文検索.md) | FTS 検索 | SCR-006 | `GET /v1/faqs?q=` |
| [../01_要件定義/FR17_インポート・エクスポート.md](../01_要件定義/FR17_インポート・エクスポート.md) | FAQ の CSV インポート/エクスポート / 質問ログのエクスポート | SCR-006 / SCR-006-M1 / SCR-008 | `POST /v1/imports`(CSV のみ), `GET /v1/exports`(CSV のみ)|
| [../01_要件定義/FR18_UX細部・データ運用.md](../01_要件定義/FR18_UX細部・データ運用.md) | UX 細部要件 / データ運用要件 | 全画面 | — |
| [../01_要件定義/FR19_アクセス制御細部.md](../01_要件定義/FR19_アクセス制御細部.md) | アクセス制御細部要件 | — | — |
| [../01_要件定義/FR20_AI推論動作.md](../01_要件定義/FR20_AI推論動作.md) | AI 推論動作要件 | — | `POST /v1/widget/ai-reply` |
| [../01_要件定義/FR21_SCR画面マスタ.md](../01_要件定義/FR21_SCR画面マスタ.md) | SCR 画面一覧マスタ | 全画面 | — |

## 5. データフロー(概観)

```mermaid
graph LR
    EU[エンドユーザー] -->|質問| Widget[ウィジェット]
    Widget -->|/v1/widget/ai-reply| API[Workers API]
    API -->|FAQ 検索| D1[(D1)]
    API -->|AI 推論| OAI[OpenAI]
    API -->|未解決| Inquiry[(question_logs)]
    Inquiry --> Admin[管理者画面]
    Inquiry -->|FAQ 化| FAQ[(faqs)]
    API -->|利用量計測| Meter[(usage_metering)]
    Meter -->|月次集計| Stripe[Stripe]
    Stripe -->|Webhook IF#10| Operator[運営者システム]
    Operator -->|転送| API
```

## 6. 非機能要件への対応方針(基本)

| 観点 | 対応方針 | 詳細 |
|---|---|---|
| 性能 | API p95 < 500ms / AI 回答 p95 < 3s | [../03_詳細設計/index.md](../03_詳細設計/index.md) §13.1 |
| 可用性 | Cloudflare グローバル分散 + マルチリージョン DB レプリケーション | §13.2 |
| スケーラビリティ | サーバーレス自動スケール + KV キャッシュ | §13.3 |
| アクセシビリティ | WCAG 2.1 AA 準拠 | §13.4 |
| 国際化 | i18n 基盤(MVP は日本語のみ) | §13.5 |
| バックアップ | D1 自動バックアップ + R2 ライフサイクル | §13.6 / [../04_運用設計/02_バックアップ・リストア設計.md](../04_運用設計/02_バックアップ・リストア設計.md) |
| データ保持 | テーブル別 retention class 制御 | §13.7 |

## 7. 基本設計ファイル一覧

| # | ファイル | 概要 |
|---|---|---|
| 01 | [01_画面設計.md](01_画面設計.md) | SCR-001〜024 + モーダル の全画面定義 |
| 02 | [02_API設計.md](02_API設計.md) | 管理 API + 連携 IF #1〜#12(送信側)の全エンドポイント |
| 03 | [03_テーブル設計.md](03_テーブル設計.md) | 全テーブル + DDL + コード値 + 状態遷移 |
| 04 | [04_権限設計.md](04_権限設計.md) | 3 ロール(オーナー / プロジェクト管理者 / メンバー)+ プロジェクト別ロール(`project_users.role`)+ 契約状態上書き |
| 05 | [05_エラー設計.md](05_エラー設計.md) | エラー ID 体系 + ステータスコード対応表 + 共通方針 |
| 06 | [06_メッセージ一覧.md](06_メッセージ一覧.md) | メッセージ / 通知契機(メール本文の正本は §11 メール設計)|
| 07 | [07_トレーサビリティマトリクス.md](07_トレーサビリティマトリクス.md) | 要件 → 設計 → テスト観点の対応 |
| 08 | [08_認証・認可設計.md](08_認証・認可設計.md) | 認証 / セッション / Principal / オーナー境界 |
| 09 | [09_セキュリティ設計.md](09_セキュリティ設計.md) | PII 暗号化 / 鍵管理 / 監査ログ / 不正利用検知 |
| 10 | [10_課金・請求設計.md](10_課金・請求設計.md) | MVP 単一プラン + 契約状態 + Stripe Smart Retries |
| 11 | [11_メール設計.md](11_メール設計.md) | 全 `TPL-*` 件名 + 本文テンプレートの正本 + 配信運用 |

## 8. SCR × ドキュメント カバレッジ表

| SCR ID | 画面名 | 画面 | API | テーブル | 権限 | エラー | メッセージ | 認証認可 | セキュリティ | 課金 |
|---|---|---|---|---|---|---|---|---|---|---|
| SCR-001 | ログイン | §5.SCR-001 | `POST /v1/sessions` | `accounts`, `sessions` | §3 ロール | E-AUTH-* | MSG-SCR-001-* | §3 ログイン | §5 ロックアウト | - |
| SCR-002 | 新規登録 | §5.SCR-002 | `POST /v1/accounts` | `accounts` | - | E-AUTH-VALIDATION | MSG-SCR-002-* | §3 新規登録 | - | §5 契約開始(active) |
| SCR-003 | パスワード再設定 | §5.SCR-003 | `POST /v1/password/reset` | `accounts` | - | E-AUTH-* | MSG-SCR-003-* | §3 パスワード再設定 | §7 監査 | - |
| SCR-004 | プロジェクト | §5.SCR-004 | `GET /v1/projects` | `projects`, `project_users` | オーナー専有 | E-AUTHZ-OWNER-ONLY | MSG-SCR-004-* | §6 オーナー境界 | - | - |
| SCR-004-M1 | プロジェクト作成・編集モーダル | §5.SCR-004-M1 | `POST /v1/projects` / `PATCH /v1/projects/{id}` / `DELETE /v1/projects/{id}` | `projects`(作成時にオーナー grants 自動 INSERT、削除は論理削除)| オーナー専有 | E-INPUT-* | MSG-SCR-004-M1-* | §6 認可判定 | - | - |
| SCR-005 | 要対応の質問 一覧 / 詳細 | §5.SCR-005 | `GET /v1/inquiries` | `question_logs`, `inquiries` | オーナー / 該当 PJ の `member`+ | E-BIZ-CASE-* | MSG-SCR-005-* | §6 オーナー境界 | - | - |
| SCR-006 | FAQ 管理 | §5.SCR-006 | `GET /v1/faqs` ほか | `faqs`, `faq_revisions`, `faq_search_fts` | オーナー / 該当 PJ の `member`+ | E-BIZ-NOT-FOUND | MSG-SCR-006-* | §6 認可判定 | - | §3 FAQ 件数上限 |
| SCR-006-M1 | FAQ CSV インポートモーダル | §5.SCR-006-M1 | `POST /faqs/import`(CSV のみ), `GET /faqs/import/template` | `faqs`, `faq_revisions` | オーナー / 該当 PJ の `member`+ | E-INPUT-CSV-INVALID, E-INPUT-CSV-FAQID-NOTFOUND | MSG-SCR-006-M1-* | §6 認可判定 | - | §3 1 ファイル 1000 件 |
| SCR-007 | ウィジェット設定(プロジェクト WS / 公開キー + 見た目 + プレビュー)| §5.SCR-007 | `PATCH /v1/widget-config`, `POST /v1/projects/{id}/widget-key/rotate` | `projects`, `allowed_domains`, `project_legacy_keys` | 当該 PJ の `admin` 以上(`member` は閲覧のみ)| E-INPUT-DOMAIN | MSG-SCR-007-* | §6 API キー検証 | §12 ウィジェット保護 | - |
| SCR-008 | 概要(プロジェクト)| §5.SCR-008 | `GET /v1/usage?viewMode=project` | `usage_metering`, `inquiries`, `faqs` | オーナー / 該当 PJ の `member`+ | E-AUTHZ-FORBIDDEN | MSG-SCR-008-* | §6 認可判定 | - | - |
| SCR-009 | メンバー(プロジェクト)| §5.SCR-009 | プロジェクトメンバーAPI | `users`, `project_users` | オーナー / `admin`(該当 PJ)| E-AUTHZ-* | MSG-SCR-009-* | §3 招待受諾 | - | - |
| SCR-009-M1 | メンバー招待 / 編集モーダル(プロジェクト単位)| §5.SCR-009-M1 | `POST /v1/projects/:id/members`(招待), `PATCH /v1/projects/:id/members/:userId`(ロール変更), `DELETE /v1/projects/:id/members/:userId`(離脱・最後の割当時はアカウント停止)| `users`, `project_users`, `sessions`, `access_tokens` | オーナー / `admin`(該当 PJ)| E-INPUT-* / E-AUTHZ-* | MSG-SCR-009-M1-* | §3 招待トークン | - | - |
| SCR-010 | 利用規約閲覧(利用規約のみ)| §5.SCR-010 | `GET /v1/terms/current` | `terms_versions`(`doc_type='terms_of_service'`)| 認証不要 | - | MSG-SCR-010-* | - | - | - |
| SCR-020 | プライバシーポリシー閲覧(プライバシーポリシーのみ)| §5.SCR-020 | `GET /v1/privacy/current` | `terms_versions`(`doc_type='privacy_policy'`)| 認証不要 | - | MSG-SCR-020-* | - | - | - |
| SCR-021 | 利用量と上限 | §5.SCR-021 | `GET /v1/projects/{id}/quota-limits` | `project_quota_limits`, `usage_metering` | 閲覧 = オーナー / 該当 PJ の `member`+ | E-AUTHZ-FORBIDDEN | MSG-SCR-021-* | §6 認可判定 | - | §3a |
| SCR-021-M1 | 質問数上限設定モーダル | §5.SCR-021-M1 | `PATCH /v1/projects/{id}/quota-limits/questions` | `project_quota_limits` | オーナー / 該当 PJ の `admin` | E-AUTHZ-FORBIDDEN / E-INPUT-* | MSG-SCR-021-M1-* | §6 認可判定 | §7 再認証 | §3a |
| SCR-011 | お知らせ一覧 | §5.SCR-011 | `GET /v1/inbox-messages` | `inbox_messages` | 全ユーザー | - | MSG-SCR-011-* | §6 認可判定 | - | - |
| SCR-012 | お知らせ詳細 | §5.SCR-012 | `PATCH /v1/inbox-messages/:id/read` | `inbox_messages` | 全ユーザー | - | MSG-SCR-012-* | §6 認可判定 | - | - |
| SCR-013 | メール確認 | §5.SCR-013 | `POST /v1/email-verification` | `accounts` | - | E-AUTH-VERIFICATION | MSG-SCR-013-* | §3 メール確認 | - | - |
| SCR-014 | 退会申請 | §5.SCR-014 | `POST /v1/withdrawal-requests` | `withdrawal_requests` | オーナー専有 | E-BIZ-WITHDRAWAL | MSG-SCR-014-* | §6 オーナー専有 | - | §5 退会フロー |
| SCR-015 | 規約再同意割込み | §5.SCR-015 | `POST /v1/terms/agree` | `terms_agreements` | 全ユーザー | E-AUTHZ-TERMS | MSG-SCR-015-* | §3 規約再同意 | - | - |
| SCR-016 | 利用状況 | §5.SCR-016 | `GET /owner/projects/usage` | `usage_metering`, `question_logs`, `faqs`, `projects.valid` | オーナー専有 | E-AUTHZ-OWNER-ONLY | MSG-SCR-016-* | §6 認可判定 | - | - |
| SCR-017 | 個人設定 | §5.SCR-017 | `PATCH /v1/me`, `POST /v1/me/password` | `accounts`, `project_users` | 全認証ユーザー(自分のみ)| E-AUTH-* | MSG-SCR-017-* | §3 | §7 | - |
| SCR-022 | 請求 | §5.SCR-022 | `GET /billing/summary`, `GET /billing/invoices` | `billing_*` | オーナー専有 | E-BILL-* | MSG-SCR-022-* | §6 | - | §5〜§16 |
| SCR-023 | 設定 | §5.SCR-023 | `PATCH /v1/me/contact-email`, 退会/出力API | `contract_owners` | オーナー専有 | E-AUTHZ-OWNER-ONLY | MSG-SCR-023-* | §6 | §7 | §5 |

## 9. 連携 IF × ドキュメント カバレッジ

| IF # | 方向 | 概要 | API | エラー | セキュリティ | 課金 |
|---|---|---|---|---|---|---|
| #1 | 顧管 → メ | 契約停止イベント受信 | §5 IF #1 | E-IF-001-* | - | §5 サスペンション |
| #2 | 顧管 → メ | 強制ログアウト受信 | §5 IF #2 | E-IF-002-* | §7 監査 | - |
| #4 | 顧管 → メ | 復元実行 | §5 IF #4 | E-IF-004-* | §7 監査 | - |
| #5 | 顧管 → メ | レート制限上書き | §5 IF #5 | E-IF-005-* | - | §3 契約上書き |
| #6 | 顧管 → メ | AI パラメータ上書き | §5 IF #6 | E-IF-006-* | - | - |
| #7 | 顧管 → メ | お知らせ生成 | §5 IF #7 | E-IF-007-* | - | - |
| #8 | メ → 顧管 | 監視メトリクス取得 | §5 IF #8 | E-IF-008-* | §10 監視 | - |
| #9 | メ → 顧管 | 不正利用検知通知 | §5 IF #9 | E-IF-009-* | §10 不正利用検知 | - |
| #10 | 外 → 顧管 → メ | 課金 Webhook 受信・転送 | §5 IF #10 | E-IF-010-* | §7 監査 | §13 Webhook 処理 |
| #12 | 顧管 → メ → 利用者 | 運営者操作通知 | §5 IF #12 | E-IF-012-* | - | - |

(#3 / #11 は要件側で予約。MVP では未割り当て)

## 10. 関連ドキュメント

| ドキュメント | 役割 | リンク |
|---|---|---|
| 要件定義 | WHAT(機能要件 / 非機能要件 / 業務要件 / 受入条件) | [../01_要件定義/index.md](../01_要件定義/index.md) |
| 詳細設計 | 実装関連の詳細(モジュール構成 / バッチ / ログ / 監視 / 実装ガイドライン) | [../03_詳細設計/index.md](../03_詳細設計/index.md) |
| 運用設計 | 監視 / バックアップ / ログ / 障害対応 / リリース / 運用手順 | [../04_運用設計/index.md](../04_運用設計/index.md) |
| 画面遷移図(ワイヤーフレーム)| UI 表現(アカウント種別別)| [オーナー](../画面遷移図_オーナー.html) / [プロジェクト管理者](../画面遷移図_プロジェクト管理者.html) / [プロジェクトメンバー](../画面遷移図_プロジェクトメンバー.html) / [ウィジェット利用者](../画面遷移図_ウィジェット利用者.html) |
| 運営者側ドキュメント | 顧客管理システム側設計書 | [../../02_運営者システム/02_基本設計/index.md](../../02_運営者システム/02_基本設計/index.md) |
| 共有概念対応表 | メイン / 運営者の正本所在 | [../../共有/共有概念.md](../../共有/共有概念.md) |

## 11. 未確定事項・確認事項

| 確認事項ID | 確認内容 | 関連箇所 | 優先度 | ステータス |
|---|---|---|---|---|
| Q-BASE-001 | (現時点で未確定事項なし — v1.0 リリース時点で全項目確定済み) | - | 低 | 確認済 |
