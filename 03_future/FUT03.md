<!-- portal-top -->
[設計ポータル](../README.md) ／ [将来対応](index.md) ／ **FUT03: 国際化・リージョン**
<!-- /portal-top -->

# FUT03: 国際化・リージョン

## <span id="0-文書情報"></span>0. 文書情報

| 項目         | 内容                                      |
|--------------|-------------------------------------------|
| 文書名       | FUT03: 国際化・リージョン                 |
| 将来対応ID   | FUT-03                                    |
| 対象システム | FAQ AI ウィジェット SaaS / メインシステム |
| 作成日       | 2026-05-17                                |
| 版数         | v1.0                                      |
| ステータス   | 検討中(MVP 外)                            |

------------------------------------------------------------------------

## <span id="1-概要"></span>1. 概要

| 項目 | 内容 |
|----|----|
| 概要 | MVP では日本語のみ・日本リージョン(apac)のみ・表示 TZ JST 固定で提供する国際化・リージョン領域について、Post-MVP で多言語 UI / マルチリージョン / 管理者単位タイムゾーンを段階導入する。 |
| 背景 | 海外契約・海外拠点管理者のユースケースを取り込むには、UI 多言語化、データ越境制限、TZ 上書きの 3 軸が必要となる。 |
| 期待効果 | 海外顧客の獲得余地、越境データ保護規制(GDPR / CCPA 等)との整合性向上、海外拠点管理者の操作性向上。 |
| 優先度(将来対応内) | 中 |
| 想定時期 | T2(ベータ判定まで)〜 T3(GA 判定まで) |

------------------------------------------------------------------------

## <span id="2-関連要件候補"></span>2. 関連要件・候補

### <span id="21-要件候補将来-fr"></span>2.1 要件候補(将来 FR)

#### <span id="国際化リージョン"></span>国際化・リージョン

| ID | 要件候補 | MVP の前提 | 判定時期 | 判定基準 / 完了条件 |
|----|----|----|----|----|
| FUT-REQ-I18N-001 | 多言語 UI | 日本語のみ | ベータ / GA | 英語追加の需要、翻訳品質、サポート体制をもとに判定し、GA では en / ja 同等品質を目標とする |
| FUT-REQ-I18N-002 | マルチリージョン | 日本リージョン(apac)のみ | ベータ / GA | ベータで region 属性導入を評価し、GA で `apac` / `wnam` / `eeur` などの選択可否を判定 |
| FUT-REQ-I18N-003 | 管理者単位タイムゾーン上書き | 表示 TZ は JST 固定、データ層は UTC | GA | 多言語化と併せて評価し、海外拠点管理者の利用頻度と UI 複雑度をもとに判定 |

### <span id="22-基本設計論点"></span>2.2 基本設計論点

#### <span id="国際化リージョン-1"></span>国際化・リージョン

| 項目 | 基本設計で具体化すること | 関連 Future 要件 |
|----|----|----|
| 多言語 UI | 翻訳キー管理、文言レビュー、メール・受信箱・ウィジェットの言語選択、言語未対応時のフォールバック | FUT-REQ-I18N-001 |
| マルチリージョン | 契約発行時の region 決定、データ配置、越境移転ガード | FUT-REQ-I18N-002 |
| 管理者単位 TZ | 契約 TZ と個人 TZ の優先順位、監査ログ時刻表示、レポート集計境界 | FUT-REQ-I18N-003 |

### <span id="23-詳細設計バックログ"></span>2.3 詳細設計バックログ

#### <span id="マルチリージョンddl-候補"></span>マルチリージョン(DDL 候補)

```sql
-- 契約オーナー専有属性に追加(v1.11 で 2 マスタ完全分離: `M_OWNERS` / `M_PRJ_USERS` / `M_PRJ_USER_ASGN` へ再編済み)
ALTER TABLE M_OWNERS
  ADD COLUMN region TEXT NOT NULL DEFAULT 'apac'
  CHECK (region IN ('apac', 'wnam', 'eeur'));

CREATE TABLE owner_region_audit_logs (
  id                      TEXT PRIMARY KEY,
  owner_id  TEXT NOT NULL REFERENCES M_OWNERS(id) ON DELETE CASCADE,
  before_region           TEXT NOT NULL,
  after_region            TEXT NOT NULL,
  approved_by             TEXT REFERENCES M_OWNERS(id) ON DELETE SET NULL,
  reason                  TEXT NOT NULL,
  created_at              TEXT NOT NULL
);
```

