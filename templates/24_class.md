# クラス図(CLS)テンプレート

> **本テンプレートはクラス図(CLS)の記載骨格(機能 / レイヤー単位 1 ファイル)を定義します。**

運用ルールの正本は [../CLAUDE.md](../CLAUDE.md)。共通記載スタイルは [共通記載スタイル](00_common-style.md) を参照する。

- **配置先**: `03_detail_design/10_class/`(`index.md` + `CLS-001.md`〜)
- **採番**: `CLS-001`〜(機能 / レイヤー単位 1 ファイル・ゼロ詰め 3 桁・欠番なし・`<span id>` 出現順に `001` から採番)。ID は各設計書の H1 に `# <span id="CLS-001"></span>CLS-001: 名称` で保持する。

## 骨格(7 セクション固定)

**機能 / レイヤー単位 1 ファイル(`CLS-NNN`)**。基本設計の [API設計(API)](10_api.md) のリクエスト/レスポンス・[DB設計(TBL)](11_database.md) のエンティティ・[画面設計(SCR)](06_screen.md) の Component を入力とし、実装スタック(TypeScript + Next.js(App Router)+ Repository層 / Cloudflare Workers・Pages・D1・Queues・Cron Triggers)のレイヤー分担に沿って、実装者がクラス構成・責務・シグネチャ・データ構造の境界を迷わず組み立てられる粒度へ具体化する。骨格:

- H1 アンカー `# <span id="CLS-NNN"></span>CLS-NNN: 名称`
- ページ要約(引用ブロック)+ 文書メタ(斜体 1 行。共通記載スタイル参照)
- ヘッダー表(CLS ID / 業務ユースケースID `UC-NNN` / 関連 API `API` / 関連画面 `SCR` / 関連テーブル `TBL` / 関連 SYS)。全層の厳密な紐付けはトレーサビリティ一覧表に一元管理し、CLS 本文に `TR-NNN` は記載しない。
- `## 1. 目的`
- `## 2. 対象範囲`
- `## 3. クラス図`(mermaid `classDiagram`)
- `## 4. クラス一覧`
- `## 5. メソッド一覧`
- `## 6. 利用するデータ構造`
- `## 7. 後続工程への引き継ぎ事項`

導出できない欄は `要確認`、該当なしは `—`(全角ダッシュ)。

## 記載ルール

