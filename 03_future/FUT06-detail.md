<!-- portal-top -->
[設計ポータル](../README.md) ／ [将来対応](index.md) ／ **FUT06: 個別チャット詳細設計**
<!-- /portal-top -->

# FUT06: 個別チャット詳細設計

## <span id="0-文書情報"></span>0. 文書情報

| 項目 | 内容 |
|----|----|
| 文書名 | FUT06: 個別チャット詳細設計 |
| 詳細設計ID | FUT06-DD |
| 対象システム | FAQ AI ウィジェット SaaS / メインシステム |
| 関連機能ID | FR-080〜091（個別チャット部屋 / メッセージ / 再入室）/ AC-011 / AC-025 |
| 作成日 | 2026-05-17 |
| 版数 | v1.3 |
| ステータス | Future |

本書は [FUT06.md](FUT06.md) の詳細設計を定義する。

## <span id="1-対象範囲"></span>1. 対象範囲

| 種別 | ID | 名称 |
|----|----|----|
| 機能 | FR-080〜091 | 独立した個別チャット部屋 / メッセージ送受信 |
| 機能 | FR-086a | 個別チャット部屋への担当管理者ユーザー割当（担当者の指定は個別チャットのみの概念。担当者は常に 1 名・未割当不可。未解決質問は担当者を持たない） |
| 機能 | FR-086b | 新規チャット部屋作成時の担当者自動割当（デフォルト担当者→未設定時オーナーへフォールバック） |
| 機能 | FR-086c | プロジェクト単位デフォルト担当者設定（SCR-034 / `M_PROJECTS.default_assignee_user_id`） |
| 機能 | FR-083 / FR-084 | 個別チャット再入室（SCR-024 連携） |
| 画面 | SCR-013 | 個別チャット一覧（利用者側 / エンドユーザー側部屋ビューを含む） |
| 画面 | SCR-033 | 個別チャット部屋（利用者側、担当者プルダウン） |
| 画面 | SCR-034 | 自動割り当て（SCR-013 チャット配下タブ） |
| 画面 | SCR-024 | 個別チャット再入室（再入室トークン） |
| API | `/chat-rooms/*` `/widget/v1/chat-rooms/*` `PATCH /projects/{id}` | チャット部屋操作（管理画面 + ウィジェット）+ デフォルト担当者設定 |
| テーブル | `chat_rooms`（`assignee_user_id` NOT NULL）`chat_messages` `M_PROJECTS`（`default_assignee_user_id`）`T_ACCESS_TOKENS (purpose=reentry)` | チャット基盤 |

## <span id="2-収録ロジック対応章"></span>2. 収録ロジック・対応章

| 元章 | 元タイトル | 概要 |
|----|----|----|
| §6 SCR-013 / SCR-033 | 画面詳細設計 | 個別チャット一覧 / エンドユーザー部屋 / 管理者向けチャット部屋 |
| §6 SCR-024 / SCR-034 | 画面詳細設計 | 個別チャット再入室 / デフォルト担当者設定 |
| §7 | 機能詳細設計（個別チャット関連） | チャット部屋 / メッセージ送信 / 再入室 |
| §3.3.1-3.3.2 | モジュール構成 | `routes/chat-rooms.ts` / widget-api の `routes/chat-rooms.ts` / `routes/reentry.ts` |
| §10.5.4 | 再入室トークン | 30 日 T_ACCESS_TOKENS、ブラウザへ直接返却 |

> 個別チャット固有の画面・API・データ仕様は本書を正本とし、MVP設計書には記載しない。

## <span id="3-詳細設計本文"></span>3. 詳細設計本文

### <span id="31-画面詳細設計"></span>3.1 画面詳細設計

| 画面 | 利用者 | 主な表示・操作 | 主な遷移 |
|----|----|----|----|
| SCR-013 個別チャット一覧 | 管理者ユーザー | チャットID、最終メッセージ、未読数、更新日時、プロジェクト・未読絞り込み | 行選択で SCR-033 |
| SCR-013 エンドユーザー部屋 | エンドユーザー | チャットID、会話履歴、メッセージ入力、機密情報注意 | AI未解決時に同一ウィジェット内で切替 |
| SCR-033 個別チャット部屋 | 管理者ユーザー | 会話履歴、返信入力、担当者変更、一覧へ戻る | SCR-013から遷移 |
| SCR-034 自動割り当て | オーナー / プロジェクト管理者 | デフォルト担当者の選択・保存 | SCR-013の管理タブから遷移 |
| SCR-024 個別チャット再入室 | エンドユーザー | チャットID、期限、再開ボタン、期限切れ案内 | ウィジェットメニューまたは再入室URLから遷移 |

