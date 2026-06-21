<!-- portal-top -->
[設計ポータル](../README.md) ／ [基本設計](index.md) ／ **ユースケース・シーケンス設計書**
<!-- /portal-top -->

# ユースケース・シーケンス設計書

**画面設計・API設計・データベース設計の 3 つの独立設計書を横断し、業務の流れ(ユースケース)を「アクター → 画面 → API → DB」のシーケンスで明確化する設計書です。** 各設計書をどう組み合わせて 1 つの業務が成立するかを、本書のシーケンス図とトレーサビリティ・マトリクスで追跡できます。

*版数 v2.2 ・ 更新 2026-06-20 ・ ユースケース 10 ・ 横断設計書*

> [!NOTE]
> **本書と詳細ユースケースの関係** 本書は複数画面・非同期処理をまたぐ横断フロー(粗粒度の 10 UC)を示します。画面イベント単位(`EV-xx`)に 1:1 対応した詳細ユースケースと、システム起点(バッチ・Webhook・非同期ジョブ)のユースケースは [ユースケース一覧](../04_usecases/index.md) を参照してください。

## <span id="model"></span>0.横断設計の考え方

本システムの 1 操作は、必ず次の 5 層を縦に貫きます。本書はこの縦串を「フロー」として可視化します。

要件FR / BR → 画面SCR(アクション) → API/v1 エンドポイント → DBテーブル(CRUD) <div class="card-grid cols-3">
<div class="card"><div class="lead-ico">①</div><h4>要件 → 画面</h4><p>要件(FR)がどの画面・アクションに落ちるかは <a href="index.md#fr">ポータル §3</a> と <a href="01_screen-design.md">画面設計</a> が担う。</p></div>
<div class="card"><div class="lead-ico">②</div><h4>画面 → API → DB</h4><p>画面の各アクションが呼ぶ API と触れるテーブルは <a href="01_screen-design.md#flow">画面設計 §4</a> に集約。</p></div>
<div class="card"><div class="lead-ico">③</div><h4>横断フロー</h4><p>複数画面・API・非同期処理にまたがる業務の流れを本書のシーケンス図で繋ぐ。</p></div>
</div>

## <span id="list"></span>1.ユースケース一覧

主要な 10 ユースケースです。各 UC はシーケンス図(§2)へリンクします。

