---
name: engineering-document-readability-review
description: 要件定義書・基本設計書を「実装するシステムエンジニアの立場」で読み、仕様判断・設計・実装に進める状態かを検査する可読性レビュー。理解できない/読み止まる/仕様判断に迷う箇所だけを8列一覧表で洗い出す。NotebookLM(外部SEレビュア)で5観点を走査し、全指摘を grep で検証してから採用する。誤字脱字や表現の好みは扱わない。「可読性レビュー」「エンジニア観点レビュー」「読み止まりレビュー」「実装着手できるか確認」と言われたら使う。全層フルレビュー(取り違え/整合性/逆参照/欠番)とは目的が異なる(あちらは full-layer-review)。
---

# エンジニア可読性レビュー(SE実装着手観点)

要件定義書・基本設計書を、**実際にこのシステムを設計・実装する立場のSE**として読む。目的は文章の体裁を整えることではなく、**エンジニアが仕様を正しく理解し後続の設計・実装・レビューに進める状態か**を確認すること。アウトプットは「読み止まる箇所」の8列一覧表。

設計判断は **NotebookLM(外部SEレビュア)** に委ね、**事実(ID・記述の実在)は grep で検証**する。NotebookLM の指摘は採用前に必ず grep で裏取りする(このリポジトリの HTML/パイプ表を NotebookLM は誤読する)。

> スコープ: 差分ではなくコーパス全体。誤字脱字・表現の好み・自明な体裁は指摘しない。**実装・設計・仕様判断に影響する読み止まりだけ**を出す。
> full-layer-review との違い: あちらは品質(取り違え/整合性/逆参照/粒度/欠番)の正本レビュー。本スキルは「SEが実装に進めるか」という**理解可能性**に絞る。スクリプト基盤(bundle/ask)は full-layer-review のものを再利用する。

```bash
SK=.claude/skills/full-layer-review/scripts          # nlm_bundle.py / nlm_ask.py を再利用
P=.claude/skills/engineering-document-readability-review/prompts
```

## レビュー観点(6つ)

1. **仕様理解のしやすさ** — 要件が曖昧で具体的な仕様判断に落とせないか / 抽象表現のまま設計に展開できないか。
2. **ドキュメント間のつながり** — 業務要件→FR→UC→基本設計の落とし込みが追えるか / 矛盾・未反映・逆参照はないか。
3. **設計根拠の明確さ** — その画面・API・テーブル・権限・エラーが「なぜ必要か」(由来する業務目的)が読めるか。
4. **用語・概念の一貫性** — ロール/権限/ステータス/プラン/プロジェクト/契約・課金等が一貫しているか(同語異義・異語同義)。
5. **条件・分岐・例外の明確さ** — 前提/例外/分岐/制約と、異常系・境界・権限不足時の扱いが読めるか。
6. **実装時の確認質問リスク** — 仕様判断が実装者任せ(未決定/TBD/「適宜」)になっていないか。

## § 0. 前提(初回のみ)

```bash
export PATH="$HOME/.local/bin:$PATH"
nlm --version && nlm doctor          # Cookies present + Account を確認。expired なら nlm login
```

## § 1. コーパスをバンドル(レイヤー別)

full-layer-review の `nlm_bundle.py` をそのまま使う(11レイヤー)。`===== <path> =====` セパレータで出典を保持する。

```bash
python3 $SK/nlm_bundle.py --root . --out _nlm/bundles \
  --bundle rules='CLAUDE.md' \
  --bundle requirements='01_requirements/index.md,01_requirements/01_business_requirement/**/*.md,01_requirements/02_functional_requirement/**/*.md,01_requirements/03_non_functional_requirement/**/*.md' \
  --bundle usecases='01_requirements/04_business_usecases/**/*.md' \
  --bundle traceability='02_basic_design/00_traceability/**/*.md' \
  --bundle screens='02_basic_design/01_frontend/01_screens/*.md' \
  --bundle system='02_basic_design/02_backend/01_system/**/*.md' \
  --bundle apis='02_basic_design/02_backend/03_apis/**/*.md' \
  --bundle database='02_basic_design/02_backend/04_database/**/*.md' \
  --bundle sequences='02_basic_design/03_sequences/**/*.md' \
  --bundle crosscut='02_basic_design/index.md,02_basic_design/05_billing-design.md,02_basic_design/04_permissions/**/*.md,02_basic_design/05_errors/**/*.md,02_basic_design/06_messages/**/*.md' \
  --bundle detail='03_detail_design/**/*.md' \
  --bundle future='04_future/**/*.md'
```

