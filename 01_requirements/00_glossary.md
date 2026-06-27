# 用語集

> **このページは、要件・設計で用いる主要な用語の正式名称・別名・意味を一元管理する正本です。** 状態語の遷移は [状態モデル](../02_basic_design/08_state-model.md)、課金・設計値は [課金設計](../02_basic_design/05_billing-design.md) / [システム仕様書](../02_basic_design/07_system-spec.md) を参照する(本ページでは重複定義しない)。

*種別 用語集 ・ ステータス ドラフト*

| 用語(正式) | 別名・英語値 | 意味 | 参照 |
|----|----|----|----|
| <span id="GLO-001"></span>オーナー | `owner` | 対象プロジェクトの作成者。当該プロジェクトの管理・課金責任を負う全権者。立場は**プロジェクト単位**で定まる(請求名義のユーザー単位概念「課金アカウント保有者」[GLO-014](#GLO-014) とは別軸)。 | [PERM-005](../02_basic_design/04_permissions/PERM-005.md#PERM-005) |
| <span id="GLO-002"></span>メンバー | プロジェクトメンバー / `member` | 当該プロジェクトへの有効な割当を持つ非オーナー(招待されて参加した利用者)。業務語の正式名称は「メンバー」。DB 物理値も `actor_type` / `created_by_type` の許容値を **`member` に統一済**(旧称 `project_user` は廃止)。 | [PERM-005](../02_basic_design/04_permissions/PERM-005.md#PERM-005) / [TBL-027](../02_basic_design/02_backend/04_database/TBL-027.md#TBL-027) / [TBL-028](../02_basic_design/02_backend/04_database/TBL-028.md#TBL-028) |
| <span id="GLO-003"></span>アカウント利用者 | サイト運営者 | アカウントを保有する認証済み利用者の総称。プロジェクト単位の立場(オーナー / メンバー)を問わない包括語であり、権限判定上のロールではない。 | [要件定義 index](index.md#1-システム概要) |
| <span id="GLO-004"></span>未認証ユーザー | — | ログイン前(セッションが存在しない)の利用者。 | [PERM-001](../02_basic_design/04_permissions/PERM-001.md#PERM-001) |
| <span id="GLO-005"></span>ウィジェット利用者 | エンドユーザー / サイト訪問者 | プロジェクトに紐づく公開キーを用いてウィジェットを利用する者。管理画面とは独立した別系統の認証を使用する。 | [PERM-001](../02_basic_design/04_permissions/PERM-001.md#PERM-001) |
| <span id="GLO-006"></span>表示名 | `displayName`(API) / `M_USER.name`(DB) | 利用者のプロフィール名(画面・通知に表示する名称、最大 100 文字)。呼称を **「表示名」に統一済**(旧称「氏名」は廃止)。 | [UC-009](04_business_usecases/UC-009.md#UC-009) / [SCR-022](../02_basic_design/01_frontend/01_screens/SCR-022.md#SCR-022) / [TBL-001](../02_basic_design/02_backend/04_database/TBL-001.md#TBL-001) |
| <span id="GLO-007"></span>関連度 | `relevanceThreshold`(API) | 検索で取得した FAQ が利用者の質問内容にどれだけ一致するかを測る指標(0.0〜1.0)。回答可否判定のしきい値の一つ。 | [RULE-012](01_business_requirement/08_rule.md#RULE-012) / [API-067](../02_basic_design/02_backend/03_apis/API-067.md#API-067) |
| <span id="GLO-008"></span>信頼度 | 確信度 / `confidenceThreshold`・`confidence`(API) | AI が生成した回答の確からしさを測る指標(0.0〜1.0)。回答可否判定のしきい値の一つ。画面では「確信度」と表記するが同一概念。正式には「信頼度」に統一する。グローバル既定値は関連度 0.50 / 信頼度 0.60(RULE-012 が正本)で、API-067 応答例のグローバル階層(信頼度 0.6 / 関連度 0.5)と一致する。 | [RULE-012](01_business_requirement/08_rule.md#RULE-012) / [API-067](../02_basic_design/02_backend/03_apis/API-067.md#API-067) / [SCR-032](../02_basic_design/01_frontend/01_screens/SCR-032.md#SCR-032) |
| <span id="GLO-009"></span>確信度 | 信頼度 | 「信頼度」の画面・UI 上の別表記(SCR-032 等)。意味は信頼度と同一。正式には「信頼度」に統一する。 | [SCR-032](../02_basic_design/01_frontend/01_screens/SCR-032.md#SCR-032) |
| <span id="GLO-010"></span>Myプロジェクト | Myプロジェクト / 自分のプロジェクト | 自分が作成し自分がオーナーであるプロジェクト。表記に揺れあり(要件・UC は「Myプロジェクト」、画面・設計は「Myプロジェクト」)。正式には「Myプロジェクト」に統一する。 | [UC-014](04_business_usecases/UC-014.md#UC-014) / [SCR-004](../02_basic_design/01_frontend/01_screens/SCR-004.md#SCR-004) |
| <span id="GLO-011"></span>Joinプロジェクト | Joinプロジェクト | 招待されて参加している(自分がオーナーでない=メンバーである)プロジェクト。課金責任を負わない。表記に揺れあり(要件・UC は「Joinプロジェクト」、画面・設計は「Joinプロジェクト」)。正式には「Joinプロジェクト」に統一する。 | [UC-082](04_business_usecases/UC-082.md#UC-082) / [SCR-004](../02_basic_design/01_frontend/01_screens/SCR-004.md#SCR-004) |
| <span id="GLO-012"></span>状態語(サスペンション / 猶予 / 退会(済) / 論理削除 / 物理削除) | — | アカウント・プロジェクト等のライフサイクル状態と遷移は [状態モデル](../02_basic_design/08_state-model.md) を正本とする(本ページでは重複定義しない)。 | [状態モデル](../02_basic_design/08_state-model.md) |
| <span id="GLO-013"></span>課金語(無料枠 / 超過単価 / 月次上限 / 支払方法ゲート) | — | 課金の方式・設計値は [課金設計](../02_basic_design/05_billing-design.md) / [システム仕様書](../02_basic_design/07_system-spec.md) を正本とする(本ページでは重複定義しない)。 | [課金設計](../02_basic_design/05_billing-design.md) / [システム仕様書](../02_basic_design/07_system-spec.md) |
| <span id="GLO-014"></span>課金アカウント保有者 | 課金アカウント / 請求名義 / `M_BILLING_ACCOUNT`(DB) | プロジェクト横断の請求名義人。**ユーザー単位**で 1 つ存在し、本人が作成した全プロジェクトの利用量を集計して請求する(支払方法もユーザー単位 1 件)。プロジェクト単位の立場である「オーナー」[GLO-001](#GLO-001) とは別軸で、同一人物がプロジェクトごとに「オーナー」、ユーザー単位で「課金アカウント保有者」となる。「サスペンション(`suspended`)」は本概念=課金アカウントの状態であり、利用者アカウントの利用可否は別途 `M_USER` の状態に従う。 | [課金設計 §5](../02_basic_design/05_billing-design.md#5-課金アカウント状態ライフサイクル) / [TBL-002](../02_basic_design/02_backend/04_database/TBL-002.md#TBL-002) |