<table style="min-width:760px">
<colgroup>
<col />
<col style="width: 28%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col />
</colgroup>
<thead>
<tr>
<th>UC ID</th>
<th>ユースケース</th>
<th>アクター</th>
<th>主な画面</th>
<th>関連要件</th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="#UC-01"><code>UC-01</code></a></td>
<td><strong>アカウント新規登録〜メール確認</strong></td>
<td>契約オーナー(新規)</td>
<td><a href="01_screen-design.md#SCR-002" style="font-size:10.5px">SCR-002</a> <a href="01_screen-design.md#SCR-013" style="font-size:10.5px">SCR-013</a></td>
<td style="font-size: 11.5px">FR01 アカウント管理</td>
</tr>
<tr>
<td><a href="#UC-02"><code>UC-02</code></a></td>
<td><strong>ログイン</strong></td>
<td>全認証ユーザー</td>
<td><a href="01_screen-design.md#SCR-001" style="font-size:10.5px">SCR-001</a></td>
<td style="font-size: 11.5px">FR01 アカウント管理</td>
</tr>
<tr>
<td><a href="#UC-03"><code>UC-03</code></a></td>
<td><strong>プロジェクト作成</strong></td>
<td>オーナー</td>
<td><a href="01_screen-design.md#SCR-004" style="font-size:10.5px">SCR-004</a> <a href="01_screen-design.md#SCR-004-001" style="font-size:10.5px">SCR-004-001</a></td>
<td style="font-size: 11.5px">FR03 プロジェクト管理</td>
</tr>
<tr>
<td><a href="#UC-04"><code>UC-04</code></a></td>
<td><strong>メンバー招待〜アカウント有効化</strong></td>
<td>オーナー / メンバー → 被招待者</td>
<td><a href="01_screen-design.md#SCR-009-001" style="font-size:10.5px">SCR-009-001</a> <a href="01_screen-design.md#SCR-018" style="font-size:10.5px">SCR-018</a></td>
<td style="font-size: 11.5px">FR02 ユーザー管理</td>
</tr>
<tr>
<td><a href="#UC-05"><code>UC-05</code></a></td>
<td><strong>FAQ 作成・公開</strong></td>
<td>オーナー / メンバー+</td>
<td><a href="01_screen-design.md#SCR-006" style="font-size:10.5px">SCR-006</a> <a href="01_screen-design.md#SCR-006-001" style="font-size:10.5px">SCR-006-001</a></td>
<td style="font-size: 11.5px">FR04 FAQ管理</td>
</tr>
<tr>
<td><a href="#UC-06"><code>UC-06</code></a></td>
<td><strong>FAQ CSV 一括インポート(非同期)</strong></td>
<td>オーナー / メンバー+</td>
<td><a href="01_screen-design.md#SCR-006-002" style="font-size:10.5px">SCR-006-002</a></td>
<td style="font-size: 11.5px">FR17 インポート・エクスポート</td>
</tr>
<tr>
<td><a href="#UC-07"><code>UC-07</code></a></td>
<td><strong>エンドユーザー質問 → AI 回答</strong></td>
<td>エンドユーザー(公開)</td>
<td><a href="01_screen-design.md#WIDGET" style="font-size:10.5px">WIDGET</a></td>
<td style="font-size: 11.5px">FR05 AI回答<br />
FR20 AI推論動作</td>
</tr>
<tr>
<td><a href="#UC-08"><code>UC-08</code></a></td>
<td><strong>未解決質問 → FAQ 化</strong></td>
<td>オーナー / メンバー+</td>
<td><a href="01_screen-design.md#SCR-005" style="font-size:10.5px">SCR-005</a> <a href="01_screen-design.md#SCR-005-001" style="font-size:10.5px">SCR-005-001</a> <a href="01_screen-design.md#SCR-006-001" style="font-size:10.5px">SCR-006-001</a></td>
<td style="font-size: 11.5px">FR06 未解決質問登録<br />
FR07 未解決質問からFAQ登録</td>
</tr>
<tr>
<td><a href="#UC-09"><code>UC-09</code></a></td>
<td><strong>利用量超過 → 支払方法ゲート</strong></td>
<td>オーナー</td>
<td><a href="01_screen-design.md#SCR-021" style="font-size:10.5px">SCR-021</a> <a href="01_screen-design.md#SCR-022" style="font-size:10.5px">SCR-022</a></td>
<td style="font-size: 11.5px">FR09 利用量・課金</td>
</tr>
<tr>
<td><a href="#UC-10"><code>UC-10</code></a></td>
<td><strong>退会申請(90日猶予)</strong></td>
<td>オーナー</td>
<td><a href="01_screen-design.md#SCR-023" style="font-size:10.5px">SCR-023</a> <a href="01_screen-design.md#SCR-014" style="font-size:10.5px">SCR-014</a></td>
<td style="font-size: 11.5px">FR01 アカウント管理<br />
FR13 プライバシー・データ管理</td>
</tr>
</tbody>
</table>

## <span id="seq"></span>2.シーケンス図(フロー)

各ユースケースを「アクター → 画面(SCR)→ API → DB」のシーケンスで示します。メッセージ中の `テーブル名(CRUD)` は [データベース設計書](03_database-design.md) のテーブルに対応します。

### <span id="UC-01"></span>UC-01 アカウント新規登録〜メール確認

**アクター** 契約オーナー(新規) **関連要件** FR01 アカウント管理

