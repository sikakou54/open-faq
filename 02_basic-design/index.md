<!-- portal-top -->
[設計ポータル](../README.md) ／ **基本設計**
<!-- /portal-top -->

# 基本設計ポータル

FAQ AI ウィジェット SaaS / メインシステム(利用者向け)の基本設計を、**画面 / API / データベースの 3 独立設計書** と、それらを横断する**ユースケース・シーケンス設計書** として構成しています。要件定義から DB までを縦串で追跡できます。

|                  |                                                       |
|------------------|-------------------------------------------------------|
| **対象システム** | FAQ AI ウィジェット SaaS / メインシステム(利用者向け) |
| **版数**         | v2.0                                                  |
| **更新日**       | 2026-06-19                                            |
| **想定読者**     | 設計レビュアー / 実装担当者 / AI 駆動開発担当         |

## <span id="map"></span>1.設計書マップ

<div class="card-grid cols-2">
<a class="doc-card" href="01_screen-design.md"><span class="dc-k">01 ・ 独立</span><h4>画面設計書</h4><p>全 28 画面 + ウィジェットをワークスペース別に整理。各画面の「アクション → API → DB」を §4 に集約。</p></a>
<a class="doc-card" href="02_api-design.md"><span class="dc-k">02 ・ 独立</span><h4>API設計書</h4><p>全 51 エンドポイントを 14 機能グループに整理。各 API の権限と I/O テーブル(CRUD)を明示。</p></a>
<a class="doc-card" href="03_database-design.md"><span class="dc-k">03 ・ 独立</span><h4>データベース設計書</h4><p>31 テーブルを 7 機能ドメインに分類。ER 図・コード値・使用元(逆引き)を併記。</p></a>
<a class="doc-card" href="04_usecase-design.md"><span class="dc-k">04 ・ 横断</span><h4>ユースケース・シーケンス設計書</h4><p>10 ユースケースを「アクター → 画面 → API → DB」のシーケンス図で可視化。縦串マトリクス付き。</p></a>
<a class="doc-card" href="05_billing-design.md"><span class="dc-k">05 ・ 横断</span><h4>課金・請求設計書</h4><p>課金モデル・質問数上限・支払方法ゲート・契約状態ライフサイクル・利用量集計・Webhook 受信方針。</p></a>
<a class="doc-card" href="06_mail-design.md"><span class="dc-k">06 ・ 横断</span><h4>メール設計書</h4><p>送信元・i18n・サニタイズ等の共通基準と全 TPL テンプレートの件名・本文・送信契機、配信運用。</p></a>
<a class="doc-card" href="07_auth-design.md"><span class="dc-k">07 ・ 横断</span><h4>認証・認可設計書</h4><p>認証方式・重要操作の再認証・認証フロー・セッション設計・認可モデルと判定フロー・規約再同意割込み。</p></a>
</div>

## <span id="fr"></span>2.要件定義 → 基本設計 の落とし込み

要件定義(機能要件 FR01〜FR21)が、どの画面・API・テーブルに落ちるかの対応一覧です。1 つの要件群が「画面(操作)→ API(処理)→ DB(記録)」へどう展開されるかを示し、横断フローはユースケース(UC)列から辿れます。

