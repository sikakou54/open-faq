# FAQ ドキュメント保守ルール

本ファイルはリポジトリレベルのドキュメント保守ルールの正本であり、要件定義書・基本設計書・詳細設計書から参照される。

## フェーズ境界

| ドキュメント | 範囲 | 含めない内容 |
|---|---|---|
| 要件定義 | WHAT(何を提供するか)、優先度、制約、受入条件 | DDL、API スキーマ、cron 式、Worker 名、実装パラメータ |
| 基本設計 | HOW(システムレベルの方式): アーキテクチャ、画面、状態、データ概念、外部 I/F、セキュリティ、非機能アプローチ | SQL DDL、JSON Schema、関数シグネチャ、具体的な runbook |
| 詳細設計 | 実装可能な仕様: DDL、API、JSON Schema、cron、Queue、マイグレーション、テスト詳細 | 要件定義に紐づかない新規プロダクト要件 |
| Future ドキュメント | MVP 後の候補・設計 / 実装バックログ | MVP 本文ドキュメントからの参照 |

## 変更適用順序

仕様または設計の変更要求があった場合、ユーザーが特定のドキュメントだけを指し示していたとしても、必ず以下の **固定順序** で全層を調査・適用すること。途中で省略すると下流に古い前提が残る。

1. **要件定義** (`01_main/01_requirements.md`、`02_admin/01_requirements.md`) — 当該変更が FR / NFR / BR / AC / SCR 参照を追加・変更・削除するか確認し、まず更新して WHAT を正本化する。
2. **基本設計** (`01_main/02_basic_design.md`、`02_admin/02_basic_design.md`) — 画面表(§5.4.x)、状態・データ概念表、ユースケース行、権限行、外部 I/F、アーキテクチャ説明に伝播。SCR 参照行とユースケース ID の連続性を検証。
3. **ワイヤーフレーム** (`01_main/wireframes.html`、`02_admin/wireframes.html`) — 影響画面ブロックと画面横断 UI(サイドバー、メンバー招待権限の説明文、通知文言など)を更新。ワイヤーフレームは **エンドユーザーから見える UI のみ** を扱い、FR / NFR / DB 列名 / 画面間設計根拠を埋め込まない。
4. **詳細設計** (`01_main/03_detailed_design.md`、`02_admin/03_detailed_design.md`) — 最後に Zod スキーマ、DDL CHECK 制約、API 表、ハンドラのコード例、Queue / cron / マイグレーション注記、監査アクションコードを更新。

各層について、変更により削除・改名された語句(FR ID、列挙値、列名、画面 / 項目ラベル)をファイル内検索して取りこぼしを修正する。最後に `99_script/check-spec-sync.sh` を実行する。ある層に関連内容が無いと判明した場合は、暗黙にスキップせず変更サマリへ明示的に記録する。

## モーダル画面

意味のある状態、バリデーション、業務ロジックを持つモーダルダイアログ(プロジェクト作成 / 編集、規約再同意など)は、呼び出し画面に埋め込まず **独立した画面として SCR ID を付与して定義する**。

- **ID 規約**: 親画面の SCR ID に `-M<n>` サフィックスを付ける。親画面下の最初のモーダルは `SCR-<親>-M1`、同じ親に複数モーダルがあれば `-M2` / `-M3` … (例: SCR-010 の編集モーダル → `SCR-010-M1`)。
- **配置**: モーダル行 / セクション / ワイヤーフレームブロックを、すべてのドキュメントで **親画面の直後** に置く — 要件定義の SCR 一覧、基本設計の SCR 一覧(§5.4)と画面表(§5.4.<親>a / b…)、サイドメニュー除外一覧(§5.6.3)、ワイヤーフレーム(`<div class="screen">` ブロックと TOC エントリ)、詳細設計(§6.<親>a / b…)。SCR ID をアルファベット順にソートすると親画面の直下にモーダルが並ぶ。
- **コンテンツ分割**: 親画面側は「モーダルを開く」操作のみを記載する。入力項目、バリデーション、保存 / キャンセルボタンはすべてモーダル SCR の項目表に記載する。
- **モーダル画面に該当しないもの**: 単純な確認ダイアログ(「本当に削除しますか?」yes/no)や再認証チャレンジは独立 SCR にせず、呼び出しボタンの注記として `(確認ダイアログ)` のままインライン記載する。
- **既存の独立モーダル**(例: SCR-025 規約再同意割込み)は後方互換のため数字 ID を保持し、遡及的なリネームは行わない。`-M<n>` 規約は本ルール導入以降に追加されるモーダルへ適用する。