|  |  |
|----|----|
| **事前条件** | 未登録のメールアドレスを保有している。 |
| **事後条件** | `M_CONTRACT` が `status=active` で作成され、ログイン可能になる。 |
| **関連画面** | [`SCR-002`](01_screen-design.md#SCR-002) ・ [`SCR-013`](01_screen-design.md#SCR-013) |

```mermaid
sequenceDiagram
  autonumber
  actor U as オーナー(新規)
  participant S2 as 画面 SCR-002 登録
  participant API as API /v1
  participant DB as DB (D1)
  participant ML as メール配信IF
  U->>S2: メール/パスワード/規約同意を入力
  S2->>API: POST /auth/signup
  API->>DB: M_USER(C) ・ M_CONTRACT(C) ・ T_TERMS_AGREE(C) ・ T_ACCESS_TOKENS(C)
  DB-->>API: 
  API->>ML: 確認メール送信(TPL-VERIFY)
  ML-->>API: 
  API-->>S2: 201 受付・確認メール送信済
  U->>API: メール内リンク POST /auth/email-verifications/{token}
  API->>DB: T_ACCESS_TOKENS(RU) ・ M_CONTRACT(U:verified)
  DB-->>API: 
  API-->>U: 画面 SCR-013 確認完了 → ログインへ
```

### <span id="UC-02"></span>UC-02 ログイン

**アクター** 全認証ユーザー **関連要件** FR01 アカウント管理

|              |                                                         |
|--------------|---------------------------------------------------------|
| **事前条件** | 有効なアカウントを保有している。                        |
| **事後条件** | `T_SESSIONS` が発行され、既定ワークスペースへ着地する。 |
| **関連画面** | [`SCR-001`](01_screen-design.md#SCR-001)              |

```mermaid
sequenceDiagram
  autonumber
  actor U as 利用者
  participant S as 画面 SCR-001 ログイン
  participant API as API /v1
  participant DB as DB (D1)
  U->>S: メール・パスワード入力
  S->>API: POST /auth/login
  API->>DB: M_CONTRACT(RU) / M_PRJ_USERS(RU) 認証
  DB-->>API: 
  API->>DB: T_SESSIONS(C) セッション発行
  DB-->>API: 
  API-->>S: 200 + Cookie → 既定WSへ
```

### <span id="UC-03"></span>UC-03 プロジェクト作成

**アクター** オーナー **関連要件** FR03 プロジェクト管理

|  |  |
|----|----|
| **事前条件** | 契約ワークスペースにログインしている。 |
| **事後条件** | `M_PROJECTS` と許可ドメインが作成され、ウィジェット公開鍵が払い出される。 |
| **関連画面** | [`SCR-004`](01_screen-design.md#SCR-004) ・ [`SCR-004-001`](01_screen-design.md#SCR-004-001) |

```mermaid
sequenceDiagram
  autonumber
  actor O as オーナー
  participant S4 as 画面 SCR-004 一覧
  participant SM as モーダル SCR-004-001
  participant API as API /v1
  participant DB as DB (D1)
  O->>S4: 「+ 新規プロジェクト」
  S4->>SM: 作成モーダルを開く
  SM-->>S4: 
  O->>SM: 名称・ドメイン入力 → 作成
  SM->>API: POST /projects
  API->>DB: M_PROJECTS(C) ・ M_ALLOWED_DOMAINS(C)
  DB-->>API: 
  API-->>SM: 201 + widget_public_key
  SM-->>S4: 一覧へ戻り新規行を表示
```

### <span id="UC-04"></span>UC-04 メンバー招待〜アカウント有効化

**アクター** オーナー / メンバー → 被招待者 **関連要件** FR02 ユーザー管理

|  |  |
|----|----|
| **事前条件** | オーナーまたは当該プロジェクトのメンバーである。 |
| **事後条件** | 被招待者の `M_USER`(予約行)が有効化(`status='active'`)され、当該プロジェクトのメンバー割当(`M_PRJ_USERS`)が有効になる。 |
| **関連画面** | [`SCR-009-001`](01_screen-design.md#SCR-009-001) ・ [`SCR-018`](01_screen-design.md#SCR-018) |

```mermaid
sequenceDiagram
  autonumber
  actor A as メンバー
  actor I as 被招待者
  participant SM as モーダル SCR-009-001
  participant API as API /v1
  participant DB as DB (D1)
  participant ML as メール配信IF
  A->>SM: メールアドレスを指定し招待
  SM->>API: POST /projects/{id}/members
  API->>DB: M_USER(C:予約行) ・ M_PRJ_USERS(C) ・ T_ACCESS_TOKENS(C)
  DB-->>API: 
  API->>ML: 招待メール送信(H_NOTIF_LOGS(C))
  ML-->>API: 
  I->>API: 招待リンク POST /auth/invitations/{token}/activate
  API->>DB: T_ACCESS_TOKENS(RU) ・ M_USER(U) ・ M_PRJ_USERS(U) ・ T_TERMS_AGREE(C)
  DB-->>API: 
  API-->>I: 画面 SCR-018 有効化完了
```

### <span id="UC-05"></span>UC-05 FAQ 作成・公開

**アクター** オーナー / メンバー+ **関連要件** FR04 FAQ管理

|  |  |
|----|----|
| **事前条件** | プロジェクトに編集権限で参加している。 |
| **事後条件** | `M_FAQS` が `status=published` となる。 |
| **関連画面** | [`SCR-006`](01_screen-design.md#SCR-006) ・ [`SCR-006-001`](01_screen-design.md#SCR-006-001) |

```mermaid
sequenceDiagram
  autonumber
  actor M as 編集者
  participant S6 as 画面 SCR-006 一覧
  participant SE as 画面 SCR-006-001 編集
  participant API as API /v1
  participant DB as DB (D1)
  M->>S6: 「FAQを作成」/ FAQ ID クリック
  S6->>SE: 編集画面へ
  SE-->>S6: 
  M->>SE: 質問・回答・状態=公開 を保存
  SE->>API: PATCH /faqs/{id} (version 楽観ロック)
  API->>DB: M_FAQS(U:published, publishedAt)
  DB-->>API: 
  API-->>SE: 200 更新後FAQ
  Note over API,DB: TP_FAQ_FTS は published 連動で更新
```

### <span id="UC-06"></span>UC-06 FAQ CSV 一括インポート(非同期)

**アクター** オーナー / メンバー+ **関連要件** FR17 インポート・エクスポート

|  |  |
|----|----|
| **事前条件** | CSV(UTF-8・最大1000件)を用意している。 |
| **事後条件** | 各行が新規/上書き判定され `M_FAQS` に取り込まれる(行単位エラー集計)。 |
| **関連画面** | [`SCR-006-002`](01_screen-design.md#SCR-006-002) |

```mermaid
sequenceDiagram
  autonumber
  actor M as 編集者
  participant SM as モーダル SCR-006-002
  participant API as API /v1
  participant Q as 非同期ジョブ
  participant DB as DB (D1)
  M->>SM: CSV をアップロード
  SM->>API: POST /faqs/import (multipart)
  API->>API: 形式検証(CSV/UTF-8/1000件)
  API->>Q: 取込ジョブ受付
  Q-->>API: 
  API-->>SM: 202 jobId / processing
  Q->>DB: 行単位 M_FAQS(CRU)
  DB-->>Q: 
  Q-->>SM: 完了通知(成功件数/失敗明細)
```

### <span id="UC-07"></span>UC-07 エンドユーザー質問 → AI 回答

**アクター** エンドユーザー(公開) **関連要件** FR05 AI回答 / FR20 AI推論動作

|  |  |
|----|----|
| **事前条件** | ウィジェットが許可ドメインに設置されている。 |
| **事後条件** | 質問が `H_QUESTION_LOGS` に記録され、低確信度なら `T_INQUIRIES` に未解決登録される。利用量を計測。 |
| **関連画面** | [`WIDGET`](01_screen-design.md#WIDGET) |

```mermaid
sequenceDiagram
  autonumber
  actor E as エンドユーザー
  participant W as ウィジェット
  participant API as API /widget/v1
  participant AI as AI推論IF
  participant DB as DB (D1)
  W->>API: POST /widget/v1/bootstrap (公開鍵+ドメイン検証)
  API->>DB: M_PROJECTS(R) ・ M_ALLOWED_DOMAINS(R)
  DB-->>API: 
  E->>W: 質問を入力
  W->>API: POST /widget/v1/ask
  API->>DB: M_FAQS(R) 候補検索
  DB-->>API: 
  API->>AI: 推論(信頼度しきい値判定)
  AI-->>API: 
  API->>DB: H_QUESTION_LOGS(C) ・ T_USAGE_METER(CU)
  DB-->>API: 
  alt 低確信度(未解決)
    API->>DB: T_INQUIRIES(C) 未解決登録
    DB-->>API: 
  end
  API-->>W: 回答 + 確信度
```

### <span id="UC-08"></span>UC-08 未解決質問 → FAQ 化

**アクター** オーナー / メンバー+ **関連要件** FR06 未解決質問登録 / FR07 未解決質問からFAQ登録

|  |  |
|----|----|
| **事前条件** | UC-07 で未解決質問が登録されている。 |
| **事後条件** | 未解決質問を基に `M_FAQS` が作成され、`T_INQUIRIES` が解決状態に更新される。 |
| **関連画面** | [`SCR-005`](01_screen-design.md#SCR-005) ・ [`SCR-005-001`](01_screen-design.md#SCR-005-001) ・ [`SCR-006-001`](01_screen-design.md#SCR-006-001) |

```mermaid
sequenceDiagram
  autonumber
  actor M as 担当者
  participant S5 as 画面 SCR-005 一覧/詳細
  participant SE as 画面 SCR-006-001 編集
  participant API as API /v1
  participant DB as DB (D1)
  M->>S5: 要対応の質問を確認
  S5->>API: GET /inquiries ・ GET /inquiries/{id}
  API->>DB: T_INQUIRIES(R) ・ H_QUESTION_LOGS(R)
  DB-->>API: 
  M->>SE: 「FAQ化」→ 内容を編集し公開
  SE->>API: POST /faqs (未解決質問の内容をコピー)
  API->>DB: M_FAQS(C) ・ H_INQUIRY_FAQ(C) ・ T_INQUIRIES(U:resolved)
  DB-->>API: 
  API-->>SE: 201 作成FAQ
```

### <span id="UC-09"></span>UC-09 利用量超過 → 支払方法ゲート

**アクター** オーナー **関連要件** FR09 利用量・課金

|  |  |
|----|----|
| **事前条件** | 当月の質問数が無料枠に近づいている。 |
| **事後条件** | 無料枠 100% 超過かつ支払方法未登録ならウィジェットを制限(契約は active のまま)。 |
| **関連画面** | [`SCR-021`](01_screen-design.md#SCR-021) ・ [`SCR-022`](01_screen-design.md#SCR-022) |

```mermaid
sequenceDiagram
  autonumber
  participant API as API /widget+/v1
  participant DB as DB (D1)
  actor O as オーナー
  participant S21 as 画面 SCR-021/SCR-022
  API->>DB: T_USAGE_METER(CU) 質問ごとに加算
  DB-->>API: 
  Note over API,DB: 80%=黄 / 100%=赤 / 125%=強調 (M_PRJ_QUOTA_LIMITS 参照)
  O->>S21: 利用量と上限/請求を確認
  S21->>API: GET /projects/{id}/quota-limits ・ GET /billing/summary
  API->>DB: M_PRJ_QUOTA_LIMITS(R) ・ T_USAGE_METER(R) ・ T_BILL_SUBS(R)
  DB-->>API: 
  alt 100%超過 & 支払方法未登録
    API-->>S21: PaymentMethodBanner(赤)+ 登録CTA
  end
```

### <span id="UC-10"></span>UC-10 退会申請(90日猶予)

**アクター** オーナー **関連要件** FR01 アカウント管理 / FR13 プライバシー・データ管理

|  |  |
|----|----|
| **事前条件** | オーナーとしてログインしている。 |
| **事後条件** | `T_WITHDRAW_REQ` が作成され、`M_CONTRACT.status` が退会フローに入る。 |
| **関連画面** | [`SCR-023`](01_screen-design.md#SCR-023) ・ [`SCR-014`](01_screen-design.md#SCR-014) |

```mermaid
sequenceDiagram
  autonumber
  actor O as オーナー
  participant S23 as 画面 SCR-023 設定
  participant S14 as 画面 SCR-014 退会申請
  participant API as API /v1
  participant DB as DB (D1)
  O->>S23: 危険な操作セクション → 退会
  S23->>S14: 退会申請画面(再認証 L3)
  S14-->>S23: 
  O->>S14: 対象名タイプ + パスワード再入力 → 申請
  S14->>API: POST /withdrawal-requests
  API->>DB: T_WITHDRAW_REQ(C) ・ M_CONTRACT(RU:withdraw)
  DB-->>API: 
  API-->>S14: 受付(90日猶予の取消可能期間)
```

## <span id="matrix"></span>3.縦串トレーサビリティ・マトリクス

要件群(FR)→ ユースケース → 画面 → 中核 API → 主テーブル の対応一覧です。詳細なアクション単位の対応は [画面設計書 §4](01_screen-design.md#flow) を正本とします。

| 要件群 | UC | 画面 | 中核API | 主テーブル |
|----|----|----|----|----|
| **FR01 アカウント管理** | UC-01 / UC-02 | SCR-001/002/013 | `POST /auth/signup ・ /auth/login` | `M_USER` ・ `M_CONTRACT` ・ `T_SESSIONS` ・ `T_TERMS_AGREE` |
| **FR02 ユーザー管理** | UC-04 | SCR-009 / SCR-009-001 / SCR-018 | `POST /projects/{id}/members` | `M_USER` ・ `M_PRJ_USERS` ・ `T_ACCESS_TOKENS` |
| **FR03 プロジェクト管理** | UC-03 | SCR-004 / SCR-004-001 | `POST/PATCH/DELETE /projects` | `M_PROJECTS` ・ `M_ALLOWED_DOMAINS` |
| **FR04 FAQ管理** | UC-05 | SCR-006 / SCR-006-001 | `PATCH /faqs/{id}` | `M_FAQS` ・ `TP_FAQ_FTS` |
| **FR05 / FR20 AI回答** | UC-07 | WIDGET | `POST /widget/v1/ask` | `H_QUESTION_LOGS` ・ `M_FAQS` ・ `T_USAGE_METER` |
| **FR06 / FR07 未解決→FAQ** | UC-08 | SCR-005 / SCR-005-001 | `GET/PATCH /inquiries ・ POST /faqs` | `T_INQUIRIES` ・ `M_FAQS` ・ `H_QUESTION_LOGS` |
| **FR09 利用量・課金** | UC-09 / UC-10(課金) | SCR-021 / SCR-022 | `GET /billing/summary ・ /quota-limits` | `T_USAGE_METER` ・ `T_BILL_SUBS` ・ `M_PRJ_QUOTA_LIMITS` |
| **FR11 / FR15 通知・お知らせ** | — | SCR-011 / SCR-012 | `GET /me/announcements` | `T_INBOX_MSG` ・ `M_SERVICE_ANNOUNCE` |
| **FR12 ウィジェット** | UC-07 | SCR-007 / WIDGET | `POST /widget/v1/bootstrap ・ /widget-key/rotate` | `M_PROJECTS` ・ `M_ALLOWED_DOMAINS` ・ `T_PRJ_LEGACY_KEYS` |
| **FR13 プライバシー・データ** | UC-10(退会) | SCR-023 / SCR-014 | `POST /withdrawal-requests` | `T_WITHDRAW_REQ` ・ `M_CONTRACT` |
| **FR17 インポート・エクスポート** | UC-06 | SCR-006-002 | `POST /faqs/import` | `M_FAQS` |

> [!TIP]
> **縦串が一直線に追える** 要件(FR)から DB テーブルまで、各層の設計書を本マトリクスとシーケンス図がつなぎます。逆方向(テーブル → 使用元 API / 画面)は [データベース設計書 §2](03_database-design.md#map) の「使用元」で追跡できます。

---

<!-- portal-bottom -->
[基本設計](index.md) ・ [↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
