# DD10: PII 偽陽性報告(運営者システム)

## 0. 文書情報

| 項目 | 内容 |
|---|---|
| 文書名 | DD10: PII 偽陽性報告(運営者システム) |
| 詳細設計ID | DD10 |
| 対象システム | FAQ AI ウィジェット SaaS / 運営者システム |
| 関連機能ID | FR-060, FR-064, NFR-805, AC-036, D-13 |
| 作成日 | 2026-05-17 |
| 版数 | v1.0 |
| ステータス | 承認済 |

## 1. 対象範囲

| 種別 | ID | 名称 |
|---|---|---|
| 機能 | FR-060 | PII 第 1 層検出(正規表現) |
| 機能 | FR-064 | PII 誤検出報告フロー |
| 受入条件 | AC-036 | PII 3 層 + 報告フロー |
| 画面 | SCR-098 | PII 誤検出報告管理(3 営業日判定) |
| API | `POST /pii-fp-reports` | 報告作成 |
| API | `POST /pii-fp-reports/{id}/transition` | 状態遷移(運営者) |
| API | `POST /pii-rules/revisions` | ルール改定(段階ロールアウト) |
| テーブル | `pii_false_positive_reports` | 報告履歴 |
| テーブル | `pii_rule_revisions` | ルール改定履歴 |

## 2. 収録ロジック・対応章

| 元章 | 元タイトル | 概要 |
|---|---|---|
| §5 SCR-098 | PII 誤検出報告管理画面 | 3 営業日タイマー + ルール改定 |
| §6 PII 機能(参照) | 報告 → 判定 → ルール更新 → KV 即時反映 | D-13 |
| 付録 B.5 | `pii_false_positive_reports.state` | 6 状態遷移 |

## 3. 詳細設計本文

### 3.1 PII 検出層(参考)

メイン側で実装される 3 層検出のうち、本書側で運営する対象:

| 層 | 検出方式 | 主管 | 本書側関与 |
|---|---|---|---|
| 第 1 層 | 正規表現(電話番号 / メール / 住所 / クレカ 等) | メイン実装、ルール本書管理 | KV `pii-rules:regex` 更新 + ロールアウト |
| 第 2 層 | NER 分類器(MVP では機能フラグ OFF) | 将来対応 | KV `feature:pii-layer2:enabled` 制御 |
| 第 3 層 | FAQ 整合性検査(LLM) | メイン | - |

詳細は [基本設計 / セキュリティ設計](../02_基本設計/09_セキュリティ設計.md) §PII を正本とする。

### 3.2 状態遷移(`pii_false_positive_reports.state`)

| From | To | トリガー |
|---|---|---|
| - | reported | 報告転送 |
| reported | under_review | SCR-098 開始(3 営業日タイマー起動) |
| under_review | ruled_false_positive | 判定 |
| under_review | ruled_correct_detection | 判定 |
| ruled_false_positive | rule_updated | KV ルール更新 |
| - | archived | 90 日経過 or rule_updated 後 |

詳細は [DD11_状態遷移詳細.md](DD11_状態遷移詳細.md) §B.5 を参照。

### 3.3 3 営業日判定タイマー(NFR-805)

`under_review` 遷移時点から **3 営業日**(JST、土日祝日除外)以内に `ruled_*` 判定を行う必要がある。超過時に運営者 normal alert。

| 項目 | 仕様 |
|---|---|
| 営業日カウント | JST タイムゾーンで月〜金、祝日マスタ(D-05、年次 11/1 取得)を除外 |
| タイマー駆動 | 1 時間 cron(`OperatorNotifyAggregatorWorker` 内のサブタスク)で `under_review` 状態かつ `last_transition_at + 3 営業日 < now` を検出 |
| 通知 | KV `monitoring:thresholds:pii-fp-pending-3bd` = 0 を超えると `pii_fp_report.transition.overdue` を運営者 normal で通知 |

### 3.4 PII 偽陽性報告作成 API

