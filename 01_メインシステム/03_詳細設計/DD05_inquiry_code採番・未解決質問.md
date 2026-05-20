# DD05: inquiry_code 採番・未解決質問

## 0. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | DD05: inquiry_code 採番・未解決質問 |
| 詳細設計ID | DD05 |
| 対象システム | FAQ AI ウィジェット SaaS / メインシステム |
| 関連機能ID | FR-070〜079（未解決質問一覧 / 詳細 / 状態遷移）/ FR-072（inquiry_code 採番）/ AC-010 / AC-012 / AC-013 |
| 作成日 | 2026-05-17 |
| 版数 | v1.0 |
| ステータス | 承認済 |

## 1. 対象範囲

| 種別 | ID | 名称 |
|---|---|---|
| 機能 | FR-070〜079 | 未解決質問一覧 / 詳細 / 状態遷移（5 値） |
| 機能 | FR-072 | inquiry_code 採番（`INQ-YYYYMMDD-XXXXXXXX`） |
| 画面 | SCR-011 | FAQ 一覧（未解決質問は派生表示） |
| API | `/inquiries/*` | 未解決質問操作 |
| テーブル | `inquiries` | 未解決質問 |

## 2. 収録ロジック・対応章

| 元章 | 元タイトル | 概要 |
|---|---|---|
| §10.3 | inquiry_code 採番 | Base32 + 衝突 1.1×10^12 / リトライ最大 3 回 |
| §6 SCR-011 | FAQ 一覧 | 未解決質問派生表示（正本は基本設計） |
| §7 | 機能詳細設計（未解決質問関連） | 状態遷移 5 値（正本は基本設計） |
| §14.1.4-14.1.5 | 730 日保持期間処理 | 未解決質問の保持期間通知 + 物理削除 |

## 3. 詳細設計本文

### 3.1 inquiry_code 採番

```ts
// app/shared/src/lib/inquiry-code.ts
const BASE32 = 'ABCDEFGHJKLMNPQRSTVWXYZ23456789';  // 紛らわしい文字除外

export function generateInquiryCode(now = new Date()): string {
  const yyyymmdd = now.toISOString().slice(0, 10).replace(/-/g, '');
  let suffix = '';
  const rand = crypto.getRandomValues(new Uint8Array(8));
  for (let i = 0; i < 8; i++) suffix += BASE32[rand[i] % 32];
  return `INQ-${yyyymmdd}-${suffix}`;
}
```

衝突確率: 32^8 ≈ 1.1 × 10^12。日次 100 万件でも 4 × 10^-7。UNIQUE インデックス（`uq_inquiries_code`）違反時はリトライ（最大 3 回）。

### 3.2 未解決質問画面（参照のみ）

未解決質問一覧 / 詳細 / 状態遷移は [../02_基本設計/01_画面設計.md](../02_基本設計/01_画面設計.md) を正本とする。`case_status` の 5 値（`open` / `in_progress` / `waiting_user` / `resolved` / `closed`）の遷移ガードは [../02_基本設計/03_テーブル設計.md](../02_基本設計/03_テーブル設計.md) §4.5.2 を正本とする。

### 3.3 未解決質問の保持期間通知（cron JST 09:00）

`case_status='open'` の未解決質問が保持期間に近づいた場合に、管理者ユーザーへ滞留通知を送信する。案件状態は変更しない。詳細は [DD14_バッチ・非同期処理.md](DD14_バッチ・非同期処理.md) §14.1.4 を参照。

### 3.4 730 日保持期間処理（cron JST 02:00）

