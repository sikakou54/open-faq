# モジュール構造図(MOD)テンプレート

> **本テンプレートはモジュール構造図(MOD)の記載骨格(機能領域単位 1 ファイル)を定義します。**

運用ルールの正本は [../CLAUDE.md](../CLAUDE.md)。共通記載スタイルは [共通記載スタイル](00_common-style.md) を参照する。

- **配置先**: `03_detail_design/11_module/`(`index.md` + `MOD-001.md`〜)
- **採番**: `MOD-001`〜(機能領域単位 1 ファイル・ゼロ詰め 3 桁・欠番なし・`<span id>` 出現順 001)。ID は各設計書の H1 に `# <span id="MOD-001"></span>MOD-001: 名称` で保持する。

## 骨格(6 セクション固定)

**機能領域単位 1 ファイル(`MOD-NNN`)**。基本設計(全体アーキテクチャ / SYS / API / SCR / TBL)を入力とし、実装スタック(TypeScript + Next.js(App Router) + Repository 層)と実行基盤(Cloudflare Workers/Pages + D1 + Queues + Cron Triggers)への **物理配置を意識したモジュール分割・依存方向** を、実装者がディレクトリ構成と呼び出し関係を迷わず組み立てられる粒度へ具体化する。**依存は内向き**(frontend → api → service → repository、外部連携は service → external-gateway)を原則とし、外向きの逆依存を作らない。骨格:

- H1 アンカー `# <span id="MOD-NNN"></span>MOD-NNN: 名称`
- ページ要約(引用ブロック)＋ 文書メタ(斜体 1 行。`*種別 モジュール構造図 ・ ステータス ドラフト*`。共通記載スタイル参照)
- ヘッダー表(MOD ID / 業務ユースケースID `UC-NNN` / 関連 API・SYS / 関連画面 `SCR` / 関連テーブル `TBL`)。全層の厳密な紐付けはトレーサビリティ一覧表に一元管理し、MOD 本文に `TR-NNN` は記載しない。
- `## 1. 目的` / `## 2. モジュール一覧` / `## 3. モジュール構造図` / `## 4. 依存関係一覧` / `## 5. モジュール別処理概要` / `## 6. 後続工程への引き継ぎ事項`

各 `##`/`###` 直後に 1〜2 文のリード文を置いてから表・図へ入る(表・図をいきなり置かない)。導出できない欄は `要確認`、該当なしは `—`。

## 記載ルール

- **種別は次の値から選ぶ**: `frontend`(Server/Client Components)/ `api`(Route Handlers = `app/api/**/route.ts`)/ `service`(`lib/service` のビジネスロジック)/ `repository`(`lib/repository` の D1 アクセス)/ `batch`(`workers/cron` = Cron Triggers ・ `workers/queues` = Queues 消費)/ `external-gateway`(`lib/gateway` の Stripe / Resend / AI 連携)/ `共通`(横断ユーティリティ・型・検証)。取りうる種別は全集合を列挙し「等」で打ち切らない。
- **物理配置を意識したモジュール名にする**(例: `lib/service/billing`・`app/api/projects/[id]/route.ts`・`workers/queues/inference-consumer`・`lib/gateway/stripe`)。ただし **物理カラム名・SQL 本文・実装コード本文・クラス/関数の内部実装は書かない**(モジュールの責務・入出力・依存方向を示すに留める。物理カラム定義は DBP の本務)。
- **依存方向は内向きを守る**。§4 で `同期/非同期` を明示し、非同期は写像先(`Queues 経由`・`Cron Triggers 起動`)を記す。逆依存(repository → service 等)や循環依存が生じる場合は設計を見直し、判断に迷う点は GitHub Issue で課題化する。
- **設計値(しきい値・単価・無料枠・タイムアウト・保持期間)・状態名の意味は本書で再定義しない。** [システム仕様書](../02_basic_design/07_system-spec.md) / [状態モデル](../02_basic_design/08_state-model.md) / [用語集](../01_requirements/00_glossary.md) へリンクまたは ID 参照で送る。「等」で打ち切らない。
- 業務ユースケースID(`UC`)と設計上必要な関連 ID(`API` / `SYS` / `SCR` / `TBL`)はヘッダー表に記載する。要件 ID(`FR` / `BR` / `NFR` / `RULE`)は設計根拠の括弧引用としてのみ許容し、逆引きの対応表・専用欄は作らない。相互参照は [共通記載スタイル](00_common-style.md) の相互参照アンカー例に従う(`03_detail_design/11_module/` からの深さは `../02_basic_design/...` / `../01_requirements/...` / `../CLAUDE.md`)。
- mermaid はコードフェンスの開き(` ```mermaid `)・閉じ(` ``` `)を独立行に置き、`flowchart` を用いる。ノードラベルに丸括弧・角括弧・スラッシュ等を含めるときは `"..."` で囲む。**絵文字は使わない。**