```yaml
/pii-fp-reports:
  post:
    summary: PII 誤検出報告作成
    parameters:
      - $ref: "#/components/parameters/IdempotencyKey"
      - $ref: "#/components/parameters/XCsrfToken"
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [detectionLayer, sampleText, reason]
            properties:
              detectionLayer: { type: string, enum: [regex, classifier, llm] }
              sampleText: { type: string }
              reason: { type: string }
    responses:
      "201":
        content: { application/json: { schema: { type: object, properties: { reportId: { type: string } } } } }
```

通常はエンドユーザーまたは管理者ユーザー側から連携 IF #8 / #9 経由で報告が転送される。`detectionLayer` でどの層の誤検出かを区別する。

### 3.5 PII ルール改定 API(段階ロールアウト、D-13)

```yaml
/pii-rules/revisions:
  post:
    summary: PII ルール改定(段階ロールアウト)
    parameters:
      - $ref: "#/components/parameters/XOpTicketId"
      - $ref: "#/components/parameters/IdempotencyKey"
      - $ref: "#/components/parameters/XCsrfToken"
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [layer, rules, rolloutPercentage]
            properties:
              layer: { type: string, enum: [regex, classifier] }
              rules: { type: array, items: { type: object } }
              rolloutPercentage: { type: integer, enum: [0, 10, 50, 100] }
    responses:
      "201":
        content: { application/json: { schema: { type: object, properties: { revisionId: { type: string } } } } }
```

| 項目 | 仕様 |
|---|---|
| 反映方式(D-13) | KV `pii-rules:regex` / `pii-rules:classifier` を即時更新、TTL 60 秒で全 Worker に伝播 |
| 過去データ修正 | しない(過去の検出結果は新ルールでは再評価しない) |
| 段階ロールアウト | `feature:pii-rule-rollout:<revision_id>` で 0% / 10% / 50% / 100% 制御 |
| 監査 | `pii_rule.update`(5y、`{revisionId, rolloutPercentage}`) |
| 報告状態遷移 | ルール改定後、対応する `pii_false_positive_reports.state` を `rule_updated` に遷移 |

### 3.6 SCR-098 主要機能

| 機能 | 説明 |
|---|---|
| 報告一覧 | `reported` / `under_review` のフィルタ + 3 営業日タイマー表示(色分け: 緑 = 余裕 / 黄 = 1 日以内 / 赤 = 超過) |
| 報告詳細 | `sampleText` (PII マスク済) + `reason` + `detectionLayer` + 過去判定履歴 |
| 状態遷移ボタン | `under_review` → `ruled_false_positive` / `ruled_correct_detection` |
| ルール改定モーダル | `ruled_false_positive` 後に直接「該当ルールを修正する」モーダルを呼び出し |
| ロールアウト進捗 | KV `feature:pii-rule-rollout:<revision_id>` の現値を確認 + 段階更新 |

### 3.7 ルール改定例

正規表現ルール例:

```json
{
  "layer": "regex",
  "rules": [
    {
      "id": "phone-jp-mobile",
      "pattern": "0[789]0[-\\s]?\\d{4}[-\\s]?\\d{4}",
      "enabled": true,
      "description": "日本の携帯電話番号"
    },
    {
      "id": "credit-card",
      "pattern": "\\d{4}[\\s-]?\\d{4}[\\s-]?\\d{4}[\\s-]?\\d{4}",
      "enabled": true,
      "description": "クレジットカード番号(MOD10 検証は省略、第 3 層で実施)"
    }
  ],
  "rolloutPercentage": 10
}
```

### 3.8 ロールアウト判定アルゴリズム(メイン側で参照)

メインの PII 検出 Worker は次の判定で新ルール採用率を決定する:

```text
function shouldUseNewRevision(revisionId: string, contractOwnerUserId: string): boolean {
    const rollout = KV.get(`feature:pii-rule-rollout:${revisionId}`);
    if (!rollout || rollout.percentage === 0) return false;
    if (rollout.percentage === 100) return true;
    const hash = sha256(`${revisionId}:${contractOwnerUserId}`);
    const bucket = parseInt(hash.substring(0, 4), 16) % 100;  // 0..99
    return bucket < rollout.percentage;
}
```

