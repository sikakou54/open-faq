<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ [API設計](index.md) ／ **AI 推論 IF**
<!-- /portal-top -->

# AI 推論 IF

> **このページは、AI 回答生成プロバイダを抽象化する内部 IF(`AnswerProvider`)の契約を定義します。**
>
> **このページの API**
>
> - API-AI-001 AI 推論 IF(`AnswerProvider`)

*版数 v1.6 ・ 更新 2026-06-17 ・ 承認済*

## <span id="API-AI-001"></span>API-AI-001 AI 推論 IF(`AnswerProvider`)

回答生成(`generate`)とヘルスチェック(`healthcheck`)を持つ内部抽象インターフェースです。エンドポイントは持たず、MVP は `WorkersAIAnswerProvider` として実装します。

```
export type AnswerResult =
  | { kind: 'answered'; answer: string; cited_faq_ids: string[]; confidence: number }
  | { kind: 'unanswerable'; reason_code: 'no_match'|'low_confidence'|'contradiction' }
  | { kind: 'error'; reason_code: 'provider_error'|'timeout'|'rate_limited' };

export interface AnswerProvider {
  generate(input: {
    question: string;
    candidate_faqs: Array<{ id: string; question: string; answer: string }>;
    policy: { faq_only: true; forbid_new_facts: true; learn: false };
    locale: 'ja-JP';
    timeout_ms: 8000;
  }): Promise<AnswerResult>;

  healthcheck(): Promise<{ ok: boolean; provider: string; model: string }>;
}
```

MVP は Cloudflare Workers AI 実装(`WorkersAIAnswerProvider`)。

**`generate` の戻り値(`AnswerResult`)**

| 項目 | 型 | 説明 |
|----|----|----|
| `kind` | enum | 結果種別(`answered` / `unanswerable` / `error`)。以下の項目は kind により異なる |
| `answer` | string | 　└ `kind=answered` 時の生成回答本文 |
| `cited_faq_ids` | array | 　└ `kind=answered` 時の引用元 FAQ ID 配列(string) |
| `confidence` | number | 　└ `kind=answered` 時の確信度 |
| `reason_code` | enum | 　└ `kind=unanswerable` 時は `no_match` / `low_confidence` / `contradiction`、`kind=error` 時は `provider_error` / `timeout` / `rate_limited` |

**`healthcheck` の戻り値**

| 項目       | 型      | 説明                 |
|------------|---------|----------------------|
| `ok`       | boolean | プロバイダが稼働中か |
| `provider` | string  | プロバイダ名         |
| `model`    | string  | 使用モデル名         |

### 処理概要

回答生成(`generate`)とヘルスチェック(`healthcheck`)を持つ内部抽象インターフェースです。エンドポイントは持たず、MVP は `WorkersAIAnswerProvider` として実装します。

| 処理 ID | 処理内容 |
|----|----|
| P-01 | 質問と候補 FAQ をプロバイダへ渡し回答を生成する(FAQ 範囲限定・新規事実生成禁止) |
| P-02 | 確信度・FAQ 一致状況から回答 / 回答不能 / エラーの種別を判定する |
| P-03 | タイムアウト・レート制限・プロバイダ障害をエラーとして返す |
| P-04 | `healthcheck` でプロバイダ・モデルの稼働状態を返す |

---

<!-- portal-bottom -->
[← API設計](index.md) ・ [基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