> [!NOTE]
> <span class="c-ic">ℹ</span>
>
> <div>
>
> 本表は要件 → 設計の入口(索引)です。アクション単位の精密な対応は [画面設計 §4](01_screen-design.md#flow)、テーブル単位の逆引きは [データベース設計 §6](03_database-design.md#def) を正本とします。
>
> </div>

| FR | 機能群 | 概要 | 画面 | 中核API | 主テーブル | UC |
|----|----|----|----|----|----|----|
| `FR01` | **アカウント管理** | 新規登録 / ログイン / 再認証 / ログアウト | SCR-001〜003 / 013 | `POST /auth/signup` ・ `/auth/login` | `M_CONTRACT` `T_SESSIONS` `T_ACCESS_TOKENS` `T_TERMS_AGREE` | [UC-01 / UC-02](04_usecase-design.md#UC-01) |
| `FR02` | **ユーザー管理** | プロジェクト単位のメンバー管理 | SCR-009 / 009-001 / 018 | `POST /projects/{id}/members` | `M_PRJ_USERS` `M_PRJ_USERS` | [UC-04](04_usecase-design.md#UC-04) |
| `FR03` | **プロジェクト管理** | プロジェクト作成 / 編集 / 削除 | SCR-004 / 004-001 | `POST/PATCH/DELETE /projects` | `M_PROJECTS` `M_ALLOWED_DOMAINS` | [UC-03](04_usecase-design.md#UC-03) |
| `FR04` | **FAQ管理** | FAQ CRUD + 公開 + 改版 | SCR-006 / 006-001 | `PATCH /faqs/{id}` | `M_FAQS` `H_FAQ_REV` `TP_FAQ_FTS` | [UC-05](04_usecase-design.md#UC-05) |
| `FR05` | **AI回答** | AI 推論 + 信頼度しきい値判定 | WIDGET | `POST /widget/v1/ask` | `H_QUESTION_LOGS` `M_FAQS` `TP_AI_THRESH_CACHE` | [UC-07](04_usecase-design.md#UC-07) |
| `FR06` | **未解決質問登録** | 未解決質問の登録 / 一覧 | SCR-005 / 005-001 | `GET /inquiries` | `T_INQUIRIES` `H_QUESTION_LOGS` | [UC-08](04_usecase-design.md#UC-08) |
| `FR07` | **未解決→FAQ登録** | 未解決 → FAQ 候補化 / 公開 | SCR-005 / 006-001 | `POST /faqs` | `M_FAQS` `T_INQUIRIES` | [UC-08](04_usecase-design.md#UC-08) |
| `FR08` | **処理エラー** | エラー一覧 / 再実行 | (運用) | — | `H_ERROR_LOGS` | — |
| `FR09` | **利用量・課金** | 利用量メータリング / 請求 | SCR-016 / 021 / 022 | `GET /usage` ・ `/billing/summary` | `T_USAGE_METER` `T_BILL_SUBS` `T_BILL_INVOICES` `M_PRJ_QUOTA_LIMITS` | [UC-09](04_usecase-design.md#UC-09) |
| `FR10` | **管理ダッシュボード** | 利用状況 / プロジェクト概要 | SCR-016 / 008 | `GET /dashboard/summary` | `T_USAGE_METER` `H_QUESTION_LOGS` | — |
| `FR11` | **通知** | 通知 / インボックス / メール | SCR-011 / 012 | `GET /me/announcements` | `T_INBOX_MSG` `H_NOTIF_LOGS` | — |
| `FR12` | **ウィジェット** | ウィジェット配信 + 設定 + 許可ドメイン | SCR-007 / WIDGET | `POST /widget/v1/bootstrap` | `M_PROJECTS` `M_ALLOWED_DOMAINS` `T_PRJ_LEGACY_KEYS` | [UC-07](04_usecase-design.md#UC-07) |
| `FR13` | **プライバシー・データ管理** | プライバシー / データ削除 / 退会 | SCR-010 / 020 / 014 | `POST /withdrawal-requests` | `T_WITHDRAW_REQ` `M_TERMS_VER` | [UC-10](04_usecase-design.md#UC-10) |
| `FR14` | **セキュリティ** | 不正利用検知 / 鍵管理 / 監査 | (横断) | — | `H_AUDIT_LOGS` `M_EMAIL_SUPPRESS` | — |
| `FR15` | **お知らせ** | お知らせ配信 / 既読 | SCR-011 / 012 | `GET /me/announcements` | `M_SERVICE_ANNOUNCE` `T_ANNOUNCE_RCPT` `M_ANNOUNCE_AUD` | — |
| `FR16` | **検索・全文検索** | FTS 検索 | SCR-006 | `GET /projects/{id}/faqs/search` | `TP_FAQ_FTS` `M_FAQS` | — |
| `FR17` | **インポート・エクスポート** | FAQ の CSV 入出力 / ログ出力 | SCR-006 / 006-002 | `POST /faqs/import` ・ `/faqs/export` | `M_FAQS` `H_FAQ_REV` | [UC-06](04_usecase-design.md#UC-06) |
| `FR18` | **UX細部・データ運用** | UX 細部要件 / データ運用要件 | 全画面 | — | (横断) | — |
| `FR19` | **アクセス制御細部** | アクセス制御細部要件 | (横断) | — | (権限設計) | — |
| `FR20` | **AI推論動作** | AI 推論動作要件 | WIDGET | `POST /widget/v1/ask` | `TP_AI_THRESH_CACHE` | [UC-07](04_usecase-design.md#UC-07) |
| `FR21` | **SCR画面マスタ** | SCR 画面一覧マスタ | 全画面 | — | — | — |

## <span id="sys"></span>3.システム全体像

エンドユーザーの質問から課金までの主要データフローです。

```mermaid
flowchart LR
  EU([エンドユーザー]) -->|質問| W[ウィジェット]
  W -->|/widget/v1/ask| API[Workers API]
  API -->|FAQ検索| DB[(D1)]
  API -->|AI推論| OAI[AI推論IF]
  API -->|未解決| INQ[(T_INQUIRIES)]
  INQ --> ADM[管理画面 SCR-005]
  ADM -->|FAQ化| FAQ[(M_FAQS)]
  API -->|計測| MET[(T_USAGE_METER)]
  MET -->|月次集計| ST[Stripe]
  ST -->|Webhook| API
``` 主要データフロー(詳細は各ユースケースのシーケンス図) <div class="card-grid cols-3" style="margin-top:8px">
<div class="card"><h4>フロントエンド</h4><p>SPA(管理コンソール)+ 公開ウィジェット(エンドユーザー側 JS)</p></div>
<div class="card"><h4>API / インフラ</h4><p>Cloudflare Workers + REST(<code>/v1</code>)+ Cron + Queues</p></div>
<div class="card"><h4>データストア</h4><p>D1(SQLite・31 テーブル)+ KV + R2</p></div>
</div>

---

---

---

<!-- portal-bottom -->
[↑ 設計ポータル](../README.md)
<!-- /portal-bottom -->
