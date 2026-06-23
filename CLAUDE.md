# FAQ 設計ポータル 保守ルール

本書(CLAUDE.md)はリポジトリの**保守・運用ルールの正本**であり、エージェントが自動読込する指示ファイルである。各ドキュメント層の**作成テンプレート(骨格・記載例)・記載スタイル標準**は [`templates/`](templates/README.md) 配下へ分離した(本書はテンプレート本文を持たない)。

本リポジトリは「FAQ AI ウィジェット SaaS / メインシステム」の **要件定義書**・**基本設計書** を **Markdown** で管理する。1 つの識別子(要件 / UC / 画面 / API / テーブル …)= 1 ファイルの**個別ページ構成**を正本とし、ルートの [`README.md`](README.md) が入口(各セクション `index.md` への手書きトップページ)である。各識別子はフラット連番でゼロ詰め 3 桁・欠番なし。

> [!IMPORTANT]
> **読み順(正本)** 要件定義 ＞ 業務ユースケース ＞ 画面設計 ＞ システム設計 ＞ API設計 ＞ DB設計 ＞ シーケンス ＞ 権限 / エラー / メッセージ。各層は前層を実現する関係で、`要件 ↔ UC ↔ (SCR / SYS) ↔ API ↔ TBL` を双方向にトレースする。画面起点の業務UCは画面層(SCR)、システム起点(バッチ/Webhook/非同期/監視/通知)の業務UCはシステム層(SYS)で実現する。

---

## 構成

ファイル名はすべて英名(ASCII / ID ベース)。ページの表示タイトル・見出しは日本語。トップは 3 グループ(`01_requirements` / `02_basic_design` / `03_future`)。各セクションはフォルダ(`index.md` + 配下の個別ページ)で構成する。

```text
README.md                          # トップページ(手書き・最小。各セクション index への入口)
CLAUDE.md                          # 保守ルール正本(本書)
templates/                         # 各層の作成テンプレート(雛形)。CLAUDE.md から分離
01_requirements/                   # 要件定義
├── index.md                       #   システム概要 / 背景・目的 / スコープ / 利用者・ロール / 制約・前提 / 各要件フォルダ・業務UCへのポインタ
├── 01_business_requirement/        #   業務要件 : index.md + BR(01_account 〜 06_security の -br、カテゴリ別 HTML テーブル)+ 業務ルール RULE(08_rule.md)
├── 02_functional_requirement/      #   機能要件 : index.md + FR(01_account 〜 06_security の -fr、各 ID は節で保持)
├── 03_non_functional_requirement/   #   非機能要件 : index.md + 07_nfr.md(分類節・通し連番)
└── 04_business_usecases/          #   業務ユースケース : index.md + UC-001..(業務処理粒度。画面起点→システム起点→要件起点。本文は BR/FR/RULE のみ)
02_basic_design/                   # 基本設計(frontend / backend グルーピング)
├── index.md                       #   基本設計トップ
├── 01_frontend/                   #   フロントエンド設計(利用者操作の画面まわり)
│   ├── index.md
│   └── 01_screens/                #     画面設計 : index.md + SCR-001..(§6 にイベント列(EVT-ID を非リンクアンカーで保持)、§1 に対応UC)
│       └── mocks/                 #       画面モック: 画像 *.png と HTML ソース *.html(同名ペア)
├── 02_backend/                    #   バックエンド設計(サーバー側)
│   ├── index.md
│   ├── 01_system/                 #     システム設計 : index.md + SYS-001..(無人処理。§6 にイベント列(SEV-ID を非リンクアンカーで保持)、§1 に対応UC)
│   ├── 03_apis/                   #     API設計 : index.md + API-001..(1 エンドポイント = 1 ファイル)
│   └── 04_database/               #     DB設計 : index.md + TBL-001..(1 テーブル = 1 ファイル)
├── 03_sequences/                  #   シーケンス設計 : index.md + SEQ-001..(対応UC、図中の画面は SCR-ID)
├── 04_permissions/                #   権限設計 : index.md + PERM-001..
├── 05_errors/                     #   エラー設計 : index.md + ERR-001..
├── 06_messages/                   #   メッセージ設計 : index.md + MSG-001..(メールテンプレ)
└── 05_billing-design.md           #   横断設計(課金。単独ファイルで存置)
03_future/                         # 将来対応 : index.md + FUT-01..(カテゴリ別。FUT-06 は -req / -detail の親子)
_build/                            # ツール(配信対象外)
```

