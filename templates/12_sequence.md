# シーケンス設計(SEQ)テンプレート

> **本テンプレートはシーケンス設計(SEQ)の記載骨格(UC 単位 1 ファイル)を定義します。**

運用ルールの正本は [../CLAUDE.md](../CLAUDE.md)。共通記載スタイルは [共通記載スタイル](00_common-style.md) を参照する。

- **配置先**: `02_basic_design/03_sequences/`
- **採番**: `SEQ-001`〜(UC 単位 1 ファイル・ゼロ詰め 3 桁・欠番なし)

## 骨格

**UC 単位 1 ファイル(`SEQ-NNN`)**。骨格:

- `## 項目`(SEQ ID / 業務ユースケースID / イベント(画面ID EVT-NN) / テーブルID / 関連画面 `SCR` / 関連 API `API` / エラー `ERR` / メッセージ `MSG`)。全層の厳密な紐付けはトレーサビリティ一覧表で一元管理し、SEQ 本文に `TR-NNN` / `業務要件` / `機能要件` は持たない。
- `## 概要`
- `## シーケンス図`(mermaid `sequenceDiagram`)
- (必要時のみ)`## 代替フロー` / `## 例外フロー` / `## 詳細設計への移管候補`
- `## 備考`

導出できない欄は `要確認`、該当なしは `—`。**冗長な「正常系シーケンス」番号付き本文は置かない**(mermaid を正本とする)。

## シーケンス図ルール

- **アクターは基本 4 者** `ユーザー / 画面 / サーバー / DB`(`actor U as ユーザー` / `participant Screen as <画面名>` / `participant Server as サーバー` / `participant DB as DB`)。**画面アクターは画面設計の具体的な画面名**を用いる(`画面 SCR-NNN` ではなく `participant Screen as ログイン` 等)。複数画面にまたがる場合も画面参加者は起点画面 1 つとし、遷移先画面はメッセージ本文で示す(SCR-ID は `関連画面` 欄でリンク)。図に名称のない画面は `画面名(要確認)`。`participant DB as DB` は `participant Server as サーバー`(システム起点はサーバー役のバッチ等)の直後に置く。
- **API / 認証認可 / 入力検証 / 業務処理 は `サーバー` に集約**し、**DB(永続データ)の参照・更新は独立した `DB` アクターへのメッセージで表す**。DB 読み書きは `Server->>DB: …` / `DB-->>Server: 取得結果(または更新完了)` の要求・応答対で描き、**テーブル別 `テーブル名(CRUD)` 表記は図に書かず** `関連テーブル` 欄で示す。**DB を触らない純粋処理(入力検証・署名検証・認証認可判定・取得済みデータの評価/判定)はサーバー自己メッセージ `Server->>Server: …` のまま残す**(`認証・データ取得` のように DB 読みを含むものは DB アクターへ送る)。図に DB の参照・更新が一切無いフロー(純粋なサニタイズ等)は `DB` アクターを置かない。
- **システム起点フロー**(バッチ / Webhook / 非同期 / 通知、概ね SEQ-088 以降。SEQ-108..122 はシステム設計 `SYS-001..015` に対応)は `ユーザー / 画面` を持たず、外部システム・スケジューラ・バッチ等の実体を参加者として残す(`participant R as Resend(外部)` / `participant SCH as スケジューラ` / `participant B as 削除バッチ` 等)。内部の API・処理はその実体または `サーバー` の自己メッセージへ集約し、DB 参照・更新は同様に `DB` アクターへのメッセージ(`B->>DB: …` / `DB-->>B: …`)で表す。
- `autonumber` を付け、要求に応答線を対で描く。分岐は `alt/else/opt/loop`。**SQL・クラス / メソッド名・ORM・テーブル CRUD・コンポーネント内部 ID(旧 `API-XXX-NNN` / `IT-` / `EV-` / `E-`)は書かない。** 図中に Markdown リンク・`id=` を書かない(検証スクリプトのため)。行単位処理・冪等性・楽観ロック等の詳細は `## 詳細設計への移管候補` に逃がす。
- SEQ 図は手保守(mermaid を正本)。

## 記載例(セクション骨格)

```markdown
# <span id="SEQ-001"></span>SEQ-001: 管理者がアカウントを登録する

> **本シーケンスは「…」を定義します。**

*種別 シーケンス設計 ・ ステータス ドラフト*

## 項目

| 項目 | 値 |
|----|----|
| SEQ ID | SEQ-001 |
| 業務ユースケースID | [UC-001](../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| イベント(画面ID EVT-NN) | SCR-001 EVT-01 |
| 関連画面 | [SCR-001](../01_frontend/01_screens/SCR-001.md#SCR-001) |
| 関連 API | [API-001](../02_backend/03_apis/API-001.md#API-001) |
| 関連テーブル | [TBL-001](../02_backend/04_database/TBL-001.md#TBL-001) |
| エラー | [ERR-001](../05_errors/ERR-001.md#ERR-001) |
| メッセージ | — |

## 概要

…

## シーケンス図

\`\`\`mermaid
sequenceDiagram
    autonumber
    actor U as ユーザー
    participant Screen as ログイン
    participant Server as サーバー
    participant DB as DB
    U->>Screen: 操作
    Screen->>Server: 要求
    Server->>Server: 入力検証・認証認可
    Server->>DB: 業務データを更新
    DB-->>Server: 更新完了
    Server-->>Screen: 応答
    Screen-->>U: 結果表示
\`\`\`

## 備考

…
```