AI未解決時は画面遷移で履歴を失わせず、「カスタマーサポートとのチャットに切り替わりました」とチャットIDを返信する。チャットIDはヘッダー付近にも常時表示する。サポートチャット開始時にメールアドレス・氏名は収集しない。

### <span id="32-apiデータ詳細設計"></span>3.2 API・データ詳細設計

| API | 用途 | 認証・認可 |
|----|----|----|
| `POST /widget/v1/chat-rooms` | 匿名チャット部屋作成、チャットID・再入室トークン返却 | ウィジェット公開キー、許可ドメイン、セッション |
| `POST /widget/v1/chat-rooms/{id}/messages` | エンドユーザー投稿 | 再入室トークンまたは作成元セッション |
| `GET /widget/v1/reentry/{token}` | チャット部屋再入室 | HMAC検証済み未使用・有効期限内トークン |
| `GET /chat-rooms` | 管理者向け一覧 | 対象プロジェクトへの有効割当 |
| `GET/POST /chat-rooms/{id}/messages` | 履歴取得・管理者返信 | `requireChatRoom` |
| `PATCH /chat-rooms/{id}` | 担当者変更 | 対象プロジェクトへの有効割当 |
| `PATCH /projects/{id}` | デフォルト担当者変更 | オーナー / 対象プロジェクト管理者 |

| テーブル・列 | 用途 |
|----|----|
| `end_users` | 匿名エンドユーザー主体。メールアドレスは必須にしない |
| `chat_rooms` | チャットID、プロジェクト、エンドユーザー、担当者、起点質問ログを保持 |
| `chat_messages` | 投稿者種別、本文、既読、投稿日時を保持 |
| `T_ACCESS_TOKENS(purpose='reentry')` | 30日有効の再入室トークンをHMACで保持 |
| `M_PROJECTS.default_assignee_user_id` | 新規部屋のデフォルト担当者 |

チャット ID 採番、匿名エンドユーザー作成、メッセージ送受信、既読、管理者向け通知、再入室フローは本機能内で完結させる。未解決質問 ID・FAQ 登録状況・部屋のオープン / クローズ状態は扱わない。

### <span id="33-実装モジュール構成"></span>3.3 実装モジュール構成

```
worker-main-api/src/
├── routes/
│   └── chat-rooms.ts         # /chat-rooms/* CRUD + メッセージ送受信 + 担当割当 PATCH（管理者側）
├── handlers/
├── domain/
│   ├── chat-message.ts       # 投稿文字数・頻度制限（純関数）
│   └── chat-assignee.ts      # 担当者解決（自動割当・フォールバック）純関数
├── repository/
│   ├── chat-rooms.ts
│   └── chat-messages.ts
└── middleware/
    └── authorize.ts          # requireChatRoom / requireProject 連動

worker-widget-api/src/
├── routes/
│   ├── chat-rooms.ts         # /widget/v1/chat-rooms/* CRUD（エンドユーザー側）
│   └── reentry.ts            # SCR-024 連携、再入室トークン検証
└── middleware/
    └── widget-session.ts
```

### <span id="34-再入室トークン"></span>3.4 再入室トークン

```
// 再入室トークンは長寿命のため、T_ACCESS_TOKENS テーブルに meta.chatRoomId を内包
// 失効・ローテーション運用:
// - 匿名チャット部屋作成時に発行し、API レスポンスでブラウザへ直接返す
// - チャット ID は照会用であり、再入室認証には使用しない
// - 30 日経過で expires_at に達し失効
// - 期限切れ・紛失時はメール再発行せず、新しいお問い合わせを開始する
```

MVP側のトークン設計とは分離し、本機能内で定義する。

### <span id="34a-担当者解決ロジックfr-086ac"></span>3.4a 担当者解決ロジック（FR-086a〜c）

担当者(`chat_rooms.assignee_user_id`)は NOT NULL であり、未割当状態を作らない。担当者の確定は以下の純関数で解決する。

```
// domain/chat-assignee.ts
// 新規チャット部屋作成時の担当者を解決する(FR-086b)。
// 優先順位:
//   1. M_PROJECTS.default_assignee_user_id が設定され、かつ当該ユーザーが
//      当該プロジェクトに有効割当(M_PRJ_USER_ASGN.valid=1)を持つ → その管理者
//   2. 上記以外(未設定 / 無効化済 / 当該PJ未割当) → オーナー(M_OWNERS.id)
// オーナーは契約あたり常に 1 名存在し全プロジェクトの暗黙 admin のため、
// 必ず担当者を確定でき、未割当の部屋は生成されない(FR-086a)。
function resolveInitialAssignee(project, defaultAssigneeValid): string {
  if (project.default_assignee_user_id && defaultAssigneeValid) {
    return project.default_assignee_user_id
  }
  return project.owner_id // オーナーへフォールバック
}
```

