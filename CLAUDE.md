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
- Shared concepts include `accounts.contract_status` (the data-isolation / billing unit, formerly the `tenants.status` column on the now-removed `tenants` table), `case_status`, notification importance, SCR IDs, AC IDs, IF #1-#12, retention classes, legal/privacy constraints, and the **owner-direct-ownership user model** (オーナーアカウント / メンバーアカウント / メンバー権限フラグ / オーナー専有機能 / メンバーのプロジェクト割当; DB tokens `accounts.is_owner` + `accounts.owner_account_id` + `account_permissions` + `account_project_grants` — main is the source of truth).
- `accounts.contract_status` is fixed to `active` / `suspended` / `deleted_pending` / `deleted` and is meaningful only on owner rows (`is_owner=1`). The legacy `tenants` table has been removed (see main basic design v3.3 / detailed design v2.0.13 / migration `0003_drop_tenants_use_owner_account.sql`).
- `case_status=closed` is never set by automatic retention processing. Only admin confirmation, including approval of an operator close request, may close a case.
- Notification importance is `low` / `normal` / `high` / `critical`. `critical` is reserved for events that require mandatory email delivery (delivered to the owner + all members holding the `users:manage` flag in the same owner scope).
- Tenant-side users are split into **owner (exactly one account per contract, all-powers, non-transferable in MVP, self-referenced via `accounts.owner_account_id = accounts.id`)** and **members (0..N, attached to an owner via `owner_account_id`, controlled by member-permission flags: `faq:manage` / `chat:respond` / `users:manage` / `project:manage` / `logs:view`, and by per-project grants in `account_project_grants`)**. Owner-only functions (billing, withdrawal, terms re-consent) cannot be granted to members. Members with zero project grants have access only to the dashboard and project-agnostic features.
- If MVP values are moved out of the main documents, update `future_*.md` so Future rows still describe the current MVP baseline accurately.

## Validation

Run the synchronization smoke check after editing requirement or design documents:

```sh
99_script/check-spec-sync.sh
```

The smoke check is not a full review substitute. It catches high-risk regressions that have caused drift between requirements and basic design.
