# DD02: プロジェクト・FAQ 管理

## 0. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | DD02: プロジェクト・FAQ 管理 |
| 詳細設計ID | DD02 |
| 対象システム | FAQ AI ウィジェット SaaS / メインシステム |
| 関連機能ID | FR-040〜048（FAQ CRUD / 公開ガード）/ FR-100〜106（FAQ 改善・下書き生成） |
| 作成日 | 2026-05-17 |
| 版数 | v1.0 |
| ステータス | 承認済 |

## 1. 対象範囲

| 種別 | ID | 名称 |
|---|---|---|
| 機能 | FR-040〜048 | FAQ CRUD / 自動公開禁止 / 公開・取下 / 一括インポート |
| 機能 | FR-100〜106 | FAQ 改善 / AI 下書き生成 / 提案承認 |
| 画面 | SCR-010 | プロジェクト一覧 |
| 画面 | SCR-011 | FAQ 一覧 |
| 画面 | SCR-012 | FAQ 編集 |
| API | `/projects/*` `/faqs/*` | プロジェクト・FAQ 操作 |
| テーブル | `projects` `faqs` `faq_embeddings` `faq_search_fts` | FAQ 基盤 |

## 2. 収録ロジック・対応章

| 元章 | 元タイトル | 概要 |
|---|---|---|
| §6 SCR-010〜012 | 画面詳細設計 | プロジェクト一覧 / FAQ 一覧 / FAQ 編集（正本は基本設計） |
| §7 | 機能詳細設計（FAQ 関連） | FAQ CRUD / 公開ガード / 一括インポート（正本は基本設計） |
| §9 | データベース詳細設計 | `projects` / `faqs` テーブル詳細（正本は基本設計） |
| §3.3.1 | `worker-main-api` モジュール構成 | `routes/projects.ts` `routes/faqs.ts` |

## 3. 詳細設計本文

### 3.1 画面詳細設計（参照のみ）

SCR-010 プロジェクト一覧 / SCR-011 FAQ 一覧 / SCR-012 FAQ 編集の画面詳細は [../02_基本設計/01_画面設計.md](../02_基本設計/01_画面設計.md) を正本とする。メッセージ ID は [../02_基本設計/06_メッセージ一覧.md](../02_基本設計/06_メッセージ一覧.md) を参照。

### 3.2 機能詳細設計（参照のみ）

FAQ CRUD / 公開ガード / 一括インポート / AI 改善提案の全項目は [../02_基本設計/02_API設計.md](../02_基本設計/02_API設計.md) を正本とする。

### 3.3 データベース詳細設計（参照のみ）

`projects` / `faqs` / `faq_embeddings` / `faq_search_fts` の DDL、CHECK 制約、インデックス、外部キー、コード値、SaaS データ分離観点（`owner_account_id`）、保持期間は [../02_基本設計/03_テーブル設計.md](../02_基本設計/03_テーブル設計.md) を正本とする。

### 3.4 実装モジュール構成

```
src/
├── routes/
│   ├── projects.ts           # /projects/* CRUD + メンバー割当
│   └── faqs.ts               # /faqs/* CRUD + 公開 / 取下 / 一括インポート / 提案承認
├── handlers/
├── domain/
│   └── faq-status.ts         # FAQ 状態遷移（draft / review / published / unpublished）
├── repository/
│   ├── projects.ts
│   ├── faqs.ts
│   └── faq-embeddings.ts
├── adapter/
│   └── workers-ai-answer-provider.ts # generateFaqDraft 実装
└── middleware/
    └── authorize.ts          # requireProject / requireRole 連動
```

### 3.5 FAQ 自動公開禁止（AC-006）

`faqs.status` は CHECK 制約で値域固定。`status='published'` への遷移は人手承認 API（`POST /api/v1/faqs/{id}/publish`）のみ許可、AI 経由の直接公開は不可。`domain/faq-status.ts` の `canTransition()` で `draft → published` を拒否、`review → published` のみ許可する。

### 3.6 FTS5 検索

`faq_search_fts` は SQLite の FTS5 virtual table で構築し、`faqs.title || faqs.body` をインデックス対象とする。FAQ 公開・更新時に同期更新。検索クエリは BM25 ランキングを利用：

