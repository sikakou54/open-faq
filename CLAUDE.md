# FAQ Document Maintenance Rules

This file is the repository-level source for document maintenance rules referenced by the requirements, basic design, and detailed design documents.

## Phase Boundary

| Document | Scope | Do not include |
|---|---|---|
| Requirements | WHAT to deliver, priority, constraints, acceptance conditions | DDL, API schema, cron expressions, Worker names, implementation parameters |
| Basic design | HOW at system level: architecture, screens, state, data concepts, external I/F, security, non-functional approach | SQL DDL, JSON Schema, function signatures, concrete runbooks |
| Detailed design | Implementable specifications: DDL, API, JSON Schema, cron, queue, migration, test details | New product requirements not traceable to requirements |
| Future documents | Post-MVP candidates and design/implementation backlog | References from MVP body documents |

## Sync Rules

- When a shared concept changes, update both `01_main` and `02_admin` documents in the same change.
- Shared concepts include `accounts.contract_status` (the data-isolation / billing unit), `case_status`, notification importance, SCR IDs, AC IDs, IF #1-#12, retention classes, legal/privacy constraints, and the **owner-direct-ownership user model** (オーナーアカウント / メンバーアカウント / メンバー権限フラグ / オーナー専有機能 / メンバーのプロジェクト割当; DB tokens `accounts.is_owner` + `accounts.owner_account_id` + `account_permissions` + `account_project_grants` — main is the source of truth).
- `accounts.contract_status` is fixed to `active` / `suspended` / `deleted_pending` / `deleted` and is meaningful only on owner rows (`is_owner=1`).
- `case_status=closed` is never set by automatic retention processing. Only admin confirmation, including approval of an operator close request, may close a case.
- Notification importance is `low` / `normal` / `high` / `critical`. `critical` is reserved for events that require mandatory email delivery (delivered to the owner + all members holding the `users:manage` flag in the same owner scope).
- Customer-side accounts are split into **owner (exactly one account per contract, all-powers, non-transferable in MVP, self-referenced via `accounts.owner_account_id = accounts.id`)** and **members (0..N, attached to an owner via `owner_account_id`, controlled by member-permission flags: `faq:manage` / `chat:respond` / `users:manage` / `project:manage` / `logs:view`, and by per-project grants in `account_project_grants`)**. Owner-only functions (billing, withdrawal, terms re-consent) cannot be granted to members. Members with zero project grants have access only to the dashboard and project-agnostic features.
- **Terminology**: the tenant concept has been fully retired. All documents must use 契約 / オーナー / メンバー vocabulary. Any occurrence of `tenant` / `テナント` outside the Terminology Mapping reference table below is a defect to be fixed.

## Terminology Mapping (Tenant → Owner / Contract)

The tenant concept has been fully retired. All documents (requirements, basic design, detailed design, wireframes HTML, operations) use the following vocabulary. Apply contextually — "tenant" in legacy text maps to either **contract** (data-isolation / billing unit) or **owner** (account that owns the contract) depending on usage. This mapping is the **only** place where `tenant` / `テナント` may appear; everywhere else they are defects.

### A. Japanese prose

| Old | New | Context |
|---|---|---|
| テナント（一般） | 契約 / オーナー（文脈次第） | Prose |
| テナント単位 | 契約単位 | Billing, terms re-consent, IP allowlist |
| テナント側ユーザー | 利用者（オーナー / メンバー） | Contrast with operator |
| テナントオーナー | オーナー（オーナーアカウント） | Prose |
| テナントメンバー | メンバー（メンバーアカウント） | Prose |
| テナント分離 | オーナー境界によるデータ分離 | NFR, security |
| テナント横断 | 全契約横断 / サービス全体 | Suppression list, HMAC collision |
| テナント表示名 | サービス名 / 組織名 | UI, email subject |
| テナント設定 | アカウント設定（オーナー設定） | UI, table |
| テナント状態 | 契約状態 (values from `accounts.contract_status`) | UI, prose |
| テナント別 / テナント毎 | 契約別 / オーナー別 | Rate limits, usage |
| 他テナント | 他契約 | Risks (R-004) |
| テナント A / B | 契約 A / B | Test examples |
| N テナント | N 契約 | Load test, ops stats |
| **テナント名（入力項目）** | **削除** | SCR-002 only |
| テナント管理者 | オーナー / メンバー（ユーザー管理権限保持） | Notification audience |
| テナント代表者 | オーナー（オーナーアカウント） | Email recipient |
| 招待テナント | 招待オーナー / 招待契約 | Release prose |
| アクティブテナント数 / 全テナント MAU | アクティブ契約数 / 全契約 MAU | KPI cards |
| テナント業務 / テナント側業務 | 利用者側業務 | Operator scope description |
| テナントプレーン | 利用者プレーン | Architecture |
| テナントロール (admin / end_user) | 利用者ロール (admin / end_user) | Auth |
| テナント派生鍵 | オーナー派生鍵 | Encryption |
| テナント値 (AI parameter precedence) | オーナー値 / 契約値 | AI parameter scope |