## 同期ルール

- 共有概念が変更される場合は、同一の変更内で `01_main` と `02_admin` の両ドキュメントを更新する。
- 共有概念には以下を含む: `accounts.contract_status`(データ分離 / 課金単位)、`case_status`、通知重要度、SCR ID、AC ID、IF #1〜#12、retention class、法令 / プライバシー制約、および **オーナー直接所有のユーザーモデル**(オーナーアカウント / メンバーアカウント / メンバー権限フラグ / オーナー専有機能 / メンバーのプロジェクト割当。DB トークン `accounts.is_owner` + `accounts.owner_account_id` + `account_permissions` + `account_project_grants` — メインを正本とする)。
- `accounts.contract_status` は `active` / `suspended` / `deleted_pending` / `deleted` に固定し、オーナー行(`is_owner=1`)でのみ意味を持つ。
- `case_status=closed` は自動 retention 処理で設定しない。管理者の確定(運営者によるクローズ要求の承認を含む)のみがクローズ可能とする。
- 通知重要度は `low` / `normal` / `high` / `critical`。`critical` はメール送信が必須となるイベント(オーナー + 同一オーナースコープで `users:manage` フラグを保持する全メンバーへ配信)に予約。
- 利用者側アカウントは **オーナー(契約あたり 1 アカウント固定、全権、MVP では譲渡不可、`accounts.owner_account_id = accounts.id` で自己参照)** と **メンバー(0..N、`owner_account_id` でオーナーに紐付き、メンバー権限フラグ `faq:manage` / `chat:respond` / `users:manage` / `project:manage` / `logs:view` および `account_project_grants` のプロジェクト割当で制御)** に分かれる。オーナー専有機能(課金、退会、規約再同意)はメンバーに付与できない。プロジェクト割当が 0 のメンバーはダッシュボードとプロジェクト非依存機能のみ利用可能。
- **用語**: テナント概念は完全廃止済み。すべてのドキュメントで 契約 / オーナー / メンバー 用語を使用すること。下記「用語マッピング」参照表以外の場所に `tenant` / `テナント` が出現したら欠陥として修正する。

## 用語マッピング(テナント → オーナー / 契約)

テナント概念は完全廃止済み。すべてのドキュメント(要件定義、基本設計、詳細設計、ワイヤーフレーム HTML、運用)で以下の語彙を使用する。文脈依存で適用すること — 旧文中の "tenant" は用法に応じて **契約**(データ分離 / 課金単位)または **オーナー**(契約を保有するアカウント)へマッピングする。本マッピングは `tenant` / `テナント` が出現してよい **唯一の場所** であり、それ以外はすべて欠陥として扱う。

### A. 日本語表現

| 旧 | 新 | 文脈 |
|---|---|---|
| テナント(一般) | 契約 / オーナー(文脈次第) | Prose |
| テナント単位 | 契約単位 | 課金、規約再同意、IP 許可リスト |
| テナント側ユーザー | 利用者(オーナー / メンバー) | 運営者との対比 |
| テナントオーナー | オーナー(オーナーアカウント) | Prose |
| テナントメンバー | メンバー(メンバーアカウント) | Prose |
| テナント分離 | オーナー境界によるデータ分離 | NFR、セキュリティ |
| テナント横断 | 全契約横断 / サービス全体 | サプレスリスト、HMAC 衝突 |
| テナント表示名 | **削除**(MVP では契約表示名 / 組織名を取得しない。SCR-002 / SCR-016 / 通知テンプレート件名はオーナーのメール識別または SaaS 名 `open-faq` で表現する) | UI、メール件名 |
| テナント設定 | アカウント設定(オーナー設定) | UI、テーブル |
| テナント状態 | 契約状態(`accounts.contract_status` の値) | UI、Prose |
| テナント別 / テナント毎 | 契約別 / オーナー別 | レート制限、利用量 |
| 他テナント | 他契約 | リスク(R-004) |
| テナント A / B | 契約 A / B | テスト例 |
| N テナント | N 契約 | 負荷試験、運用統計 |
| **テナント名(入力項目)** | **削除** | SCR-002 / SCR-016 双方で削除済み。`accounts.contract_display_name` も廃止 |
| テナント管理者 | オーナー / メンバー(ユーザー管理権限保持) | 通知の宛先 |
| テナント代表者 | オーナー(オーナーアカウント) | メール宛先 |
| 招待テナント | 招待オーナー / 招待契約 | リリース prose |
| アクティブテナント数 / 全テナント MAU | アクティブ契約数 / 全契約 MAU | KPI カード |
| テナント業務 / テナント側業務 | 利用者側業務 | 運営者スコープの説明 |
| テナントプレーン | 利用者プレーン | アーキテクチャ |
| テナントロール(admin / end_user) | 利用者ロール(admin / end_user) | 認可 |
| テナント派生鍵 | オーナー派生鍵 | 暗号鍵 |
| テナント値(AI パラメータ優先順) | オーナー値 / 契約値 | AI パラメータスコープ |