- ファイル名は原則 ID 1 件 = 1 ファイル(例 `UC-001.md` / `SCR-001.md` / `API-001.md` / `TBL-001.md` / `SEQ-001.md` / `PERM-001.md` / `ERR-001.md` / `MSG-001.md`)。**ただし要件仕様(BR/FR/NFR/RULE)はファイル数削減のためカテゴリ別・種別別ファイルへ統合**し、各 ID は当該ファイル内で保持する(種別ごとに `01_business_requirement/`(BR + RULE)/ `02_functional_requirement/`(FR)/ `03_non_functional_requirement/`(NFR)へ分割。ID・アンカー・採番は不変)。**BR は HTML テーブルの行(ID セルに `<span id="ID"></span>`)**、FR / NFR / RULE は節 `## <span id="ID"></span>ID: 名称` で保持する。
- ページ間リンクはすべて `.md`。同一フォルダ内は兄弟参照、フォルダ / グループをまたぐ参照は相対パス(下記「相互参照アンカー」)。

### 採番ルール(最重要)

各系列は**フラット連番・ゼロ詰め 3 桁・欠番なし**。番号はその系列の**文書出現順**(定義の `<span id>` 出現順)に `001` から採番する。

| 系列 | 接頭辞 | 範囲(現状) | 備考 |
|----|----|----|----|
| 業務要件 | `BR-` | `BR-001`〜 | `01_business_requirement/` のカテゴリ別 HTML テーブルに統合(行で保持) |
| 機能要件 | `FR-` | `FR-001`〜 | `02_functional_requirement/` のカテゴリ別ファイルへ統合(節で保持) |
| 非機能要件 | `NFR-` | `NFR-001`〜 | 分類別ではなく通し連番。`03_non_functional_requirement/07_nfr.md` に分類節で統合 |
| 業務ルール | `RULE-` | `RULE-001`〜 | FR / BR から抽出した定量しきい値・ポリシー(`01_business_requirement/08_rule.md` に統合) |
| 業務ユースケース | `UC-` | `UC-001`〜 | 業務処理粒度(誰が〜する)。画面起点 → システム起点 → 要件起点の順 |
| 画面 | `SCR-` | `SCR-001`〜 | 1 画面 = 1 ファイル(フラット。`-NNN` 従属は廃止)。`01_frontend/01_screens/` |
| 画面イベント | `EVT-` | `EVT-001`〜 | 画面設計 SCR §6 のイベント一覧に `<span id>` アンカー(非リンク)として保持(独立ファイル・フォルダは廃止)。API / エラー ERR / 権限 PERM / シーケンス SEQ がプレーン ID で参照 |
| システム | `SYS-` | `SYS-001`〜 | 1 システム処理 = 1 ファイル(バッチ/Webhook/非同期/監視/通知の無人処理。画面 `SCR` の backend 版)。`02_backend/01_system/` |
| システムイベント | `SEV-` | `SEV-001`〜 | システム設計 SYS §6 のイベント一覧に `<span id>` アンカー(非リンク)として保持(独立ファイル・フォルダは廃止)。将来のシステム起点シーケンスが参照 |
| API | `API-` | `API-001`〜 | 1 エンドポイント = 1 ファイル。`02_backend/03_apis/` |
| テーブル | `TBL-` | `TBL-001`〜 | 分類接頭辞(`M_`/`T_`/`H_`/`TP_`)は物理名に残し ID は通し連番 |
| シーケンス | `SEQ-` | `SEQ-001`〜 | UC 単位 |
| 権限 | `PERM-` | `PERM-001`〜 | |
| エラー | `ERR-` | `ERR-001`〜 | API エラーコードを正規化・採番 |
| メッセージ | `MSG-` | `MSG-001`〜 | メールテンプレ |
| 将来対応 | `FUT-` | `FUT-01`〜 | MVP 後バックログ。カテゴリ別・2 桁連番(3 桁フラット連番の唯一の例外)。`FUT-06` は `-req` / `-detail` の親子 |

> [!WARNING]
> **欠番を作らない。** 識別子を削除したら後続を詰めて再採番し、**全層の参照を 1 パスで一括張替**する(例 `(?<![A-Za-z0-9])FR-\d+(?![0-9])` を旧→新マッピングで置換)→ 壊れリンク・壊れアンカーが無い(**0 / 0**)ことを確認する。