- 各 `##`/`###` 直後に 1〜2 文のリード文を置いてから表へ入る(表をいきなり置かない)。
- **Next.js(App Router)+ Repository層のレイヤー分担でクラスを切る。** 種別は Route Handler(Controller 相当。`app/api/**/route.ts`)/ Server Component / Client Component(画面 = SCR)/ Service(業務ロジック)/ Repository(D1 アクセス)/ DTO / Form / ViewModel のいずれかに割り当てる。上位レイヤーは下位レイヤーへ依存し逆流させない(Component → Service → Repository → D1)。外部連携(Stripe / Resend / AI)・非同期(Queues)・バッチ(Cron Triggers)を含む場合はその境界クラス(Client / Handler)も 1 レイヤーとして示す。
- **DTO / Entity / ViewModel の境界を明確化する。** DTO は API 境界の入出力(リクエスト/レスポンス構造)、Entity は永続データ(TBL 由来のドメインモデル)、ViewModel は画面表示用の整形済みモデルとして役割を分け、どこで変換するか(Service / Component)を §6 に明記する。物理カラム名の対応・変換規則の詳細は [DB物理設計(DBP)](11_database.md) / [入出力設計書(IO)](17_io-spec.md) へ委ね、本書は論理項目・クラス項目で示す。
- **シグネチャ粒度に留め、実装コード本文を書かない。** クラス名・メソッド名・引数/戻り値の論理型は示すが、メソッド本体の処理ロジック・SQL 本文・アルゴリズム実装・変数名・JSON キー名・物理カラム名の羅列は書かない(判定条件・入出力の論理型・疑似シグネチャは可)。処理ロジックの詳細は [IPO処理機能記述書(IPO)](18_ipo.md) / [詳細シーケンス図(DSQ)](21_sequence.md) へ委ねる。
- **設計値(しきい値・単価・タイムアウト・保持期間)・状態名の意味は本書で再定義しない。** [システム仕様書](../02_basic_design/07_system-spec.md) / [状態モデル](../02_basic_design/08_state-model.md) / [用語集](../01_requirements/00_glossary.md) へリンクまたは ID 参照で送る(例:「信頼度しきい値([システム仕様書 §1](../02_basic_design/07_system-spec.md#1-aiしきい値))」)。**「等」で打ち切らない**(取りうるクラス・メソッド・データ構造は列挙する)。
- 業務ユースケースID(`UC`)と設計上必要な関連 ID(`API` / `SCR` / `TBL` / `SYS`)はヘッダー表に記載する。要件 ID(`FR` / `BR` / `NFR` / `RULE`)は設計根拠の括弧引用としてのみ許容し、逆引きの対応表・専用欄は作らない。相互参照は [共通記載スタイル](00_common-style.md) の相互参照アンカー例に従う。
- **mermaid `classDiagram` は描画可能であること。** フェンスの開き(` ```mermaid `)・閉じ(` ``` `)を独立行に置き、後続要素を同一行へ連結しない。ノードラベル・メンバーに丸括弧等の特殊文字を含める場合は表現を避けるか置換する。図中に Markdown リンク・`id=` を書かない。**絵文字は使わない。**

## 記載例(セクション骨格)

```markdown
# <span id="CLS-001"></span>CLS-001: 新規登録機能 クラス構成

> **本クラス図は「新規登録機能を実装する Route Handler・Service・Repository・DTO/Entity の構成と責務」を定義します。**

*種別 クラス図 ・ ステータス ドラフト*

| 項目 | 値 |
|----|----|
| CLS ID | CLS-001 |
| 業務ユースケースID | [UC-002](../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| 関連 API | [API-001](../../02_basic_design/02_backend/03_apis/API-001.md#API-001) |
| 関連画面 | [SCR-002](../../02_basic_design/01_frontend/01_screens/SCR-002.md#SCR-002) |
| 関連テーブル | [TBL-001](../../02_basic_design/02_backend/04_database/TBL-001.md#TBL-001) |
| 関連 SYS | — |

## 1. 目的

本クラス図が確定する機能 / レイヤーの範囲と、実装者が押さえるべきレイヤー分担(依存方向)を 1〜2 文で示す。

## 2. 対象範囲

対象とする機能・レイヤーと、対象外を明示する。

| 区分 | 対象 |
|----|----|
| 対象機能 | 新規登録([API-001](../../02_basic_design/02_backend/03_apis/API-001.md#API-001))・登録画面([SCR-002](../../02_basic_design/01_frontend/01_screens/SCR-002.md#SCR-002)) |
| 対象レイヤー | Route Handler / Service / Repository / DTO / Entity / Form |
| 対象外 | 確認メール再送(別 CLS)・課金アカウント作成・メール配信の外部連携([外部インターフェース設計(EIF)](20_external-if.md) が担う) |

## 3. クラス図

レイヤーごとのクラスと依存方向を示す(Component → Service → Repository → D1、逆流させない)。

\`\`\`mermaid
classDiagram
    class SignupRouteHandler {
        +post(SignupRequest) SignupResponse
    }
    class SignupForm {
        +submit() void
    }
    class SignupService {
        +register(SignupInput) SignupResult
    }
    class UserRepository {
        +create(UserEntity) UserEntity
        +findByEmail(email) UserEntity
    }
    class SignupRequestDto
    class SignupResponseDto
    class UserEntity
    SignupForm --> SignupRouteHandler
    SignupRouteHandler --> SignupService
    SignupRouteHandler --> SignupRequestDto
    SignupRouteHandler --> SignupResponseDto
    SignupService --> UserRepository
    UserRepository --> UserEntity
\`\`\`

## 4. クラス一覧

各クラスの種別(レイヤー)・責務・主なメソッドを一覧化する。

| クラス名 | 種別 | 責務 | 主なメソッド | 備考 |
|----|----|----|----|----|
| SignupRouteHandler | Route Handler(Controller 相当) | 入力受領・DTO 変換・Service 呼び出し・応答整形 | `post` | `app/api/auth/signup/route.ts` 相当 |
| SignupForm | Client Component | 入力フォーム表示・クライアント検証・送信 | `submit` | 検証仕様は [SCR-002](../../02_basic_design/01_frontend/01_screens/SCR-002.md#SCR-002) §5 |
| SignupService | Service | 登録の業務判定・重複確認・トークン発行の統括 | `register` | 判定詳細は [IPO](18_ipo.md) へ委譲 |
| UserRepository | Repository | ユーザーの永続化・照会(D1) | `create` / `findByEmail` | 物理項目対応は [DBP](11_database.md) |

## 5. メソッド一覧

主要メソッドの目的・入出力・例外をシグネチャ粒度で定義する(実装本体は書かない)。

| クラス名 | メソッド名 | 目的 | 入力 | 出力 | 例外 | 備考 |
|----|----|----|----|----|----|----|
| SignupRouteHandler | `post` | 登録要求を受理し応答を返す | 登録リクエスト DTO | 受付結果 DTO | 検証エラー([ERR-001](../02_basic_design/05_errors/ERR-001.md#ERR-001)) | HTTP 境界 |
| SignupService | `register` | 登録の業務処理を実行する | 登録入力(論理項目) | 登録結果 | メール重複([ERR-014](../02_basic_design/05_errors/ERR-014.md#ERR-014)) | トークン発行を含む |
| UserRepository | `findByEmail` | メールでユーザーを照会する | メールアドレス | ユーザー Entity / 該当なし | — | 加工後の値で照会 |

## 6. 利用するデータ構造

クラス間で受け渡すデータ構造を DTO / Entity / ViewModel の境界で定義する。

| 名称 | 種別 | 主な項目 | 用途 |
|----|----|----|----|
| SignupRequestDto | DTO | 表示名・メールアドレス・パスワード・規約/プライバシー同意 | API 境界の入力(Route Handler で受領) |
| SignupResponseDto | DTO | 受付結果 | API 境界の出力 |
| UserEntity | Entity | ユーザーID・メールアドレス・表示名・状態 | 永続ドメインモデル([TBL-001](../../02_basic_design/02_backend/04_database/TBL-001.md#TBL-001) 由来) |
| UserProfileViewModel | ViewModel | 表示名・状態ラベル | 画面表示用整形モデル(Service で Entity から変換) |

## 7. 後続工程への引き継ぎ事項

詳細ロジック設計(IPO)・詳細シーケンス(DSQ)・テスト設計へ引き継ぐ観点を挙げる。

- DTO ↔ Entity ↔ ViewModel の変換規則(どのレイヤーで変換するか)を IPO / IO で確定する。
- レイヤー間の依存方向・例外伝播の境界をテスト設計でケース化する。
- 論理項目 ↔ 物理カラムの対応は [DB物理設計(DBP)](11_database.md) で確定する。
```

## テンプレ運用の注記(実ドキュメントには転記しない)

本節はテンプレートの使い方ガイドである。以下の内容を実際の `CLS-NNN.md` へ転記しない。

- **記載しない項目**: メソッド本体の実装コード・処理ロジック・SQL 本文・アルゴリズム実装・変数名 / JSON キー名 / 物理カラム名の羅列、設計値の再定義(しきい値 / 単価 / タイムアウト / 保持期間は正本へリンク)、状態名の意味(状態モデルへ参照)、`TR-NNN`(層横断トレーサビリティ)と要件 ID(`FR` / `BR` / `NFR` / `RULE`)の逆引き対応表・専用欄。クラス名・メソッド名・引数/戻り値の論理型はシグネチャ粒度で示す。
- **基本設計との責務分担**: 基本設計は「機能として何を提供するか」を示す — API はエンドポイントのリクエスト/レスポンス構造、TBL はエンティティ(物理項目)、SCR は画面 Component と表示項目。CLS はこれらを入力に「実装スタック(Next.js App Router + Repository層)のレイヤーへどうクラスを配置し、どの責務・シグネチャ・データ構造(DTO/Entity/ViewModel)で組むか」を実装可能粒度へ具体化する。基本設計に無い仕様は推測で足さず、不明点は GitHub Issue で課題化する。処理ロジックの詳細は IPO、詳細な相互作用は DSQ、物理カラム定義は DBP が担う。
- **後続テスト設計への引き継ぎ観点**: レイヤー間の依存方向(逆流の有無)・例外の伝播境界・DTO ↔ Entity ↔ ViewModel の変換規則(変換レイヤーと欠損時の扱い)・Repository の照会/更新条件の境界を §7 に整理し、後続の IPO / DSQ / テスト設計がクラス責務と成否条件を一意に読み取れる状態を保つ。
