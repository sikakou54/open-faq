# 各層テンプレート索引

> **本ディレクトリは FAQ 設計ポータルの各ドキュメント層の作成テンプレート(雛形)を保持します。**

運用ルールの正本は [../CLAUDE.md](../CLAUDE.md)。本ディレクトリは各層の作成テンプレート(雛形)を保持する。

新規ページを作成するときは、該当層のテンプレートを雛形にして、対応するフォルダに `<ID>.md`(要件仕様はカテゴリ別ファイル)を作成する。骨格・章立て・記載例・体裁は本テンプレートに従い、いつ・なぜ・何を守るか(運用方針・粒度・トレース・検証・採番・Issue)は [../CLAUDE.md](../CLAUDE.md) を参照する。

## 共通記載スタイル

全ページに共通する固定骨格・文章ルール・注記(GitHub Alert)・表の作法・コード/図の標準は [共通記載スタイル](00_common-style.md) を参照する(各層テンプレートはこのスタイルを前提とする)。

## テンプレート一覧

| # | テンプレート | 対象層 | 配置先フォルダ |
|----|----|----|----|
| 00 | [共通記載スタイル](00_common-style.md) | 全ページ共通 | — |
| 01 | [業務要件(BR)](01_business-requirement.md) | 業務要件 | `01_requirements/01_business_requirement/` |
| 02 | [機能要件(FR)](02_functional-requirement.md) | 機能要件 | `01_requirements/02_functional_requirement/` |
| 03 | [非機能要件(NFR)](03_non-functional-requirement.md) | 非機能要件 | `01_requirements/03_non_functional_requirement/` |
| 04 | [業務ルール(RULE)](04_business-rule.md) | 業務ルール | `01_requirements/01_business_requirement/08_rule.md` |
| 05 | [業務ユースケース(UC)](05_business-usecase.md) | 業務ユースケース | `01_requirements/04_business_usecases/` |
| 06 | [画面設計(SCR)](06_screen.md) | 画面設計 | `02_basic_design/01_frontend/01_screens/` |
| 08 | [システム設計(SYS)](08_system.md) | システム設計 | `02_basic_design/02_backend/01_system/` |
| 10 | [API設計(API)](10_api.md) | API設計 | `02_basic_design/02_backend/03_apis/` |
| 11 | [DB設計(TBL)](11_database.md) | DB設計 | `02_basic_design/02_backend/04_database/` |
| 12 | [シーケンス設計(SEQ)](12_sequence.md) | シーケンス設計 | `02_basic_design/03_sequences/` |
| 13 | [権限/エラー/メッセージ(PERM/ERR/MSG)](13_permission-error-message.md) | 権限・エラー・メッセージ | `02_basic_design/04_permissions/` ・ `05_errors/` ・ `06_messages/` |
| 14 | [将来対応(FUT)](14_future.md) | 将来対応 | `04_future/` |
| 15 | [状態遷移図(STS)](15_state-transition.md) | 詳細設計 | `03_detail_design/01_state_transitions/` |
| 16 | [画面遷移図(STR)](16_screen-flow.md) | 詳細設計 | `03_detail_design/02_screen_flows/` |
| 17 | [入出力設計書(IO)](17_io-spec.md) | 詳細設計 | `03_detail_design/03_io_specs/` |
| 18 | [IPO処理機能記述書(IPO)](18_ipo.md) | 詳細設計 | `03_detail_design/04_ipo/` |
| 19 | [バッチ処理設計書(BAT)](19_batch.md) | 詳細設計 | `03_detail_design/05_batch/` |
| 20 | [外部インターフェース設計図(EIF)](20_external-if.md) | 詳細設計 | `03_detail_design/06_external_if/` |
| 21 | [データベース物理設計書(DBP)](21_db-physical.md) | 詳細設計 | `03_detail_design/07_db_physical/` |
| 22 | [詳細シーケンス図(DSQ)](22_sequence-detail.md) | 詳細設計 | `03_detail_design/08_sequences/` |
| 23 | [アクティビティ図(ACT)](23_activity.md) | 詳細設計 | `03_detail_design/09_activities/` |
| 24 | [クラス図(CLS)](24_class.md) | 詳細設計 | `03_detail_design/10_class/` |
| 25 | [モジュール構造図(MOD)](25_module.md) | 詳細設計 | `03_detail_design/11_module/` |

## 要件仕様(BR / FR / NFR / RULE)の配置・カテゴリ共通説明

要件仕様(01〜04)は次の方針で配置する。BR / FR / NFR / RULE を**種別フォルダ + カテゴリ別・種別別ファイルへ統合**する。種別ごとに 3 フォルダへ分割し、各フォルダは自身の `index.md` で一覧する。**業務要件(BR)はカテゴリ別ファイル内の HTML テーブル(1 行 = 1 要件)で一覧化**し、FR / NFR / RULE は各要件を節として保持する。業務要件(BR)と機能要件(FR)は**カテゴリごとに別ファイル**(`-br` / `-fr`)へ分離する。

フォルダ・ファイル構成:

| フォルダ | ファイル | 内容 |
|----|----|----|
| `01_business_requirement/` | `01_account-br.md` 〜 `06_security-br.md`(6) | 業務要件 BR(カテゴリ別 HTML テーブル) |
| `01_business_requirement/` | `08_rule.md` | 業務ルール RULE(`## <分類>` ではなく RULE 節) |
| `02_functional_requirement/` | `01_account-fr.md` 〜 `06_security-fr.md`(6) | 機能要件 FR(カテゴリ別・節) |
| `03_non_functional_requirement/` | `07_nfr.md` | 非機能要件 NFR(`## <分類>` 節別) |

カテゴリは 6 種(`01_account` アカウント・ユーザー・アクセス制御 / `02_faq-ai` FAQ・AI 回答・未解決質問・処理エラー / `03_usage` 利用量・課金・ダッシュボード・運用 / `04_widget` ウィジェット・検索・入出力 / `05_notification` 通知・お知らせ / `06_security` セキュリティ・プライバシー)。

- ファイル先頭はカテゴリ + 種別の `# 見出し` + 要約 + メタ。カテゴリ↔種別↔要件の対応は各種別フォルダの `index.md`。BR/FR ファイルは単一種別なので種別節は持たない。**BR ファイルは要件を HTML テーブルで直接並べ**、FR ファイルは要件節を直接並べる。
- 各要件節の骨格(FR / NFR / RULE): `## <span id="ID"></span>ID: 名称` → 要約 → メタ → `### 要件`(RULE は `### ルール`)→ **`### シーケンス`(FR のみ)**。**リード文は置かない。** ID アンカーは要件見出しに付け、節見出し(要件 / シーケンス / ルール 等)には付けない(ファイル内で重複するため)。
- **要件は後工程へのリンク・参照を持たない / BR・FR は `### 関連` セクションを持たない**(書式上の指示)。詳細な粒度・逆参照のルールは [../CLAUDE.md](../CLAUDE.md) の粒度分離ルール・トレーサビリティ規約を参照する。