## 記載例(セクション骨格)

```markdown
# <span id="MOD-001"></span>MOD-001: 課金・請求モジュール構造

> **本構造図は「課金・請求」機能領域のモジュール分割と内向き依存の方向を定義します。**

*種別 モジュール構造図 ・ ステータス ドラフト*

| 項目 | 値 |
|----|----|
| MOD ID | MOD-001 |
| 業務ユースケースID | [UC-056](../../01_requirements/04_business_usecases/UC-056.md#UC-056) |
| 関連 API / SYS | [API-060](../../02_basic_design/02_backend/03_apis/API-060.md#API-060) ・ [SYS-004](../../02_basic_design/02_backend/01_system/SYS-004.md#SYS-004) |
| 関連画面 | [SCR-011](../../02_basic_design/01_frontend/01_screens/SCR-011.md#SCR-011) |
| 関連テーブル | [TBL-032](../../02_basic_design/02_backend/04_database/TBL-032.md#TBL-032) |

## 1. 目的

本機能領域が担う業務目的と、モジュール分割の方針(内向き依存・物理配置の対応・外部連携の切り出し)を 1〜2 文で示す。

## 2. モジュール一覧

本機能領域を構成するモジュールを物理配置・種別・責務・入出力で一覧化する。

| モジュールID | モジュール名 | 種別 | 責務 | 主な入力 | 主な出力 |
|----|----|----|----|----|----|
| M-01 | `app/billing`(請求画面) | frontend | 請求状況・支払方法を表示し操作を受け付ける | 利用者操作 | API 呼び出し |
| M-02 | `app/api/billing/route.ts` | api | 請求操作の受付・認証認可・入力検証・Service 呼び出し | HTTP リクエスト | Service 呼び出し・HTTP レスポンス |
| M-03 | `lib/service/billing` | service | 月次請求確定・サスペンション判定の業務ロジック | 請求要求・課金状態 | Repository / Gateway 呼び出し |
| M-04 | `lib/repository/billing` | repository | 課金アカウント・請求データの参照・更新(D1) | Service からの取得 / 更新要求 | 取得結果 / 更新結果 |
| M-05 | `lib/gateway/stripe` | external-gateway | 課金プロバイダ(Stripe)への決済・購読操作と Webhook 受信 | 決済要求・Webhook | 決済結果・状態通知 |
| M-06 | `workers/queues/billing-consumer` | batch | 非同期の請求確定ジョブを消費し Service を起動する | Queues メッセージ | Service 呼び出し |

## 3. モジュール構造図

モジュール間の依存を内向き(上位 → 下位)で示す。外部連携は独立ノードとして分離する。

\`\`\`mermaid
flowchart TB
    M01["請求画面(frontend)"]
    M02["請求 API(api)"]
    M03["請求サービス(service)"]
    M04["請求リポジトリ(repository)"]
    M05["Stripe ゲートウェイ(external-gateway)"]
    M06["請求確定コンシューマ(batch)"]
    DB["D1(TBL 参照)"]
    M01 --> M02
    M02 --> M03
    M06 --> M03
    M03 --> M04
    M03 --> M05
    M04 --> DB
\`\`\`

## 4. 依存関係一覧

呼び出し元・呼び出し先の依存を、同期/非同期の別と用途で一覧化する。

| 呼び出し元 | 呼び出し先 | 用途 | 同期/非同期 | 備考 |
|----|----|----|----|----|
| M-01 請求画面 | M-02 請求 API | 請求操作の送信 | 同期 | — |
| M-02 請求 API | M-03 請求サービス | 業務ロジック委譲 | 同期 | — |
| M-03 請求サービス | M-04 請求リポジトリ | 課金データの参照・更新 | 同期 | 物理カラムは [TBL-032](../../02_basic_design/02_backend/04_database/TBL-032.md#TBL-032) を参照 |
| M-03 請求サービス | M-05 Stripe ゲートウェイ | 決済・購読操作 | 同期 | タイムアウトは [システム仕様書](../02_basic_design/07_system-spec.md#3-タイムアウトセッション認証) を参照 |
| M-06 請求確定コンシューマ | M-03 請求サービス | 月次請求確定の起動 | 非同期(Queues 経由) | 失敗継続分は DLQ へ退避 |

## 5. モジュール別処理概要

各モジュールの処理概要と例外処理の方針を示す。実装コード本文・SQL 本文は書かない。

| モジュール | 処理概要 | 例外処理 | 備考 |
|----|----|----|----|
| M-03 請求サービス | 課金状態としきい値を評価し月次請求を確定、無料枠超過はサスペンション判定へ回す | 判定不能時は確定を保留しアラート | しきい値・無料枠の正本は [システム仕様書](../02_basic_design/07_system-spec.md) |
| M-05 Stripe ゲートウェイ | 決済・購読操作を送信し、Webhook を署名検証して状態を取り込む | 署名検証失敗は取り込まず記録・重複再送は冪等応答 | 状態名は [状態モデル](../02_basic_design/08_state-model.md) を参照 |

## 6. 後続工程への引き継ぎ事項

実装・テスト設計へ引き継ぐ観点(依存方向の逸脱検出・非同期境界・外部連携の切り離しテスト等)を箇条書きで示す。

- 内向き依存の逸脱(逆依存・循環依存)が生じていないことの検証観点。
- Queues 経由の非同期境界(投入・消費・冪等・DLQ 滞留)のテスト観点。
- external-gateway をスタブ化した Service 単体テストの分離観点。
```