> [!NOTE]
> **ページ内局所IDは本表の対象外。** `IT-`(画面項目)/ `EV-`(画面イベント)/ `PR-`(処理ステップ)/ `SE-`(システムイベント)等は各ページ内でのみ一意な局所識別子で、全系列フラット採番(ゼロ詰め 3 桁・欠番なし)の対象ではない。これに対し `EVT-` / `SEV-` は広域IDで、画面設計 SCR §6 / システム設計 SYS §6 のイベント一覧に `<span id>` アンカーとして保持する(両者は別物)。

---

## ドキュメントの粒度分離ルール

各ドキュメント層は役割と記載粒度が異なる。**上位から下位へ、次の順で粒度を分離し、層の役割を混在させない。**

```text
業務要件 → 機能要件・非機能要件 → 業務ユースケース → 基本設計
```

| 層 | 書くこと(役割) |
|----|----|
| 業務要件(BR) | 業務上実現したいこと(誰が・何のために・何を可能にするか)を記載する |
| 機能要件(FR) | システムが提供する機能を記載する |
| 非機能要件(NFR) | 性能・セキュリティ・可用性・運用性などの品質要件を記載する |
| 業務ユースケース(UC) | 業務目的を達成するための利用者・システムの流れを記載する |
| 基本設計(SCR/SYS/API/TBL/SEQ ほか) | 要件をシステムとしてどう実現するかを記載する |

- **過剰な実装詳細を上位層へ書かない。** 業務要件・業務ユースケースに、画面ID・画面イベントID・API ID・テーブル名・物理名・カラム名・SQL・クラス / 関数 / メソッド名・実装詳細などを書かない。これらは業務語へ言い換えるか、対応する下位層へ委ねる。

> [!IMPORTANT]
> **UC 本文には基本設計レベルの情報を書かない。** 画面ID(`SCR`)/ 画面イベントID(`EVT`)/ API ID(`API`)/ テーブルID(`TBL`)/ シーケンスID(`SEQ`)/ エラーID(`ERR`)/ メッセージID(`MSG`)、画面名・ボタン名・フォーム名・入力項目名、API名 / エンドポイント / メソッド / ステータスコード、テーブル名・物理名・カラム名・SQL、クラス / 関数 / メソッド名、mermaid 図は記載しない。これらは業務語へ言い換えて除去する。

- **BR と FR で重複を作らない。** BR=業務意図(誰が・何のために・何を可能にするか + 業務上の制約 / リスク / 方針の質的言明)を 1〜2 文で。FR=システム機能の細粒度。**数値しきい値・手順番号・対象操作の列挙・状態名・画面 / UI 文言・FR とほぼ同文の機能記述は BR に書かず**、対応 FR(数値は業務ルール RULE)へ委ねる。FR に無い業務理由・価値・ステークホルダ別役割・固有方針は BR に残す。FR から BR の業務観点を再掲しない。

> [!WARNING]
> **逆参照(下位 → 上位を正本扱いする参照)を作らない。** 要件(BR / FR / NFR / RULE)は後工程(業務UC・基本設計)へのリンク・「…を正本とする」等の委譲文を持たない。参照は**下流 → 上流の一方向のみ**(UC → 要件、基本設計 → UC など)。要件 → 下流のトレースは下流側の逆引き(UC の `対応要件ID`、各設計の `対応業務UC`、SCR / PERM の由来要件など)で辿る。

---

## 上位設計変更時の影響調査ルール

上位ドキュメントを変更したら、**必ず下位ドキュメントへの影響調査を行う**。粒度分離(上記)に沿って、変更が下流へ波及していないかを毎回確認する。

| 変更した層 | 影響調査の対象 |
|----|----|
| 業務要件(BR) | 機能要件 / 非機能要件 / 業務ユースケース / 基本設計への影響を確認する |
| 機能要件(FR) | 業務ユースケース / 基本設計への影響を確認する |
| 非機能要件(NFR) | 基本設計 / 運用設計への影響を確認する |
| 業務ユースケース(UC) | 基本設計への影響を確認する |