## § 2. 専用ノートブックを作成しソースを追加

```bash
NB=$(nlm create notebook "FAQ 可読性レビュー(SE観点) $(date +%F)" | grep -oE '[a-f0-9-]{36}' | head -1)
echo "$NB" > _nlm/readability_nb_id.txt
rm -f _nlm/readability_source_ids.json
for f in rules requirements usecases traceability screens system apis database sequences crosscut future; do
  out=$(nlm source add "$NB" --file "_nlm/bundles/$f.md" --wait)
  sid=$(echo "$out" | grep -oiE '[a-f0-9-]{36}' | head -1)
  python3 -c "import json,os;p='_nlm/readability_source_ids.json';m=json.load(open(p)) if os.path.exists(p) else {};m['$f']='$sid';json.dump(m,open(p,'w'),ensure_ascii=False,indent=2)"
done
```

## § 3. 5本の可読性クエリを実行(観点ごとにスコープを絞る)

メガプロンプト1本より、焦点を絞った複数クエリの方が網羅性が上がり hallucination が減る。プロンプトは `prompts/` 配下。全プロンプトが「提供ソースのみ・相対パス+実在ID根拠・推測禁止・指摘なければ『指摘なし』・8列表で出力」を内蔵する。

```bash
NB=$(cat _nlm/readability_nb_id.txt); IDS=_nlm/readability_source_ids.json
ask(){ python3 $SK/nlm_ask.py --notebook "$NB" --ids-map $IDS --prompt-file "$P/$1" --sources "$2" --out "_nlm/readability/$3"; }

ask r1_requirements_clarity.md requirements,usecases                                   r1   # 観点1,5: 要件の曖昧さ・例外不足
ask r2_layer_linkage.md        requirements,usecases,traceability,screens,apis,system  r2   # 観点2,3: 落とし込み・逆参照・設計根拠
ask r3_screens_apis.md         screens,apis                                            r3   # 観点5,6: 画面挙動・API異常系・未決定
ask r4_data_perm_err.md        database,crosscut                                       r4   # 観点3,4,5: データ保持・権限境界・エラー挙動
ask r5_terminology.md          requirements,usecases,screens,apis,database,crosscut,system r5  # 観点4: 用語・概念の一貫性
```

出力は `_nlm/readability/<r>_answer.md`(回答+引用根拠)。

| クエリ | プロンプト | スコープ | 主な観点 |
|----|----|----|----|
| r1 | `r1_requirements_clarity.md` | requirements,usecases | 1 仕様理解 / 5 条件・例外 |
| r2 | `r2_layer_linkage.md` | requirements,usecases,traceability,screens,apis,system | 2 つながり / 3 設計根拠・逆参照 |
| r3 | `r3_screens_apis.md` | screens,apis | 5 分岐・例外 / 6 確認質問リスク |
| r4 | `r4_data_perm_err.md` | database,crosscut | 3 設計根拠 / 4 用語 / 5 例外 |
| r5 | `r5_terminology.md` | (全層横断) | 4 用語・概念の一貫性 |

## § 4. 全指摘を grep で検証してから採用(最重要)

NotebookLM の指摘を**そのまま信じない**。各指摘につき:引用 ID・記述が実在するか grep し、主張のスコープを正本で確認して **確定 / 偽陽性 / 設計判断** に分類する。