```sql
SELECT f.*, bm25(faq_search_fts) AS rank
FROM faq_search_fts JOIN faqs f ON f.rowid = faq_search_fts.rowid
WHERE faq_search_fts MATCH ?1 AND f.project_id = ?2 AND f.status = 'published'
ORDER BY rank LIMIT 20
```

詳細は [DD03_AI回答パイプライン.md](DD03_AI回答パイプライン.md) §3.2 関連度計算を参照。

### 3.7 埋め込みベクトル事前計算

FAQ 公開時に `@cf/baai/bge-base-en-v1.5` で埋め込みベクトルを計算し、`faq_embeddings` テーブル（または KV `embedding:{faqId}`）に保存。AI 推論時のリランキング用。

### 3.8 AI 下書き生成（FR-100〜106）

`POST /api/v1/faqs/draft` で AnswerProvider の `generateFaqDraft(input)` を呼び出し、提案文を返す。`handlers/faqs/draft.ts` で生成結果を `faqs` テーブルに `status='draft'` で INSERT し、`writeAudit({action: 'faq.draft.generate'})` で監査記録。

### 3.9 一括インポート（`faq.bulk_import`）

CSV / JSON ファイル → R2 ステージング → Queue 投入 → consumer が分割 INSERT。1 リクエスト最大 1000 件。詳細は [DD14_バッチ・非同期処理.md](DD14_バッチ・非同期処理.md) を参照。

### 3.10 リミット

| 項目 | 警告 | 拒否 |
|---|---|---|
| FAQ 件数 / 契約 | 8,000 | 12,000（409 `FAQ_LIMIT_EXCEEDED`） |
| プロジェクト数 / 契約 | 40 | 50（409 `PROJECT_LIMIT_EXCEEDED`） |

### 3.11 関連する横断設計

- 認可: [DD09_認可ヘルパ.md](DD09_認可ヘルパ.md) の `requireProject` でオーナー境界 + プロジェクト割当を検証
- 監査ログ: `faq.create` / `faq.update` / `faq.publish` / `faq.unpublish` / `faq.bulk_import` を `retention_class=general` で記録
- リアルタイム反映: FAQ 公開・編集時に `widget-api` 側の KV キャッシュ（`embedding:{faqId}`、`ai_threshold:{owner}:{project}` は別系統）を invalidate

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
| 関連 DD | [DD03_AI回答パイプライン.md](DD03_AI回答パイプライン.md) / [DD09_認可ヘルパ.md](DD09_認可ヘルパ.md) / [DD10_監査ログ書込・完全性検証.md](DD10_監査ログ書込・完全性検証.md) / [DD13_ウィジェット配信.md](DD13_ウィジェット配信.md) |

## 5. テスト観点

| AC ID | テスト ID | テスト方式 | テストファイル |
|---|---|---|---|
| AC-006 | `u-faq-publish-001` / `it-faq-publish-001` | Unit + Integration | `workers/main-api/test/{unit,integration}/faq/publish-guard.test.ts` |
| AC-014 | `e2e-faq-crud-001` | E2E | `apps/admin/e2e/faq/crud.spec.ts` |

### 5.1 その他観点

| 観点 | 内容 |
|---|---|
| 単体 | `faq-status.ts` 遷移ガード全パターン |
| 結合 | FTS5 検索の MATCH 構文 / BM25 ランキング |
| 異常系 | 他オーナーのプロジェクトに対する FAQ CRUD アクセス時 404 |
| 境界値 | FAQ 件数 7999 / 8000 / 8001 / 11999 / 12000 / 12001 |
| 権限 | `faq:manage` フラグ無メンバーによる FAQ 編集時 403 |
| 性能 | `POST /api/v1/faqs/{id}/publish` p95 < 300ms（UPDATE 1 行 + KV invalidate） |

## 6. 未確定事項・確認事項

| 確認事項ID | 確認内容 | 優先度 | ステータス |
|---|---|---|---|
| - | v1.0 リリース時点で全項目確定済み | 低 | 確認済 |