- 影響がある場合は、関連する下位ドキュメントを更新する。
- 影響が無い場合でも、**「影響調査を実施した」ことを作業ログ(Issue コメントや作業報告)に残す**。調査自体を省略しない。

---

## ナビゲーションと索引

ナビゲーションは次の手動保守で行う。

- **トップページ** = ルート [`README.md`](README.md)(手書き・最小)。各セクションの `index.md` への入口。
- **各セクションの一覧** = 各フォルダの `index.md`(要件仕様 / 業務UC / 画面 / システム / API / テーブル / シーケンス / 権限 / エラー / メッセージ の一覧を兼ねる)。一覧・索引は手動で保守する。
- ページ間の移動は各 `index.md` と相互参照リンク(下記)で辿る。右 TOC(「このページ」)はビューア(GitHub 等)が見出しから自動生成するため埋め込まない。

### 相互参照アンカー(最重要)

リンクは「定義側にアンカー、参照側に Markdown リンク」の 2 点で結線する。

- **定義側**: アンカーに `<span id="ID"></span>` を埋める(見出し `# <span id="FR-001"></span>FR-001: …`、表は対象セルの先頭に `<span id="TBL-001"></span>`)。**新しい定義行・見出しを追加したら必ず付ける。**
- **参照側**: 通常の Markdown リンク `[ID](相対パス.md#ID)` で送る。リンク先は常に `.md#<ID>`。`../` の数は参照元ファイルのリポジトリ root からの深さで決まる(例: `02_basic_design/01_frontend/01_screens/` は深さ 3、`02_basic_design/03_sequences/` は深さ 2)。
- **要件仕様の特例**: ファイル名は ID ではなく「カテゴリ + 種別」(例 `02_faq-ai-fr.md`)、アンカーは `#<ID>`。各系列の一覧は所属フォルダの `index.md`。
- **イベント ID の特例**: 画面イベント `EVT-xxx` / システムイベント `SEV-xxx` は独立ページを持たず、画面設計 SCR §6 / システム設計 SYS §6 のイベント一覧に **非リンクのアンカー** `<span id="EVT-001"></span>EVT-001` として定義する。これを参照する側(API 設計・エラー ERR・権限 PERM・シーケンス SEQ・将来のシステム起点シーケンス等)は、リンクではなく **プレーンテキストの広域 ID**(例 `EVT-001`)で記す。

相対パスの早見表(参照元 → 参照先):

| 参照元 → 参照先 | 相対パス例 |
|----|----|
| 同一ページ | `[FR-001](#FR-001)` |
| 要件仕様 同種別フォルダ内 | `[FR-007](02_faq-ai-fr.md#FR-007)` / `[BR-001](01_account-br.md#BR-001)` |
| 要件仕様 種別跨ぎ・業務UC → 要件(`01_requirements` 内) | `[FR-001](../02_functional_requirement/01_account-fr.md#FR-001)` / `[RULE-001](../01_business_requirement/08_rule.md#RULE-001)` |
| 同一フォルダの別ページ(SCR / SYS など) | `[SCR-002](SCR-002.md#SCR-002)` / `[SYS-002](SYS-002.md#SYS-002)` |
| 基本設計 同グルーピング内(兄弟フォルダ) | API → テーブル `[TBL-001](../04_database/TBL-001.md#TBL-001)` / システム → API `[API-060](../03_apis/API-060.md#API-060)` |
| 基本設計 グルーピング跨ぎ | シーケンス → API `[API-002](../02_backend/03_apis/API-002.md#API-002)` / 画面 → API `[API-061](../../02_backend/03_apis/API-061.md#API-061)` / システム → エラー `[ERR-001](../../05_errors/ERR-001.md#ERR-001)` |
| グループ跨ぎ(基本設計 → 要件 / 業務UC) | 画面 → 業務UC `[UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001)`(深さ 3)/ システム → 業務UC `[UC-061](../../../01_requirements/04_business_usecases/UC-061.md#UC-061)`(深さ 3)/ シーケンス → 業務UC `[UC-001](../../01_requirements/04_business_usecases/UC-001.md#UC-001)`(深さ 2) |

### ページの編集・追加

Markdown が正本なので、**該当 `.md` の本文を直接編集する**。ページを追加したら当該フォルダに `<ID>.md` を作成し、当該フォルダの `index.md`(必要に応じて [`README.md`](README.md))の一覧へ手で追記する。新規ページは [`templates/`](templates/README.md) の該当テンプレートを雛形にする(下記「テンプレート(各層の雛形)」)。編集後は壊れリンク・アンカーが無い(0 / 0)ことを確認する。