```ts
export async function processOpenInquiryRetention(env: Env) {
  const cutoff = new Date(Date.now() - 730 * 86400000).toISOString();
  const stuck = await env.DB.prepare(`
    SELECT id, contract_owner_user_id, case_status FROM inquiries
    WHERE case_status = 'open'
      AND created_at <= ?1
      AND deleted_at IS NULL
  `).bind(cutoff).all();
  for (const i of stuck.results) {
    await enqueueNotification(env, {
      contractOwnerUserId: i.contract_owner_user_id, kind: 'OPEN_INQUIRY_RETENTION_NOTICE',
      refType: 'inquiry', refId: i.id,
    });
    await writeAudit(env, {
      action: 'inquiry.retention_notice', contractOwnerUserId: i.contract_owner_user_id, targetId: i.id,
      retentionClass: 'general',
    });
  }
}
```

> **注**: `case_status='closed'` は自動 retention 処理で設定しない。管理者の確定（運営者によるクローズ要求の承認を含む）のみがクローズ可能。

### 3.5 実装モジュール構成

```
src/
├── routes/
│   └── inquiries.ts          # /inquiries/* CRUD + 状態遷移
├── handlers/
├── domain/
│   └── inquiry-status.ts     # case_status 5 値の遷移ガード
├── repository/
│   └── inquiries.ts
└── lib/
    └── inquiry-code.ts       # generateInquiryCode（@faq-saas/shared 経由）
```

## 4. 関連設計

| 種別 | 参照先 |
|---|---|
| 要件 | [../01_要件定義/index.md](../01_要件定義/index.md) |
| 基本設計 | [../02_基本設計/index.md](../02_基本設計/index.md) |
| 画面設計 | [../02_基本設計/01_画面設計.md](../02_基本設計/01_画面設計.md) |
| テーブル設計 | [../02_基本設計/03_テーブル設計.md](../02_基本設計/03_テーブル設計.md) |
| API 設計 | [../02_基本設計/02_API設計.md](../02_基本設計/02_API設計.md) |
| 運用設計 | [../04_運用設計/index.md](../04_運用設計/index.md) |
| 将来対応 | [../05_future/index.md](../05_future/index.md) |
| 関連 DD | [DD06_個別チャット.md](DD06_個別チャット.md) / [DD07_通知ロジック.md](DD07_通知ロジック.md) / [DD14_バッチ・非同期処理.md](DD14_バッチ・非同期処理.md) |

## 5. テスト観点

| AC ID | テスト ID | テスト方式 | テストファイル |
|---|---|---|---|
| AC-010 | `e2e-inquiry-flow-001` | E2E | `apps/admin/e2e/inquiries/flow.spec.ts` |
| AC-012 | `u-inquiry-transition-001` | Unit | `workers/main-api/test/unit/inquiry/transition.test.ts` |
| AC-013 | `u-inquiry-code-001` | Unit | `workers/main-api/test/unit/inquiry/code-issue.test.ts` |

### 5.1 単体テスト例

```ts
// tests/unit/domain/inquiry-status-transition.test.ts
import { describe, it, expect } from 'vitest';
import { canTransition, assertTransition } from '@faq-saas/shared';

describe('inquiry status transition', () => {
  it('closed → open は拒否', () => {
    expect(canTransition('closed', 'open')).toBe(false);
  });
  it('assertTransition は不正遷移で throw', () => {
    expect(() => assertTransition('closed', 'open')).toThrow('INVALID_STATE');
  });
});
```

### 5.2 その他観点

| 観点 | 内容 |
|---|---|
| 単体 | `generateInquiryCode` 衝突リトライ最大 3 回 / `case_status` 全 5 値遷移 |
| 結合 | inquiry_code UNIQUE 制約違反 → リトライ → 成功 |
| 異常系 | `closed → open` 等の不正遷移は 422 `INVALID_STATE` |
| 境界値 | 保持期間 729 / 730 / 731 日経過時の通知挙動 |
| 性能 | `GET /api/v1/inquiries` p95 < 500ms（`idx_inquiries_contract_status_created` 利用） |

## 6. 未確定事項・確認事項

| 確認事項ID | 確認内容 | 優先度 | ステータス |
|---|---|---|---|
| - | v1.0 リリース時点で全項目確定済み | 低 | 確認済 |