- **担当者変更(SCR-033, `PATCH /chat-rooms/{id}`)**: `assigneeUserId` は必須・`null` 不可。当該プロジェクトに有効割当を持つ管理者(オーナー / `admin` / `member`)のみ受理。それ以外は 400 `E-INPUT-ASSIGNEE`。変更操作自体は `member`+ の誰でも可。
- **自動割り当て設定(SCR-034, `PATCH /projects/{id}` `defaultAssigneeUserId`)**: SCR-013チャット配下の「自動割り当て」タブから操作する。オーナー / 該当PJの`admin`のみ。`null`を許容し、未設定時はオーナーへフォールバックする。
- **担当管理者の論理削除時の付け替え**: 担当者であった管理者ユーザーがアカウント論理削除(`users.valid=0`)される場合、当該管理者が担当する全部屋の `assignee_user_id` を `resolveInitialAssignee` と同じ優先順位(デフォルト担当者→オーナー)で付け替えてから `valid=0` に更新する。これにより NOT NULL 制約と「未割当を作らない」不変条件を維持する。デフォルト担当者(`M_PROJECTS.default_assignee_user_id`)が当該削除ユーザーを指していた場合も同フローで `NULL` 化(以後オーナーへフォールバック)する。

### <span id="35-機能境界"></span>3.5 機能境界

チャット部屋は未解決質問と独立して作成する。同じ質問ログを起点とする場合も `source_question_log_id` を個別に保持するだけとし、チャットの投稿・既読・通知・再入室から未解決質問の FAQ 登録状況を更新しない。

### <span id="36-関連する横断設計"></span>3.6 関連する横断設計

- 認可: `requireChatRoom` でオーナー境界を検証
- 通知: メッセージ受信時に管理者へ通知
- 監査ログ: `chat.create` / `chat.message.send` / `chat.message.read` を `retention_class=general` で記録

## <span id="4-関連設計"></span>4. 関連設計

| 種別       | 参照先                           |
|------------|----------------------------------|
| Future要件 | [FUT06-req.md](FUT06-req.md) |
| Future概要 | [FUT06.md](FUT06.md)         |
| Future索引 | [index.md](index.md)         |

## <span id="5-テスト観点"></span>5. テスト観点

| AC ID | テスト ID | テスト方式 | テストファイル |
|----|----|----|----|
| AC-011 | `e2e-chat-flow-001` | E2E | `apps/{admin,widget}/e2e/chat/flow.spec.ts` |
| AC-025 | `e2e-reentry-001` | E2E | `apps/widget/e2e/reentry.spec.ts` |

### <span id="51-その他観点"></span>5.1 その他観点

| 観点 | 内容 |
|----|----|
| 単体 | 投稿文字数・頻度制限 / 再入室時の新トークン発行 / `resolveInitialAssignee`(デフォルト担当者あり→その人 / なし→オーナー / 無効割当→オーナー) |
| 結合 | 管理者送信 → エンドユーザー再入室 → 返信 → 未解決質問状況が不変 / 新規チャット作成時に担当者が必ず 1 名セットされる / 担当管理者の論理削除で担当部屋がデフォルト担当者(またはオーナー)へ付け替わる |
| 異常系 | 期限切れ再入室トークン使用時の 400 `TOKEN_EXPIRED` / 担当者に `null` または当該 PJ 未割当ユーザーを指定 → 400 `E-INPUT-ASSIGNEE` / メンバーがデフォルト担当者設定 → 403 |
| 境界値 | 再入室トークン TTL 30 日ぴったり / 同一ウィジェットセッションの新規チャット 24 時間 5 件 |
| 性能 | `POST /api/v1/chats/.../messages` p95 \< 500ms（NFR-104） |
| ショートカット | SCR-033 個別チャット部屋で `Ctrl+Enter`（macOS では `Cmd+Enter`）でメッセージ送信 |

## <span id="6-未確定事項確認事項"></span>6. 未確定事項・確認事項

| 確認事項ID | 確認内容                             | 優先度 | ステータス |
|------------|--------------------------------------|--------|------------|
| \-         | その他は v1.0 リリース時点で確定済み | 低     | 確認済     |

---

---

---

<!-- portal-bottom -->
[将来対応](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