ハッシュベース判定により、同一オーナーは常に同じバケットに割り当てられる(段階上げでサンプルが移動しない安定性)。

### 3.9 PII マスキング(報告データ)

報告本文(`sampleText`)に含まれる PII は永続化前に伏字化:

| 種別 | マスク方式 | 例 |
|---|---|---|
| 電話番号 | 中央 4 桁 `****` | `090-****-1234` |
| メール | local-part の最初 2 文字以外 `***` | `ab***@example.com` |
| クレカ | 中央 8 桁 `********` | `4111-****-****-1111` |
| 住所 | 番地以下削除 | `東京都千代田区` |

メイン側で実装する PII マスク関数を利用。マスク前の生データは保存しない。

### 3.10 主要エラーコード

| エラー ID | HTTP | 説明 |
|---|---|---|
| `E-OP-PII-001` | 409 | INVALID_STATE_TRANSITION(`reported` → `rule_updated` 等、許可されない直接遷移) |
| `E-OP-PII-002` | 400 | INVALID_RULE_REGEX(正規表現コンパイル失敗) |
| `E-OP-PII-003` | 422 | ROLLOUT_PERCENTAGE_INVALID(0/10/50/100 以外) |
| `E-OP-PII-004` | 410 | REPORT_ARCHIVED(90 日経過、操作不可) |

完全な E-OP-PII-* 一覧は [基本設計 / エラー設計](../02_基本設計/05_エラー設計.md) を正本とする。

## 4. 関連設計

| 種別 | 参照先 |
|---|---|
| 要件 | [../01_要件定義/index.md](../01_要件定義/index.md) |
| 基本設計 | [../02_基本設計/index.md](../02_基本設計/index.md) |
| セキュリティ設計(正本) | [../02_基本設計/09_セキュリティ設計.md](../02_基本設計/09_セキュリティ設計.md) |
| API 設計(正本) | [../02_基本設計/02_API設計.md](../02_基本設計/02_API設計.md) |
| メインテーブル設計 | [../../01_メインシステム/02_基本設計/03_テーブル設計.md](../../01_メインシステム/02_基本設計/03_テーブル設計.md) |
| 関連 DD | [DD07_KV・R2オブジェクト.md](DD07_KV・R2オブジェクト.md) / [DD11_状態遷移詳細.md](DD11_状態遷移詳細.md) |
| 運用設計 | [../04_運用設計/index.md](../04_運用設計/index.md) |
| 将来対応 | [../05_future/index.md](../05_future/index.md) |

## 5. テスト観点

### 5.1 ユニットテスト

- 状態遷移ガード(`reported → rule_updated` 直接遷移拒否)
- 3 営業日計算(JST + 祝日マスタ + 週末除外)
- 正規表現コンパイル検証
- ハッシュベースロールアウト判定(同一 ownerId は同バケット)
- PII マスキング全種別

### 5.2 結合テスト(Miniflare)

- 報告作成 → `under_review` → `ruled_false_positive` → ルール改定 → `rule_updated`
- KV `pii-rules:regex` 更新後 60 秒以内のメイン側参照で反映
- 3 営業日超過で通知発火
- 90 日経過で `archived` 自動遷移

### 5.3 E2E テスト(Playwright)

| テスト ID | シナリオ |
|---|---|
| `e2e-scr098-001` | 報告詳細 → 判定 → ルール改定モーダル → ロールアウト 10% |

### 5.4 品質回帰

| データセット | 件数 |
|---|---|
| PII 第 1 層 | 陽性 100 + 陰性 100 / 各国内パターン |

### 5.5 受入条件マッピング

| AC | 検証手段 |
|---|---|
| AC-036(PII 3 層 + 報告フロー) | 単体 + 報告 E2E + 都度運用 |

## 6. 未確定事項・確認事項

| 確認事項ID | 確認内容 | 優先度 | ステータス |
|---|---|---|---|
| - | v1.0 リリース時点で全項目確定済み | 低 | 確認済 |