### B. 英語識別子

| 旧 | 新 | 文脈 |
|---|---|---|
| `tenant_id`(列) | `owner_account_id` | DDL、SQL、KV |
| `tenantId`(JSON) | `ownerAccountId` | API、JSON Schema |
| `tenants` テーブル | 廃止(参照しない) | DDL |
| `tenant_quota_overrides` | `owner_quota_overrides` | テーブル |
| `tenant_registration_reviews` | `owner_registration_reviews` | テーブル |
| `tenant_settings` | `account_settings`(`is_owner=1`) | テーブル |
| `audience_tenant_ids` | `audience_owner_account_ids` | 列 |
| `TENANT_SUSPENDED` | `CONTRACT_SUSPENDED` | エラーコード |
| `scope: "tenant"` | `scope: "owner"` | API、KV、AI パラメータ |
| `scope IN ('global','tenant','project')` | `scope IN ('global','owner','project')` | CHECK 制約 |
| `scope IN ('my_data_only','all_with_tenant')` | `scope IN ('my_data_only','all_with_owner')` | 削除請求 |
| `tenantKey` / `deriveTenantKey()` | `ownerKey` / `deriveOwnerKey()` | 暗号鍵導出 |
| `tenantName` / `ownerName`(Zod フィールド) | 削除 | SCR-002 / SCR-016 API ともに廃止 |
| `accounts.contract_display_name`(列) | 削除(DDL なし) | DDL(組織表示名は保存しない) |
| `tenant_admin`(source enum) | `member_console` | `account_permissions.source` |
| `idx_*_tenant_*` | `idx_*_owner_*` | インデックス名 |
| `uq_accounts_tenant_owner` | `uq_accounts_owner_unique` | UNIQUE 制約 |
| `auth.tenant_boundary_violation` | `authz.owner_boundary_violation` | 監査アクション |
| `tenant_status_created`(監査) | `contract_status_created` | event_kind |
| `tenant_action_created` | `owner_action_created` | event_kind |
| `tenant_account_unread` | `owner_account_unread` | event_kind |
| `tenant_owner_search` | `owner_search` | インデックス名 |
| `ratelimit:{tenant_id}:{kind}` | `ratelimit:{owner_account_id}:{kind}` | KV キー |
| `ai-params:tenant:abc` | `ai-params:owner:abc` | KV キー |
| `POST .../v1/tenant/forced-logout` | `.../v1/owner/forced-logout` | API URL |
| `"resourceType": "tenant"` | `"resourceType": "owner"` | API レスポンス |
| `tenant_mfa_policy_audit_logs` | `owner_mfa_policy_audit_logs` | Future 監査テーブル |
| `tenant_region_audit_logs` | `owner_region_audit_logs` | Future 監査テーブル |
| `tenant_key_versions` | `owner_key_versions` | Future 鍵ローテーションテーブル |
| `tenant_id`(JSON ログフィールド) | `owner_account_id` | ロギング / 可観測性 |
| `{{$labels.tenant}}` | `{{$labels.owner_account_id}}` | Prometheus アラートラベル |
| `SAMPLE-tenant-NNN` | `SAMPLE-owner-NNN` | ワイヤーフレームのモックデータ |
| `ten_SAMPLE_...` | `own_SAMPLE_...` | 監査の例示 ID |
| `tenant.suspend` / `tenant.restore` / `tenant.physical_delete` | `owner.suspend` / `owner.restore` / `owner.physical_delete` | 監査アクションコード |
| `tenant.legal_review.*` | `owner.legal_review.*` | 監査アクションコード |

## 検証

要件定義書・設計書を編集した後は、同期スモークチェックを実行すること:

```sh
99_script/check-spec-sync.sh
```

このスモークチェックは完全なレビューの代替ではない。要件定義と基本設計のドリフトを引き起こしたことのある高リスクな退行を検出する。