#### <span id="実装設計バックログ関連分"></span>実装設計バックログ(関連分)

| ID | 対象 | 実装設計で具体化すること | 関連 Future 要件 |
|----|----|----|----|
| FUT-DD-I18N-001 | 多言語 UI | i18n key 管理、メールテンプレート多言語化、fallback、翻訳差分 CI | FUT-REQ-I18N-001 |
| FUT-DD-I18N-002 | マルチリージョン | `M_OWNERS.region`、routing、D1 / R2 配置、region guard、越境拒否 API | FUT-REQ-I18N-002 |
| FUT-DD-I18N-003 | 管理者単位 TZ | profile setting、日付フォーマット、集計境界、監査ログ UTC 正本との変換 | FUT-REQ-I18N-003 |

#### <span id="api--worker-候補関連分"></span>API / Worker 候補(関連分)

| 領域 | 候補 |
|----|----|
| マルチリージョン | `TenantRegionGuard`、`POST /admin/v1/owners/{id}/region-approval` |

#### <span id="テスト検証候補関連分"></span>テスト・検証候補(関連分)

| 領域 | 検証項目 |
|----|----|
| 多言語 | 翻訳キー欠落、メールテンプレート、日付・数値フォーマット、a11y |
| マルチリージョン | region guard、越境拒否、D1 / R2 配置、監査ログの region 記録 |

------------------------------------------------------------------------

## <span id="3-影響範囲"></span>3. 影響範囲

| 種別 | 影響内容 |
|----|----|
| 要件 | NFR-069(言語)、NFR-070(TZ)、region 属性導入による契約モデル拡張 |
| 画面 | UI 言語スイッチャー、契約発行画面(region 選択)、アカウント設定(個人 TZ) |
| API | `POST /admin/v1/owners/{id}/region-approval`、`TenantRegionGuard` ミドルウェア(全 API)、メール送信 API の locale パラメータ |
| テーブル | `M_OWNERS.region` 列追加、`owner_region_audit_logs`、翻訳キー管理テーブル(Future で具体化) |
| 運用 | 越境移転ガードの監査、translation 差分 CI、海外メールテンプレートのレビュー、リージョン別 D1 / R2 配置運用、リージョン横断レポート集計 |

------------------------------------------------------------------------

## <span id="4-実施条件"></span>4. 実施条件

| 項目 | 内容 |
|----|----|
| 実施判断条件 | 多言語は英語追加の需要・翻訳品質・サポート体制、マルチリージョンは region 属性導入評価(ベータ)→ 選択可否(GA)、TZ 上書きは多言語化との併用評価 |
| 期限 | T2(region 属性導入評価、英語追加判定)、T3(マルチリージョン選択、多言語 en / ja 同等品質、TZ 上書き) |
| 依存関係 | 共有概念の 2 マスタ完全分離ユーザーモデル(`M_OWNERS` / `M_PRJ_USERS` / `M_PRJ_USER_ASGN`)拡張、PII 暗号化・鍵管理(メイン正本)とリージョン別鍵配置 |

------------------------------------------------------------------------

## <span id="5-関連設計"></span>5. 関連設計

| 種別 | 参照先 |
|----|----|
| 要件 | [../01_requirements/index.md](../01_requirements/index.md) |
| 基本設計 | [../02_basic_design/index.md](../02_basic_design/index.md) |

------------------------------------------------------------------------

## <span id="6-未確定事項確認事項"></span>6. 未確定事項・確認事項

| 確認事項ID | 確認内容 | 優先度 | ステータス |
|----|----|----|----|
| FUT-I18N-Q-001 | 翻訳キー管理ツール(i18next 等)と翻訳差分 CI 方式の選定 | 中 | 検討中 |
| FUT-I18N-Q-002 | マルチリージョン契約での region 変更可否(原則固定 / 例外手順 RB-014 連携) | 中 | 検討中 |
| FUT-I18N-Q-003 | 管理者単位 TZ と契約 TZ の優先順位、監査ログ表示時刻のルール | 中 | 検討中 |
| FUT-I18N-Q-004 | リージョン横断レポート(課金集計等)の境界 | 低 | 検討中 |

---

<!-- portal-bottom -->
[将来対応](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
