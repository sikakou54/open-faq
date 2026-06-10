# 基本設計 index(運営者システム)

## 0. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | 基本設計 index(運営者システム) |
| 対象システム名 | FAQ AI ウィジェット SaaS / 運営者システム(SaaS 提供事業者向け管理コンソール) |
| 作成日 | 2026-05-17 |
| 作成者 | プロジェクト設計チーム |
| 版数 | v1.0 |
| ステータス | 承認済(v1.0 初版) |

## 1. 目的・対象範囲

| 項目 | 内容 |
|---|---|
| 目的 | 運営者システム(SaaS 提供者 = `open-faq` 運営)の全体方針 + 設計方針 + 個別設計書への索引。詳細仕様は本ディレクトリ配下の 10 個別設計書を正本とする。 |
| 対象範囲 | `service_operator` 単一ロール + 4-eyes 多段ガード + 監査ハッシュチェーン + Stripe Webhook 一次受信 |
| 対象外 | 利用者向けメインシステム([../../01_メインシステム/02_基本設計/](../../01_メインシステム/02_基本設計/))|
| 想定読者 | 設計レビュアー / 実装担当者 / 監査担当 / 運用担当 |

## 2. 設計方針(全体像)

| # | 方針 | 概要 | 詳細 |
|---|---|---|---|
| 1 | 6 段認可判定方針 | IP allowlist → セッション → MFA → role → 再認証 → 4-eyes の順で全 API・全画面に適用 | [08_認証・認可設計.md](08_認証・認可設計.md) |
| 2 | 4-eyes 承認フロー方針 | 対象 10 操作のうち 3 操作はハードゲート(承認なし実行不可)、7 操作は承認ログ(実行と承認ログを別運営者で実施) | [04_権限設計.md](04_権限設計.md) |
| 3 | 監査ハッシュチェーン方針 | `audit_logs` 全行に前行ハッシュを連鎖し改竄不能化。日次完全性検証 cron。3 区分保持(1y / 5y / 7y)。 | [09_セキュリティ設計.md](09_セキュリティ設計.md) |
| 4 | Stripe Webhook 一次受信方針 | 運営者側で一次受信し DLQ 30 日リプレイ。署名検証 + payload 差分検出 + メインへの転送 | [10_課金・請求設計.md](10_課金・請求設計.md) |
| 5 | 画面設計方針 | SCR-090〜099 + SCR-AUTH / SCR-HOME / SCR-APPROVALS。承認待ち一覧 + モーダル承認/却下。 | [01_画面設計.md](01_画面設計.md) |
| 6 | API 設計方針 | `/v1/operator/*` 配下。連携 IF #1〜#12 の主管責任(送信 8 + 受信 2)。 | [02_API設計.md](02_API設計.md) |
| 7 | データ設計方針 | `operator_*` テーブル群 + `audit_logs`(ハッシュチェーン)+ `webhook_events` + `operator_approvals` + `accounts_retired`。 | [03_テーブル設計.md](03_テーブル設計.md) |
| 8 | エラー設計方針 | `E-OP-*` プレフィックス。4-eyes 未承認 / IP allowlist 拒否 / 再認証期限切れの専用エラー。 | [05_エラー設計.md](05_エラー設計.md) |
| 9 | メッセージ設計方針 | 運営者画面文言 + IF #12 経由通知 + お知らせテンプレート。重要度 `critical` メール強制送信。 | [06_メッセージ一覧.md](06_メッセージ一覧.md) |
| 10 | トレーサビリティ方針 | 要件 → 機能 → 画面 → API → DB → 権限 → エラー → メッセージ → テスト観点。4-eyes 操作 10 件のマッピング表を含む。 | [07_トレーサビリティマトリクス.md](07_トレーサビリティマトリクス.md) |
| 11 | メール設計方針 | 運営者システム送信の全 `TPL-OP-*` 件名・本文の正本。運営者宛 13 + IF #12 経由 5 = 計 18 テンプレート + 集約窓 10 分。 | [11_メール設計.md](11_メール設計.md) |

## 3. システム構成(全体像)