---

## ページ形式

各ページは**自己完結 Markdown**(本文のみ)。

- 外部依存なし。図は ` ```mermaid ` コードフェンスで記述し、対応ビューア(GitHub 等)でそのまま描画される。
- **絵文字は使わない。**
- 画面モック(ワイヤーフレーム)は **PNG 画像で表示**する(下記「画面モックの画像化」)。
- 各ページの固定骨格・本文の書き方(タイトル / 要約 / メタ / 本編)・文章ルール・注記(GitHub Alert)・表の作法・コード / 図の体裁は [`templates/00_common-style.md`](templates/00_common-style.md)(共通記載スタイル)を正本とする。

## 画面モックの画像化

GitHub は埋め込み HTML の `style=`/`class=` を除去するため、画面モック(`02_basic_design/01_frontend/01_screens/SCR-*.md` の §3 画面レイアウト)は **PNG 画像で表示**する。HTML ソースは MD に埋め込まず、**`02_basic_design/01_frontend/01_screens/mocks/<画面>-<n>.html`** に外出しして保持する(MD は画像 1 行のみ)。画像も同じ `02_basic_design/01_frontend/01_screens/mocks/<画面>-<n>.png` に置き、各 SCR からは `mocks/<画面>-<n>.png`(子階層相対・`../` なし)で参照する。**`../` 親参照にすると Cursor / VS Code のプレビューが画像を読み込めない**ため、必ず各ページと同階層配下に置く。

`mocks/<画面>-<n>.html` は単体で開けて図と同じ見た目になる完結 HTML(クロップ用に `#wrap` を持つ)。**モックを変更するときはこの .html を直接編集**し、PNG を再生成する(ルートで):

```sh
node ~/.claude/skills/html-to-png/scripts/html_to_png.js 02_basic_design/01_frontend/01_screens/mocks --selector "#wrap"
```