```bash
grep -rn "<ID や引用語>" 01_requirements 02_basic_design        # 実在確認
```

このリポジトリで繰り返す**偽陽性パターン**(採用しない):
- **HTML/パイプ表が「空」「欠落」** — テーブル誤読。実際は入力済み(`grep -A6 '## 利用テーブル'` 等で確認)。
- **廃止概念が「残存」** — 例「契約(テナント)が本文に残存」→ 実際は利用契約/契約義務(法的語)や更新履歴のみで、現役要件には無い。両方の出現箇所を grep して片方しか無ければ偽陽性。
- **存在しない ID・履歴** — 例「NFR-905」「v2.2 で廃止」等。`grep -rn` で実在確認。
- **要件が定めない不足の指摘** — 要件のスコープ外を「欠落」と言う。追加は要件捏造。要件の実スコープを確認。

**基本設計の適切な委譲を「未定義」と誤指摘しない** — 例 `row_hash` 正規化対象が「詳細設計で確定」と明記済みなら、それは粒度として妥当(優先度低・対応不要)。CLAUDE.md の粒度分離(物理実装は詳細設計へ)に照らす。

**NotebookLM が得意で活用すべき領域**(検証しつつ採用): 画面↔API のバリデーション/必須・任意の不一致、要件↔下位設計のしきい値不整合、UIラベルの要件混入(粒度)、用語ぶれ(同語異義・異語同義)、列挙値(reason等)の網羅漏れ、状態/保持期間の取り違え。検証中に**新たな読み止まり**(重複API・命名重複等)を見つけたら追加する。

指摘を黙って捨てない・検証せず適用しない。確定/偽陽性/設計判断と理由を必ず記録する。

## § 5. 成果物 — 8列一覧表

確定指摘を統合(重複はマージ・関連はクロス参照)し、重要度順に並べた表を出す。**これが唯一の納品物。**

```text
| No | 対象ドキュメント | 該当箇所 | 読み止まる理由 | 想定される影響 | 確認すべき事項 | 改善案 | 優先度 |
```

各列のルール:
- **該当箇所**: 章番号・見出し・実在ID(SCR/API/TBL/FR/UC等)で特定できる情報。
- **読み止まる理由**: なぜそこで詰まるかを具体的に。「分かりにくい」は不可(例:「SCR-022 は表示名必須だが API-015 は任意で、空文字更新の可否が読めない」)。
- **想定される影響**: そのまま進めた場合の事象(解釈分裂 / 画面・API不整合 / 権限チェック漏れ / エラー時挙動未定義 / 保持データ判断不能 等)。
- **確認すべき事項**: 仕様確定のための質問。
- **改善案**: ドキュメント修正に落とせる粒度。
- **優先度**: 高(仕様判断・実装に直接影響)/ 中(設計理解に支障、補足で解決)/ 低(用語・表現で読みやすくなる)。

監査証跡として `_nlm/readability/FINDINGS.md`(統合表+検証メモ+偽陽性除外理由)を残す。

## § 6. 注意

- **指摘の修正まではしない。** 本スキルは「読み止まりの洗い出し(レビュー)」が役割。修正・反映は別途(設計変更時は CLAUDE.md の双方向影響調査に従う)。
- 要件定義/基本設計/詳細設計の**粒度混在**を見つけたら指摘する(例:要件にUIラベル・HTTPコード・物理カラム名が混入)。
- 要件が基本設計を**逆参照**している構造を見つけたら必ず指摘する。
- 上位ドキュメントの変更が下位に**未反映**なら指摘する。
- ステークホルダー判断が要る項目は、必要に応じ CLAUDE.md の課題管理に従い GitHub Issue 化する。

## 完了条件

- 読み止まり箇所が8列一覧表で整理されている。
- 各指摘に 理由・影響・確認事項・改善案・優先度 がある。
- 全指摘が grep 検証済みで、偽陽性は除外理由付きで記録されている。
- 実装者が「次に何を確認・修正すべきか」を判断できる。
