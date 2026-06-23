# シーケンス設計(SEQ)テンプレート

> **本テンプレートはシーケンス設計(SEQ)の記載骨格(UC 単位 1 ファイル)を定義します。**

運用ルールの正本は [../CLAUDE.md](../CLAUDE.md)。共通記載スタイルは [共通記載スタイル](00_common-style.md) を参照する。

- **配置先**: `02_basic_design/03_sequences/`
- **採番**: `SEQ-001`〜(UC 単位 1 ファイル・ゼロ詰め 3 桁・欠番なし)

## 骨格

**UC 単位 1 ファイル(`SEQ-NNN`)**。骨格:

- `## 項目`(SEQ ID / 対応業務ユースケース `UC` / 業務要件 `BR` / 機能要件 `FR` / 画面イベント `EVT`(プレーンテキストの ID。EVT は独立ページを持たず SCR §6 のアンカーのため、リンクにしない)/ 関連画面 `SCR` / 関連 API `API` / 関連テーブル `TBL` / エラー `ERR` / メッセージ `MSG`)
- `## 概要`
- `## シーケンス図`(mermaid `sequenceDiagram`)
- (必要時のみ)`## 代替フロー` / `## 例外フロー` / `## 詳細設計への移管候補`
- `## 備考`

導出できない欄は `要確認`、該当なしは `—`。**冗長な「正常系シーケンス」番号付き本文は置かない**(mermaid を正本とする)。

## シーケンス図ルール

- **アクターは基本 3 者** `ユーザー / 画面 / サーバー`(`actor U as ユーザー` / `participant Screen as <画面名>` / `participant Server as サーバー`)。**画面アクターは画面設計の具体的な画面名**を用いる(`画面 SCR-NNN` ではなく `participant Screen as ログイン` 等)。複数画面にまたがる場合も画面参加者は起点画面 1 つとし、遷移先画面はメッセージ本文で示す(SCR-ID は `関連画面` 欄でリンク)。図に名称のない画面は `画面名(要確認)`。
- **API / DB / 認証認可 / 入力検証 / 業務処理 はすべて `サーバー` に集約**する。DB 操作は `Server->>Server: 業務処理・DB更新` のようなサーバー自己メッセージで表し、**テーブル別 `テーブル名(CRUD)` 表記は図に書かず** `関連テーブル` 欄で示す。
- **システム起点フロー**(バッチ / Webhook / 非同期 / 通知、概ね SEQ-088 以降。SEQ-108..122 はシステム設計 `SYS-001..015` に対応)は `ユーザー / 画面` を持たず、外部システム・スケジューラ・バッチ等の実体を参加者として残す(`participant R as Resend(外部)` / `participant SCH as スケジューラ` / `participant B as 削除バッチ` 等)。内部の API/DB/処理はその実体または `サーバー` の自己メッセージへ集約する。
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
| 対応業務ユースケース | [UC-001](../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| 業務要件 | [BR-001](../../01_requirements/01_business_requirement/01_account-br.md#BR-001) |
| 機能要件 | [FR-001](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-001) |
| 画面イベント | EVT-001 |
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
    U->>Screen: 操作
    Screen->>Server: 要求
    Server->>Server: 業務処理・DB更新
    Server-->>Screen: 応答
    Screen-->>U: 結果表示
\`\`\`

## 備考

…
```