`mocks/*.html` → 同名 `mocks/*.png` を一括レンダリングする(html-to-png グローバルスキル / `puppeteer-core` + ローカル Chromium)。`mermaid` は画像化せず ` ```mermaid ` のまま(GitHub が描画)。

---

## テンプレート(各層の雛形)

各ドキュメント層の骨格・章立て・記載例・体裁指示は [`templates/`](templates/README.md) 配下に分離した。**新規ページを作成するときは、該当テンプレートを雛形にして本文を起こす。** テンプレートは記載スタイル標準(共通)+ 各層テンプレート(要件仕様 / 業務UC / 画面 / システム / API / DB / シーケンス / 権限・エラー・メッセージ / 将来対応)で構成する。

| テンプレート | 対象 |
|----|----|
| [templates/README.md](templates/README.md) | テンプレート索引 |
| [templates/00_common-style.md](templates/00_common-style.md) | 共通記載スタイル(タイトル / 要約 / メタ / 文章ルール / 注記 / 表 / コード・図) |
| [templates/01_business-requirement.md](templates/01_business-requirement.md) | 業務要件 `BR` |
| [templates/02_functional-requirement.md](templates/02_functional-requirement.md) | 機能要件 `FR` |
| [templates/03_non-functional-requirement.md](templates/03_non-functional-requirement.md) | 非機能要件 `NFR` |
| [templates/04_business-rule.md](templates/04_business-rule.md) | 業務ルール `RULE` |
| [templates/05_business-usecase.md](templates/05_business-usecase.md) | 業務ユースケース `UC` |
| [templates/06_screen.md](templates/06_screen.md) | 画面設計 `SCR` |
| [templates/08_system.md](templates/08_system.md) | システム設計 `SYS` |
| [templates/10_api.md](templates/10_api.md) | API設計 `API` |
| [templates/11_database.md](templates/11_database.md) | DB設計 `TBL` |
| [templates/12_sequence.md](templates/12_sequence.md) | シーケンス設計 `SEQ` |
| [templates/13_permission-error-message.md](templates/13_permission-error-message.md) | 権限 / エラー / メッセージ `PERM` / `ERR` / `MSG` |
| [templates/14_future.md](templates/14_future.md) | 将来対応 `FUT` |

---

## レビュー方針(NotebookLM レビュー活用)

ドキュメントのレビューは **NotebookLM を活用する**。NotebookLM はレビューの判定者(外部レビュアー)である。

> [!IMPORTANT]
> **NotebookLM を使うときは必ずスキル(`design-doc-review` / `notebooklm-review`)経由でレビューする。** スキルを介さず直接操作しない(`design-doc-review` が全層フルレビューのオーケストレーション、`notebooklm-review` が `nlm` CLI の基本操作を担う)。

レビュー観点(最低限):

- 設計書の構成・記載粒度が適切か。
- 要件定義・基本設計に抜け漏れがないか。
- ドキュメント間の整合性が取れているか。
- 業務要件・機能要件・非機能要件・業務UC・基本設計の粒度が混在していないか。
- 上位ドキュメントの変更が下位に反映されているか。
- 要件定義が基本設計を参照する逆参照になっていないか。

> [!WARNING]
> **レビュー指摘があれば修正し、再度 NotebookLM でレビューする。指摘が無くなるまでレビューと修正を繰り返す。** 1 回のレビューで打ち切らない。

---

## Agent 実行ルール

> [!IMPORTANT]
> **タスクは一人の Agent だけで完結させない。「統括Agent + 作業Agent」の構成で実行する。** 必要に応じて レビューAgent / 調査Agent / 影響調査Agent / Issue管理Agent を追加する。

| 役割 | 担当 |
|----|----|
| 統括Agent | 作業全体の方針決定・作業分解・進捗管理・成果物統合・レビュー依頼・最終確認 |
| 作業Agent | 統括Agentから割り当てられた範囲の調査・編集・修正・報告 |
| レビューAgent / 調査Agent / 影響調査Agent / Issue管理Agent | 必要に応じて追加し、レビュー・調査・影響調査・課題管理を分担する |

---

## 課題管理(GitHub Issue 運用)

作業中に発生した課題は GitHub Issue に登録し、解決したらクローズする。**記録を残さないまま放置しない。**

### 登録

課題が発生したら GitHub に Issue を登録する。**登録すべきケース:**

- 要件が不足している。
- 仕様の解釈が複数あり得る。
- ドキュメント間で矛盾がある。
- 影響範囲が広い。
- 関係者の判断が必要である。
- その場ですぐに解決できない。
- 後続作業に影響する。

`gh issue create` で起票する。表題に区分(`traceability` / `design-gap` / `needs-review` 等)を付ける。

### Issue 本文の記載ルール

> [!IMPORTANT]
> **Issue 本文は中学生にも理解できる表現にする。** 専門用語を使う場合は簡単な説明を添える。**必ず提案を添える。**

本文は最低限、次の見出し構成で書く:

| 見出し | 書くこと |
|----|----|
| `# 概要` | 何が問題か |
| `# 背景` | なぜ発生したか |
| `# 影響` | 放置すると何に困るか |
| `# 提案` | どう対応するのがよいか |
| `# 確認したいこと` | 関係者に判断してほしいこと |
| `# 関連ドキュメント` | 関係するファイル名・パス |

### クローズ

課題を解決したら**必ず該当 Issue を Close する**。Close は解決コミット本文に `Closes #<番号>` を入れるか `gh issue close <番号>` で行う。

> [!WARNING]
> **Close する前に次を確認する。** いずれかが満たせない場合は Close しない。
> - 課題が解決している。
> - 関連ドキュメントが更新されている。
> - 必要な影響調査(上記「上位設計変更時の影響調査ルール」)が完了している。
> - NotebookLM レビューで問題が残っていない。
> - 対応内容が Issue にコメントされている。

---

## 注意

- Markdown が正本。本文変更は該当 `.md` の本文を直接編集する。README・各 `index.md`(一覧)は手動保守する。
- **各層の作成テンプレート・記載スタイル標準は [`templates/`](templates/README.md) へ分離した。** 新規ページ作成・体裁確認は templates/ の該当ファイルを参照する(本書はテンプレート本文を持たない)。
- 定義行・見出しを追加したら `<span id="…"></span>` を必ず付ける。削除・改名した識別子は、`01_requirements` / `02_basic_design`(配下フォルダ含む)/ `03_future` を検索して取りこぼしを修正する。
- 運用ルールの更新は本書 `CLAUDE.md` を直接編集する。
