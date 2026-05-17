# DD04: AI しきい値 3 階層適用

## 0. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | DD04: AI しきい値 3 階層適用 |
| 詳細設計ID | DD04 |
| 対象システム | FAQ AI ウィジェット SaaS / メインシステム |
| 関連機能ID | FR-340 / FR-341（AI しきい値プロジェクト / オーナー / グローバル の 3 階層適用）/ AC-038 |
| 作成日 | 2026-05-17 |
| 版数 | v1.0 |
| ステータス | 承認済 |

## 1. 対象範囲

| 種別 | ID | 名称 |
|---|---|---|
| 機能 | FR-340 / FR-341 | AI しきい値 3 階層適用 |
| 受入 | AC-038 | AI しきい値 3 階層 |
| API | `POST /widget/v1/ask` | しきい値取得を内包 |
| API | `POST /internal/admin-integration/v1/threshold/*` | IF #6 受信側 |
| API | `POST /internal/admin-integration/v1/cache/ai-threshold/invalidate` | 明示的キャッシュ無効化 |
| テーブル | `ai_threshold_persistent_cache` | 永続キャッシュ |
| KV | `ai_threshold:{owner}:{project}` | TTL 60s キャッシュ |

## 2. 収録ロジック・対応章

| 元章 | 元タイトル | 概要 |
|---|---|---|
| §10.2.1 | 取得フロー | 3 階層 (KV → D1 永続 → グローバル既定) |
| §10.2.2 | KV TTL 60s + 永続キャッシュ更新 | IF #6 受信時の両更新 |
| §10.2.3 | フォールバック発動アラート | KPI 監視 |
| §10.2.4 | 明示的キャッシュ無効化 | invalidate API |

## 3. 詳細設計本文

### 3.1 取得フロー

```ts
// app/workers/widget-api/src/domain/ai-threshold.ts
export async function getThreshold(env: Env, ownerAccountId: string, projectId: string): Promise<{
  confidenceThreshold: number;
  relevanceThreshold: number;
  source: 'kv' | 'persistent' | 'global_default';
}> {
  // 1) KV (TTL 60s)
  const kvKey = `ai_threshold:${ownerAccountId}:${projectId}`;
  const kvHit = await env.KV_CACHE.get<Threshold>(kvKey, 'json');
  if (kvHit) return { ...kvHit, source: 'kv' };

  // 2) 連携 IF #6 経由で受信したものが KV 反映されている前提。
  //    KV miss なら D1 永続キャッシュへフォールバック
  const persistent = await env.DB.prepare(`
    SELECT confidence_threshold, relevance_threshold FROM ai_threshold_persistent_cache
    WHERE (scope='project' AND project_id=?1)
       OR (scope='owner' AND owner_account_id=?2)
       OR (scope='global')
    ORDER BY CASE scope WHEN 'project' THEN 0 WHEN 'owner' THEN 1 ELSE 2 END
    LIMIT 1
  `).bind(projectId, ownerAccountId).first<Threshold>();
  if (persistent) {
    await env.KV_CACHE.put(kvKey, JSON.stringify(persistent), { expirationTtl: 60 });
    return { ...persistent, source: 'persistent' };
  }

  // 3) グローバル既定値
  await enqueueServiceAlert(env, {
    level: 'normal', message: `AI しきい値フォールバック発動: owner=${ownerAccountId}`,
  });
  return { confidenceThreshold: 0.60, relevanceThreshold: 0.50, source: 'global_default' };
}
```

### 3.2 KV TTL 60s + 永続キャッシュ更新

IF #6 受信時に KV (`expirationTtl: 60`) と D1 (`ai_threshold_persistent_cache`) の両方を更新。KV ミス時は D1 から再ロード。

### 3.3 フォールバック発動アラート

グローバル既定値にフォールバックした場合、毎時集計で件数を KPI として監視。

### 3.4 明示的キャッシュ無効化

`POST /internal/admin-integration/v1/cache/ai-threshold/invalidate` で KV キーを削除し、次回アクセス時に D1 から再ロード。

## 4. 関連設計

| 種別 | 参照先 |
|---|---|
| 要件 | [../01_要件定義/index.md](../01_要件定義/index.md) |
| 基本設計 | [../02_基本設計/index.md](../02_基本設計/index.md) |
| API 設計 | [../02_基本設計/02_API設計.md](../02_基本設計/02_API設計.md) |
| 運用設計 | [../04_運用設計/index.md](../04_運用設計/index.md) |
| 将来対応 | [../05_future/index.md](../05_future/index.md) |
| 関連 DD | [DD03_AI回答パイプライン.md](DD03_AI回答パイプライン.md) / [DD13_ウィジェット配信.md](DD13_ウィジェット配信.md) |

## 5. テスト観点

| AC ID | テスト ID | テスト方式 | テストファイル |
|---|---|---|---|
| AC-038 | `it-ai-threshold-001` | Integration | `workers/main-api/test/integration/ai/threshold-3layer.test.ts` |

### 5.1 その他観点

| 観点 | 内容 |
|---|---|
| 単体 | `getThreshold` の 3 階層分岐（project / owner / global）全網羅 |
| 結合 | IF #6 受信 → KV + D1 更新 → 後続 `/widget/v1/ask` で反映確認 |
| 異常系 | KV / D1 両方失敗時のグローバル既定値フォールバック発動 |
| 境界値 | scope 優先順位（project > owner > global）の最優先一致が選ばれる |
| 性能 | `/widget/v1/ask` 内でのしきい値取得は KV キャッシュヒット時 < 10ms |

## 6. 未確定事項・確認事項

| 確認事項ID | 確認内容 | 優先度 | ステータス |
|---|---|---|---|
| - | v1.0 リリース時点で全項目確定済み | 低 | 確認済 |