| レイヤ | 構成要素 | 補足 |
|---|---|---|
| フロントエンド | 運営者専用 SPA(管理画面)| `admin.<domain>` の独立サブドメイン |
| API バックエンド | Cloudflare Workers + REST API | `/v1/operator/*` |
| データストア | D1(SQLite 互換)+ KV(セッション / IP allowlist)+ R2(エクスポート)| RDB は運営者専用 |
| 外部連携 | Stripe(Webhook 一次受信)/ メインシステム / SMTP / 監視 SaaS | 連携 IF #1〜#12 主管 |
| 認証基盤 | TOTP(MFA)+ 再認証チャレンジ + IP allowlist + 4-eyes | 6 段認可判定 |

詳細構成図と Worker トポロジーは [../03_詳細設計/index.md](../03_詳細設計/index.md) §2 を参照。

## 4. 機能一覧(FRxx_*.md と基本設計成果物の対応)

| FRxx ファイル | 概要 | 主関連画面 | 主関連 API |
|---|---|---|---|
| [../01_要件定義/FR01_アカウント管理.md](../01_要件定義/FR01_アカウント管理.md) | アカウント管理(メイン側を正本として参照)| - | - |
| [../01_要件定義/FR02_ユーザー管理.md](../01_要件定義/FR02_ユーザー管理.md) | ユーザー管理(メイン側を正本として参照)| - | - |
| [../01_要件定義/FR03_プロジェクト管理.md](../01_要件定義/FR03_プロジェクト管理.md) | プロジェクト管理(メイン側を正本として参照)| - | - |
| [../01_要件定義/FR04_FAQ管理.md](../01_要件定義/FR04_FAQ管理.md) | FAQ 管理(メイン側を正本として参照)| - | - |
| [../01_要件定義/FR05_AIパラメータ設定.md](../01_要件定義/FR05_AIパラメータ設定.md) | AI 推論パラメータの本番上書き(4-eyes ハードゲート)| SCR-092 | `PATCH /v1/operator/ai-parameters` |
| [../01_要件定義/FR06_未解決質問登録.md](../01_要件定義/FR06_未解決質問登録.md) | 未解決質問関連(メイン側を正本として参照)| - | - |
| [../01_要件定義/FR07_個別チャット.md](../01_要件定義/FR07_個別チャット.md) | 個別チャット関連(メイン側を正本として参照)| - | - |
| [../01_要件定義/FR08_未解決質問からFAQ登録.md](../01_要件定義/FR08_未解決質問からFAQ登録.md) | 未解決 → FAQ 関連(メイン側を正本として参照)| - | - |
| [../01_要件定義/FR09_処理エラー.md](../01_要件定義/FR09_処理エラー.md) | 処理エラー対応(運営者側エラーチケット連携)| - | - |
| [../01_要件定義/FR10_利用量・課金.md](../01_要件定義/FR10_利用量・課金.md) | 利用量・課金(運営者主管: Stripe Webhook 一次受信 / 月次請求確定)| SCR-097 | `POST /v1/operator/webhook/replay` |
| [../01_要件定義/FR11_管理ダッシュボード.md](../01_要件定義/FR11_管理ダッシュボード.md) | 運営者ホームダッシュボード | SCR-HOME | `GET /v1/operator/home` |
| [../01_要件定義/FR12_通知.md](../01_要件定義/FR12_通知.md) | 通知(IF #12 経由でメインへ転送)| - | - |
| [../01_要件定義/FR13_ウィジェット.md](../01_要件定義/FR13_ウィジェット.md) | ウィジェット(メイン側を正本として参照)| - | - |
| [../01_要件定義/FR14_プライバシー・データ管理.md](../01_要件定義/FR14_プライバシー・データ管理.md) | プライバシー / GDPR 越境移転ガード / `accounts_retired` 永久保持 | - | - |
| [../01_要件定義/FR15_セキュリティ.md](../01_要件定義/FR15_セキュリティ.md) | セキュリティ(運営者主管: 監査ハッシュチェーン / IP allowlist / MFA)| - | - |
| [../01_要件定義/FR16_お知らせ.md](../01_要件定義/FR16_お知らせ.md) | お知らせ作成・配信 | SCR-094 | `POST /v1/operator/announcements` |
| [../01_要件定義/FR17_削除データ参照・復元.md](../01_要件定義/FR17_削除データ参照・復元.md) | 削除データ参照 / 復元(運営者専用 / 4-eyes 承認ログ)| SCR-090 / SCR-091 | `GET /v1/operator/deleted/:type/:id`, `POST /v1/operator/restore` |
| [../01_要件定義/FR18_運営者の責務.md](../01_要件定義/FR18_運営者の責務.md) | 運営者の責務(SLA / オンコール / 監査 / GDPR)| - | - |
| [../01_要件定義/FR19_UI・UX共通.md](../01_要件定義/FR19_UI・UX共通.md) | 運営者画面 UI/UX 共通要件 | 全画面 | - |
| [../01_要件定義/FR20_ナビゲーション・情報構造.md](../01_要件定義/FR20_ナビゲーション・情報構造.md) | ナビゲーション・情報構造要件 | 全画面 | - |
| [../01_要件定義/FR21_ローディング・フィードバック.md](../01_要件定義/FR21_ローディング・フィードバック.md) | ローディング・フィードバック要件 | 全画面 | - |
| [../01_要件定義/FR22_アクセシビリティ強化.md](../01_要件定義/FR22_アクセシビリティ強化.md) | アクセシビリティ強化要件 | 全画面 | - |
| [../01_要件定義/FR23_4-eyes承認.md](../01_要件定義/FR23_4-eyes承認.md) | 4-eyes 承認(対象 10 操作)| SCR-APPROVALS | `POST /v1/operator/approvals` ほか |
| [../01_要件定義/FR24_監査・SLA.md](../01_要件定義/FR24_監査・SLA.md) | 監査ログ参照 / SLA 監視 / 運営者活動ダッシュボード | SCR-096 | `GET /v1/operator/audit-logs` |

## 5. SCR × ドキュメント カバレッジ表

| SCR ID | 画面名 | 画面 | API | テーブル | 権限 | エラー | メッセージ | 認証認可 | セキュリティ | 課金 |
|---|---|---|---|---|---|---|---|---|---|---|
| SCR-AUTH | 運営者ログイン | §5.SCR-AUTH | `POST /v1/operator/sessions` | `operator_sessions`, `service_operators` | §2 単一ロール | E-OP-AUTH-* | MSG-SCR-AUTH-* | §3 ログイン | §5 ロックアウト | - |
| SCR-AUTH-M1 | MFA 初回セットアップ | §5.SCR-AUTH-M1 | `POST /v1/operator/mfa/enroll` | `operator_mfa_secrets` | - | E-OP-MFA-* | MSG-SCR-AUTH-M1-* | §3 MFA / §4 TOTP | - | - |
| SCR-HOME | ホームダッシュボード | §5.SCR-HOME | `GET /v1/operator/home` | (各種) | 全運営者 | - | MSG-SCR-HOME-* | §6 セッション検証 | - | - |
| SCR-090 | 削除データ参照 | §5.SCR-090 | `GET /v1/operator/deleted/:type/:id` | `accounts_retired`, `audit_logs` | 4-eyes 不要 | E-OP-AUTHZ-* | MSG-SCR-090-* | §6 再認証 | §7 監査 | - |
| SCR-091 | 削除データ復元 | §5.SCR-091 | `POST /v1/operator/restore` | `accounts_retired`, `audit_logs` | 4-eyes 承認ログ | E-OP-RESTORE-* | MSG-SCR-091-* | §6 4-eyes 承認 | §7 監査 | - |
| SCR-092 | AI 推論パラメータ設定 | §5.SCR-092 | `PATCH /v1/operator/ai-parameters` | `ai_parameter_overrides`, `audit_logs` | **4-eyes ハードゲート** | E-OP-4EYES-* | MSG-SCR-092-* | §6 ハードゲート | §7 監査 | - |
| SCR-093 | レート制限(契約単位)・上限件数(プロジェクト単位)上書き | §5.SCR-093 | `PUT /admin/v1/overrides/rate-limit/{owner_id}`(契約)/ `.../usage-limit/{owner_id}/{project_id}`(プロジェクト)| `owner_quota_overrides`(レート)/ メイン `project_quota_limits`(月次上限件数)| 4-eyes 承認ログ | E-OP-OVERRIDE-* | MSG-SCR-093-* | §6 4-eyes 承認 | §7 監査 | §3 利用上限上書き |
| SCR-094 | お知らせ作成・配信 | §5.SCR-094 | `POST /v1/operator/announcements` ほか | `announcement_drafts`, `service_announcements` | 全運営者 | E-OP-INPUT-* | MSG-SCR-094-* | §6 認可判定 | - | - |
| SCR-096 | 運営者活動ダッシュボード | §5.SCR-096 | `GET /v1/operator/audit-logs` | `audit_logs` | 全運営者(参照)| - | MSG-SCR-096-* | §6 認可判定 | §7 監査参照 | - |
| SCR-097 | Webhook リプレイ・DLQ 操作 | §5.SCR-097 | `POST /v1/operator/webhook/replay` ほか | `webhook_events`, `dlq_replay_log` | 4-eyes 承認ログ | E-OP-WEBHOOK-* | MSG-SCR-097-* | §6 4-eyes 承認 | §7 監査 | §13 DLQ |
| SCR-098 | PII 誤検出報告管理 | §5.SCR-098 | `GET /v1/operator/pii-reports` ほか | `pii_false_positive_reports` | 全運営者 | E-OP-PII-* | MSG-SCR-098-* | §6 認可判定 | §13 PII マスキング | - |
| SCR-099 | Webhook ペイロード差分検出 | §5.SCR-099 | `GET /v1/operator/webhook/diffs` | `webhook_payload_diffs` | 全運営者 | - | MSG-SCR-099-* | §6 認可判定 | §7 監査 | §13 差分検出 |
| SCR-APPROVALS | 承認待ち一覧(4-eyes)| §5.SCR-APPROVALS | `GET /v1/operator/approvals` | `operator_approvals` | 4-eyes 申請者/承認者 | E-OP-4EYES-* | MSG-SCR-APPROVALS-* | §6 4-eyes フロー | §7 監査 | - |
| SCR-APPROVALS-M1 | 4-eyes 承認申請モーダル | §5.SCR-APPROVALS-M1 | `POST /v1/operator/approvals` | `operator_approvals` | 4-eyes 申請者 | E-OP-4EYES-* | MSG-SCR-APPROVALS-M1-* | §6 申請 / payload_hash | §7 監査 | - |
| SCR-APPROVALS-M2 | 4-eyes 承認/却下モーダル | §5.SCR-APPROVALS-M2 | `POST /v1/operator/approvals/:id/approve` ほか | `operator_approvals` | 4-eyes 承認者 | E-OP-4EYES-* | MSG-SCR-APPROVALS-M2-* | §6 承認 / 自己承認禁止 | §7 監査 | - |

## 6. 4-eyes 対象 10 操作カバレッジ表

| # | 操作 | 種別 | SCR | action code | retention_class | API |
|---|---|---|---|---|---|---|
| 1 | 契約物理削除 | **ハードゲート** | SCR-091 派生 | `owner.physical_delete` | 7y(operator_high_priv)| `DELETE /v1/operator/owners/:id/physical` |
| 2 | AI パラメータ変更(本番)| **ハードゲート** | SCR-092 | `ai_parameter.update` | 5y(operator_high_priv)| `PATCH /v1/operator/ai-parameters` |
| 3 | マスター鍵ローテーション | **ハードゲート** | (運用 CLI) | `key.master_rotate` | 5y(operator_high_priv)| (CLI) |
| 4 | 契約無効化 / サスペンション解除 | 承認ログ | SCR-091 派生 | `owner.suspend`, `owner.restore` | 5y(billing)| `POST /v1/operator/owners/:id/suspend` ほか |
| 5 | 契約別レート制限上書き | 承認ログ | SCR-093 | `rate_limit.override` | 5y(general)| `PATCH /v1/operator/rate-limits` |
| 6 | プロジェクト別上限件数上書き | 承認ログ | SCR-093 | `usage_limit.override` | 5y(billing)| `PUT /admin/v1/overrides/usage-limit/{owner_id}/{project_id}` |
| 7 | 強制停止(契約単位)| 承認ログ | SCR-093 派生 | `owner.force_stop` | 5y(operator_high_priv)| `POST /v1/operator/owners/:id/force-stop` |
| 8 | 削除データ復元 | 承認ログ | SCR-091 | `owner.restore_data` | 5y(operator_high_priv)| `POST /v1/operator/restore` |
| 9 | 課金 Webhook リプレイ | 承認ログ | SCR-097 | `webhook.replay` | 5y(billing)| `POST /v1/operator/webhook/replay` |
| 10 | 法的レビュー結果記録 | 承認ログ | SCR-098 派生 | `owner.legal_review.record` | 7y(operator_high_priv)| `POST /v1/operator/legal-review` |

## 7. 連携 IF × ドキュメント カバレッジ

| IF # | 方向 | 概要 | API | エラー | セキュリティ | 課金 |
|---|---|---|---|---|---|---|
| #1 | 顧管 → メ | 契約停止イベント送信 | §5 IF #1(送信主管)| E-OP-IF-001-* | §7 監査 | §5 サスペンション |
| #2 | 顧管 → メ | 強制ログアウト送信 | §5 IF #2 | E-OP-IF-002-* | §7 監査 | - |
| #4 | 顧管 → メ | 復元実行 | §5 IF #4 | E-OP-IF-004-* | §7 監査 | - |
| #5 | 顧管 → メ | レート制限上書き | §5 IF #5 | E-OP-IF-005-* | §7 監査 | §3 契約上書き |
| #6 | 顧管 → メ | AI パラメータ上書き | §5 IF #6 | E-OP-IF-006-* | §7 監査 | - |
| #7 | 顧管 → メ | お知らせ生成 | §5 IF #7 | E-OP-IF-007-* | §7 監査 | - |
| #8 | メ → 顧管 | 監視メトリクス取得 | §5 IF #8(受信主管)| - | §10 監視 | - |
| #9 | メ → 顧管 | 不正利用検知通知 | §5 IF #9(受信主管)| - | §10 不正利用検知 | - |
| #10 | 外 → 顧管 → メ | 課金 Webhook 一次受信(Stripe)| §5 IF #10(送信主管)| E-OP-IF-010-* | §7 監査 | §13 Webhook 処理 |
| #12 | 顧管 → メ → 利用者 | 運営者操作通知 | §5 IF #12 | E-OP-IF-012-* | §7 監査 | - |

## 8. 関連ドキュメント

| ドキュメント | 役割 | リンク |
|---|---|---|
| 要件定義 | WHAT(運営者要件)| [../01_要件定義/index.md](../01_要件定義/index.md) |
| 詳細設計 | 実装関連の詳細(モジュール構成 / バッチ / マイグレーション)| [../03_詳細設計/index.md](../03_詳細設計/index.md) |
| 運用設計 | 監視 / バックアップ / ログ / 障害対応 / リリース / 運用手順 | [../04_運用設計/index.md](../04_運用設計/index.md) |
| 将来対応 | 運営者サブロール ほか | [../05_future/index.md](../05_future/index.md) |
| ワイヤーフレーム | 運営者画面表現 | [../画面遷移図.html](../画面遷移図.html) |
| メイン側ドキュメント | 利用者側設計書 | [../../01_メインシステム/02_基本設計/index.md](../../01_メインシステム/02_基本設計/index.md) |
| 共有概念対応表 | メイン / 運営者の正本所在 | [../../共有/共有概念.md](../../共有/共有概念.md) |

## 9. 未確定事項・確認事項

| 確認事項ID | 確認内容 | 関連箇所 | 優先度 | ステータス |
|---|---|---|---|---|
| Q-BASE-OP-001 | (現時点で未確定事項なし — v1.0 リリース時点で全項目確定済み)| - | 低 | 確認済 |

## 10. 変更履歴

| 日付 | 版数 | 変更内容 | 変更者 |
|---|---|---|---|
| 2026-05-17 | 1.0 | 初版作成(新構成への再編)| プロジェクト設計チーム |