## テンプレ運用の注記

本節はテンプレの使い方ガイドであり、**実ドキュメントには転記しない。**

- **記載しない項目**: 実装コード本文・SQL 本文・ORM クエリ・物理カラム名の羅列・クラス/関数の内部実装・アルゴリズム詳細・変数名/JSON キー名。層横断トレーサビリティ(`TR-NNN`)。要件 ID(`FR` / `BR` / `NFR` / `RULE`)の逆引き対応表・専用欄。正本で定義済みの具体値(しきい値・単価・無料枠・タイムアウト・保持期間・状態名の意味)の再定義。「等」での打ち切り。
- **基本設計との責務分担**: 基本設計(全体アーキテクチャ / SYS / API / SCR / TBL)は「システムが何を実現するか・どの契機で何を呼ぶか」を業務語と論理単位で定義する。MOD はその詳細設計として「Next.js on Cloudflare の物理配置(`app/`・`lib/service`・`lib/repository`・`workers/cron`・`workers/queues`・`lib/gateway` 等)へどうモジュールを分割し、内向きの依存方向(frontend → api → service → repository、外部連携は service → external-gateway)でどう結線するか」を定義する。基本設計に無い機能・依存は推測で足さず、不明点は GitHub Issue で課題化する。処理ロジック本体は IPO、バッチ/非同期の起動制御は BAT、外部連携仕様は EIF、物理カラム定義は DBP が担い、MOD は分割境界と依存方向に責務を絞る。
- **後続テスト設計への引き継ぎ観点**: §6 に、内向き依存の逸脱(逆依存・循環依存)検出、Queues による非同期境界(投入・消費・冪等・DLQ 滞留)、external-gateway をスタブ化した Service 単体テストの分離、モジュール境界での契約(入出力)整合など、後続の実装・テスト設計が分割境界と依存方向を一意に読み取れる観点を残す。
```