### B. English identifiers

| Old | New | Context |
|---|---|---|
| `tenant_id` (column) | `owner_account_id` | DDL, SQL, KV |
| `tenantId` (JSON) | `ownerAccountId` | API, JSON Schema |
| `tenants` table | Retired (do not reference) | DDL |
| `tenant_quota_overrides` | `owner_quota_overrides` | Table |
| `tenant_registration_reviews` | `owner_registration_reviews` | Table |
| `tenant_settings` | `account_settings` (`is_owner=1`) | Table |
| `audience_tenant_ids` | `audience_owner_account_ids` | Column |
| `TENANT_SUSPENDED` | `CONTRACT_SUSPENDED` | Error code |
| `scope: "tenant"` | `scope: "owner"` | API, KV, AI parameters |
| `scope IN ('global','tenant','project')` | `scope IN ('global','owner','project')` | CHECK constraint |
| `scope IN ('my_data_only','all_with_tenant')` | `scope IN ('my_data_only','all_with_owner')` | Deletion request |
| `tenantKey` / `deriveTenantKey()` | `ownerKey` / `deriveOwnerKey()` | Crypto key derivation |
| `tenantName` (Zod field) | Removed | SCR-002 API |
| `tenant_admin` (source enum) | `member_console` | `account_permissions.source` |
| `idx_*_tenant_*` | `idx_*_owner_*` | Index naming |
| `uq_accounts_tenant_owner` | `uq_accounts_owner_unique` | UNIQUE constraint |
| `auth.tenant_boundary_violation` | `authz.owner_boundary_violation` | Audit action |
| `tenant_status_created` (audit) | `contract_status_created` | event_kind |
| `tenant_action_created` | `owner_action_created` | event_kind |
| `tenant_account_unread` | `owner_account_unread` | event_kind |
| `tenant_owner_search` | `owner_search` | Index name |
| `ratelimit:{tenant_id}:{kind}` | `ratelimit:{owner_account_id}:{kind}` | KV key |
| `ai-params:tenant:abc` | `ai-params:owner:abc` | KV key |
| `POST .../v1/tenant/forced-logout` | `.../v1/owner/forced-logout` | API URL |
| `"resourceType": "tenant"` | `"resourceType": "owner"` | API response |
| `tenant_mfa_policy_audit_logs` | `owner_mfa_policy_audit_logs` | Future audit table |
| `tenant_region_audit_logs` | `owner_region_audit_logs` | Future audit table |
| `tenant_key_versions` | `owner_key_versions` | Future key rotation table |
| `tenant_id` (JSON log field) | `owner_account_id` | Logging / observability |
| `{{$labels.tenant}}` | `{{$labels.owner_account_id}}` | Prometheus alert label |
| `SAMPLE-tenant-NNN` | `SAMPLE-owner-NNN` | Wireframes mock data |
| `ten_SAMPLE_...` | `own_SAMPLE_...` | Audit example IDs |
| `tenant.suspend` / `tenant.restore` / `tenant.physical_delete` | `owner.suspend` / `owner.restore` / `owner.physical_delete` | Audit action codes |
| `tenant.legal_review.*` | `owner.legal_review.*` | Audit action codes |

## Validation

Run the synchronization smoke check after editing requirement or design documents:

```sh
99_script/check-spec-sync.sh
```

The smoke check is not a full review substitute. It catches high-risk regressions that have caused drift between requirements and basic design.
