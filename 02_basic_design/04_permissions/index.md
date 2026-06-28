# 権限設計

> **このページは、認可判定フロー・ロール別業務UC遂行可否マトリクス・ロール別操作権限の一覧と、UC / 画面(SCR)/ 画面イベント(EVT)/ API から権限への対応表です。** 認証後のユーザーは、アクセス対象プロジェクトとの関係に基づき「オーナー（対象プロジェクトの作成者）」または「メンバー（当該プロジェクトへの有効な割当を持つ非オーナー）」として導出されます。各権限ルールは `PERM-NNN.md` で個別定義し、拒否時のエラーは [エラー設計](../05_errors/index.md)、画面文言・メールは [メッセージ設計](../06_messages/index.md) を参照します。

*ステータス ドラフト*

## <span id="reading"></span>読み順

要件定義(FR / BR / RULE)＞ 本権限設計 ＞ API設計 / エラー設計 / メッセージ設計。認可判定の各段は [PERM-002](PERM-002.md#PERM-002) を参照する。

## <span id="auth-flow"></span>0. 認可判定フロー（4層モデル）

1 リクエストが業務処理へ到達するまでに通す 4 つの業務的関門です。上から順に評価し、いずれかで拒否されると後続の関門には進みません。

```mermaid
graph TD
    A[リクエスト受信] --> B{第1層:セッション/規約}
    B -- No --> B1[認証エラー/再同意誘導]
    B -- Yes --> C{第2層:プロジェクト境界判定}
    C -- 割当なし/部外者 --> C1[404:リソースの存在を秘匿]
    C -- 割当あり/関係者 --> D{第3層:操作権限判定}
    D -- 権限なし --> D1[403:権限不足]
    D -- 権限あり --> E{第4層:重要操作再認証}
    E -- 未充足 --> E1[再認証要求]
    E -- 充足 --> F[業務処理実行]
```

| 関門 | 業務的意味 | 拒否パターン | 参照 |
|----|----|----|----|
| 第1層: セッション・規約 | 本人確認済みで、アカウントが有効かつ規約に同意しているか | 認証エラー・再同意誘導 | [PERM-007](PERM-007.md#PERM-007) [PERM-008](PERM-008.md#PERM-008) [PERM-009](PERM-009.md#PERM-009) [PERM-010](PERM-010.md#PERM-010) |
| 第2層: プロジェクト境界 | 対象リソースが自分の所有または割当プロジェクト範囲内か | 404 偽装（存在を明かさない） | [PERM-005](PERM-005.md#PERM-005) |
| 第3層: 操作権限 | ロールとして許可された操作か（オーナー専有・保護制約含む） | 403 権限不足 | [PERM-001](PERM-001.md#PERM-001) [PERM-003](PERM-003.md#PERM-003) [PERM-004](PERM-004.md#PERM-004) |
| 第4層: 重要操作再認証 | 不可逆・高リスク操作の直前に本人確認を再実施 | 再認証要求 | [PERM-006](PERM-006.md#PERM-006) |

上記の4層は、実装上の判定順序([PERM-002](PERM-002.md#PERM-002) の「11 段」)を業務的にまとめたものである。対応は次のとおり。

| 4層モデル | 対応する判定段(PERM-002) | 拒否の型 |
|----|----|----|
| 第1層: セッション・規約 | 段1 セッション / 段2 アカウント有効性 / 段3 規約再同意 / 段4 課金・アカウント状態ゲート | 再誘導・認証エラー |
| 第2層: プロジェクト境界 | 段5 オーナー判定 / 段6 所有境界 / 段7 割当境界 | **404 偽装** |
| 第3層: 操作権限 | 段8 オーナー専有 / 段9 オーナー保護・自己操作禁止 | 403 |
| 第4層: 重要操作再認証 | 段10 再認証判定 | 再認証要求 |

(段11 利用上限判定は認可通過後の業務判定であり、本フローの後段に位置する。)

## <span id="matrix"></span>1. ロール別業務UC遂行可否マトリクス

アクター定義: **未認証ユーザー** = ログイン前の利用者。**プロジェクトオーナー** = 対象プロジェクトの作成者（管理・課金責任を負う全権者）。**プロジェクトメンバー** = 当該プロジェクトに有効な割当を持つ利用者（オーナー除く）。◯ = 実行可 / × = 実行不可 / — = 対象外（当該アクターの文脈で発生しない操作）。備考欄は △（制限あり）の場合のみ具体的内容を記載。

> [!NOTE]
> **前提条件（第2層）**: 本表は第2層（プロジェクト境界判定）を通過した「関係者」に対する操作認可を定義するものである。第2層に未達のユーザー（割当なし・部外者）には、業務内容を問わず一律 404 を返す。「割当なし」は操作権限の問題ではなく境界チェックの問題であり、個別 PERM の権限表には登場しない。詳細は [PERM-005](PERM-005.md#PERM-005)。

| 業務カテゴリ | 業務ユースケース | 未認証 | オーナー | メンバー | 備考 |
|----|----|----|----|----|-----|
| **認証・アカウント登録** | [UC-001](../../01_requirements/04_business_usecases/UC-001.md#UC-001) ログイン | ◯ | × | × | ログイン前にのみ実行 |
| | [UC-002](../../01_requirements/04_business_usecases/UC-002.md#UC-002) アカウント新規作成 | ◯ | × | × | |
| | [UC-003](../../01_requirements/04_business_usecases/UC-003.md#UC-003) 登録確認メール検証 | ◯ | × | × | |
| | [UC-004](../../01_requirements/04_business_usecases/UC-004.md#UC-004) パスワード再設定要求 | ◯ | × | × | |
| | [UC-005](../../01_requirements/04_business_usecases/UC-005.md#UC-005) 新しいパスワードを設定 | ◯ | × | × | |
| | [UC-006](../../01_requirements/04_business_usecases/UC-006.md#UC-006) 招待受諾 | ◯ | × | × | 招待リンクから有効化 |
| **アカウント管理** | [UC-007](../../01_requirements/04_business_usecases/UC-007.md#UC-007) 連絡先メールアドレス確認 | × | ◯ | ◯ | |
| | [UC-008](../../01_requirements/04_business_usecases/UC-008.md#UC-008) 個人プロフィール閲覧 | × | ◯ | ◯ | |
| | [UC-009](../../01_requirements/04_business_usecases/UC-009.md#UC-009) 個人プロフィール編集 | × | ◯ | ◯ | △ 再認証必須 |
| | [UC-010](../../01_requirements/04_business_usecases/UC-010.md#UC-010) パスワード変更 | × | ◯ | ◯ | △ 再認証必須 |
| | [UC-011](../../01_requirements/04_business_usecases/UC-011.md#UC-011) 利用規約閲覧 | × | ◯ | ◯ | |
| | [UC-012](../../01_requirements/04_business_usecases/UC-012.md#UC-012) プライバシーポリシー閲覧 | × | ◯ | ◯ | |
| | [UC-013](../../01_requirements/04_business_usecases/UC-013.md#UC-013) 改定文書への再同意 | × | ◯ | ◯ | アカウント単位（立場を問わない） |
| | [UC-022](../../01_requirements/04_business_usecases/UC-022.md#UC-022) アカウント退会 | × | ◯ | ◯ | △ 再認証必須・アカウント単位 |
| **プロジェクト管理** | [UC-014](../../01_requirements/04_business_usecases/UC-014.md#UC-014) Myプロジェクト一覧閲覧 | × | ◯ | × | 自身が所有するプロジェクト一覧 |
| | [UC-015](../../01_requirements/04_business_usecases/UC-015.md#UC-015) プロジェクト作成 | × | ◯ | × | オーナー専有 |
| | [UC-016](../../01_requirements/04_business_usecases/UC-016.md#UC-016) プロジェクト編集 | × | ◯ | × | オーナー専有 |
| | [UC-017](../../01_requirements/04_business_usecases/UC-017.md#UC-017) プロジェクト削除 | × | ◯ | × | △ オーナー専有・再認証必須 |
| | [UC-082](../../01_requirements/04_business_usecases/UC-082.md#UC-082) Joinプロジェクト一覧閲覧 | × | ◯ | ◯ | メンバーとして参加中のプロジェクト一覧 |
| **メンバー管理** | [UC-018](../../01_requirements/04_business_usecases/UC-018.md#UC-018) メンバー一覧閲覧 | × | ◯ | ◯ | |
| | [UC-019](../../01_requirements/04_business_usecases/UC-019.md#UC-019) メンバー招待 | × | ◯ | ◯ | △ 再認証必須 |
| | [UC-020](../../01_requirements/04_business_usecases/UC-020.md#UC-020) メンバー情報編集 | × | ◯ | ◯ | |
| | [UC-021](../../01_requirements/04_business_usecases/UC-021.md#UC-021) メンバー削除 | × | ◯ | ◯ | △ 再認証必須。オーナーへの実行は不可（[PERM-004](PERM-004.md#PERM-004)） |
| **FAQ・質問管理** | [UC-023](../../01_requirements/04_business_usecases/UC-023.md#UC-023) FAQ 一覧閲覧 | × | ◯ | ◯ | |
| | [UC-024](../../01_requirements/04_business_usecases/UC-024.md#UC-024) FAQ 作成・編集 | × | ◯ | ◯ | |
| | [UC-025](../../01_requirements/04_business_usecases/UC-025.md#UC-025) FAQ 削除 | × | ◯ | ◯ | |
| | [UC-026](../../01_requirements/04_business_usecases/UC-026.md#UC-026) FAQ 公開状態一括変更 | × | ◯ | ◯ | |
| | [UC-027](../../01_requirements/04_business_usecases/UC-027.md#UC-027) FAQ インポート（CSV） | × | ◯ | ◯ | |
| | [UC-028](../../01_requirements/04_business_usecases/UC-028.md#UC-028) FAQ エクスポート（CSV） | × | ◯ | ◯ | |
| | [UC-029](../../01_requirements/04_business_usecases/UC-029.md#UC-029) 未解決質問一覧閲覧 | × | ◯ | ◯ | |
| | [UC-030](../../01_requirements/04_business_usecases/UC-030.md#UC-030) 未解決質問詳細確認 | × | ◯ | ◯ | |
| | [UC-031](../../01_requirements/04_business_usecases/UC-031.md#UC-031) 未解決質問対応状況更新 | × | ◯ | ◯ | |
| | [UC-074](../../01_requirements/04_business_usecases/UC-074.md#UC-074) プロジェクト範囲の FAQ・質問ログ・未解決操作 | × | ◯ | ◯ | |
| | [UC-075](../../01_requirements/04_business_usecases/UC-075.md#UC-075) プロジェクト単位の信頼度・関連度しきい値調整 | × | ◯ | ◯ | |
| | [UC-076](../../01_requirements/04_business_usecases/UC-076.md#UC-076) FAQ・質問ログ検索 | × | ◯ | ◯ | |
| **ダッシュボード・利用量** | [UC-032](../../01_requirements/04_business_usecases/UC-032.md#UC-032) プロジェクト概要ダッシュボード閲覧 | × | ◯ | ◯ | |
| | [UC-033](../../01_requirements/04_business_usecases/UC-033.md#UC-033) 利用量と上限の閲覧 | × | ◯ | ◯ | |
| | [UC-034](../../01_requirements/04_business_usecases/UC-034.md#UC-034) 利用上限・アラート閾値設定 | × | ◯ | ◯ | △ 再認証必須 |
| **請求・課金** | [UC-035](../../01_requirements/04_business_usecases/UC-035.md#UC-035) 請求管理（プロジェクト別課金状況）閲覧 | × | ◯ | × | オーナー専有 |
| | [UC-036](../../01_requirements/04_business_usecases/UC-036.md#UC-036) 請求情報閲覧 | × | ◯ | × | オーナー専有 |
| | [UC-037](../../01_requirements/04_business_usecases/UC-037.md#UC-037) 支払方法登録・更新 | × | ◯ | ◯ | △ 再認証必須・アカウント単位（プロジェクトの立場を問わない） |
| | [UC-081](../../01_requirements/04_business_usecases/UC-081.md#UC-081) 退会済みユーザーによる請求情報閲覧 | × | ◯ | × | 退会後も本人のみ閲覧可 |
| **ウィジェット設定** | [UC-038](../../01_requirements/04_business_usecases/UC-038.md#UC-038) ウィジェット設定編集 | × | ◯ | ◯ | |
| | [UC-039](../../01_requirements/04_business_usecases/UC-039.md#UC-039) ウィジェット公開キー再発行 | × | ◯ | ◯ | |
| **お知らせ** | [UC-043](../../01_requirements/04_business_usecases/UC-043.md#UC-043) お知らせ一覧閲覧 | × | ◯ | ◯ | |
| | [UC-044](../../01_requirements/04_business_usecases/UC-044.md#UC-044) お知らせ詳細閲覧 | × | ◯ | ◯ | |
| | [UC-045](../../01_requirements/04_business_usecases/UC-045.md#UC-045) お知らせ既読化 | × | ◯ | ◯ | |
| **ウィジェット利用者主体** | [UC-040](../../01_requirements/04_business_usecases/UC-040.md#UC-040)〜[UC-042](../../01_requirements/04_business_usecases/UC-042.md#UC-042) ウィジェット操作（チャット / 検索 / 案内） | — | — | — | ウィジェット利用者（公開キー認証）が主体 |
| | [UC-057](../../01_requirements/04_business_usecases/UC-057.md#UC-057) 許可ドメイン上でのみウィジェット動作 | — | — | — | システムによる制御。ウィジェット利用者の前提条件 |
| **システム主体の自動処理** | [UC-046](../../01_requirements/04_business_usecases/UC-046.md#UC-046)〜[UC-053](../../01_requirements/04_business_usecases/UC-053.md#UC-053) 利用量・AI 推論・上限制御 | — | — | — | システムが主体の処理。ユーザーロール権限外 |
| | [UC-054](../../01_requirements/04_business_usecases/UC-054.md#UC-054)〜[UC-056](../../01_requirements/04_business_usecases/UC-056.md#UC-056) 月次請求確定・サスペンション・課金 Webhook | — | — | — | システム・外部連携が主体 |
| | [UC-058](../../01_requirements/04_business_usecases/UC-058.md#UC-058)〜[UC-065](../../01_requirements/04_business_usecases/UC-065.md#UC-065) メール配信・通知自動生成 | — | — | — | システムが主体の処理 |
| | [UC-066](../../01_requirements/04_business_usecases/UC-066.md#UC-066)〜[UC-073](../../01_requirements/04_business_usecases/UC-073.md#UC-073) データ削除・セッション管理・監査・レート制限 | — | — | — | システムが主体の処理 |
| | [UC-077](../../01_requirements/04_business_usecases/UC-077.md#UC-077)〜[UC-080](../../01_requirements/04_business_usecases/UC-080.md#UC-080) 通知・お知らせ管理 | — | — | — | システムが主体の処理 |

## <span id="list"></span>2. ロール別操作権限一覧（11）

権限ルールの索引です。各 PERM の定義（判定基準・不変条件・権限不足時の挙動）は個別ファイルが正本です。ロールはオーナー / メンバー / 未認証の 3 区分です（ウィジェット利用者は管理画面とは独立した別系統の認証を使用）。「割当なし」ユーザーは第2層（プロジェクト境界判定）で 404 偽装により除外されるため、個別ファイルの操作権限表には登場しません。

| PERM ID | 権限ルール | 概要 |
| ---- | ---- | ---- |
| <span id="PERM-001"></span>[PERM-001](PERM-001.md#PERM-001) | ユーザー種別とオーナー判定 | 認可の起点となるユーザー種別(オーナー / メンバー / ウィジェット利用者)の判定方法と権限の表し方を定義します。 |
| <span id="PERM-002"></span>[PERM-002](PERM-002.md#PERM-002) | 認可判定の順序 | 1 リクエストを許可するまでに通す認可判定の段(セッション → 課金アカウント状態 / アカウント状態 → 対象プロジェクトのオーナー判定 → 所有境界 / 割当境界 → 専有 → 再認証 → 利用上限)と、各段の拒否時エラーを定義します。 |
| <span id="PERM-003"></span>[PERM-003](PERM-003.md#PERM-003) | オーナー専有機能 | 非オーナーに付与してはならないオーナー専有機能(当該プロジェクトの課金・請求確認・プロジェクト CRUD)と、アカウント本人単位の操作(退会・規約再同意)、その判定段を定義します。 |
| <span id="PERM-004"></span>[PERM-004](PERM-004.md#PERM-004) | オーナー保護・自己操作禁止 | 運用が止まらないための保護制約(オーナーへの退会・停止・削除・降格・譲渡の禁止、自己操作の禁止)を定義します。 |
| <span id="PERM-005"></span>[PERM-005](PERM-005.md#PERM-005) | オーナー境界・プロジェクト境界判定 | 他オーナー・他プロジェクトのデータへ越境させない境界チェック(プロジェクト所有境界・プロジェクト割当)と、404 偽装による拒否を定義します。 |
| <span id="PERM-006"></span>[PERM-006](PERM-006.md#PERM-006) | 重要操作の再認証 | 不可逆・高リスクな操作の直前に求める再認証と、対象操作を定義します。再認証の有効範囲は [システム仕様書 §3](../07_system-spec.md#3-タイムアウトセッション認証) を参照します。 |
| <span id="PERM-007"></span>[PERM-007](PERM-007.md#PERM-007) | セッションとログイン失敗ロックアウト | セッション寿命・複数デバイス同時ログイン・失効優先順位と、連続ログイン失敗によるロックアウトを定義します。具体値は [システム仕様書 §3](../07_system-spec.md#3-タイムアウトセッション認証) を参照します。 |
| <span id="PERM-008"></span>[PERM-008](PERM-008.md#PERM-008) | アカウント状態と利用可否 | アカウント状態(有効 / 招待中 / メール未確認 / ロック中 / 無効化)ごとのログイン可否と利用範囲を定義します。 |
| <span id="PERM-009"></span>[PERM-009](PERM-009.md#PERM-009) | 課金アカウント状態・アカウント状態によるアクセス制限 | 課金アカウント状態(停止中)・アカウント状態(退会済み / 削除済み)ごとに管理画面で許す操作とセッションの扱いを定義します。 |
| <span id="PERM-010"></span>[PERM-010](PERM-010.md#PERM-010) | 規約再同意の認可割込み | 規約・プライバシーポリシー改定時に、ログイン後の認可フローへ再同意画面を割り込ませる発火条件と段階適用を定義します。 |
| <span id="PERM-011"></span>[PERM-011](PERM-011.md#PERM-011) | critical 通知の宛先解決 | critical 通知を「誰に送るか」を決める宛先解決(オーナー + 当該プロジェクトの有効メンバーの 2 系統合算・重複排除)を定義します。 |

## <span id="stages"></span>3. 認可判定の順序（正本）

1 リクエストを許可するまでに通す認可判定の段です。上から評価し、各段の拒否時エラーは [エラー設計](../05_errors/index.md) が正本です。詳細は [PERM-002](PERM-002.md#PERM-002)。

| \# | 判定段 | 内容 | 拒否時のエラー |
|----|----|----|----|
| 1 | セッション検証 | [システム仕様書 §3](../07_system-spec.md#3-タイムアウトセッション認証) のセッション有効条件を満たすか | [`E-AUTH-SESSION-EXPIRED`](../05_errors/index.md) |
| 2 | アカウント有効性 | アカウントが利用可能状態か（無効化済みなら再ログインへ誘導） | — |
| 3 | 規約再同意ゲート | 改定済みで未同意の文書があれば再同意画面へ割込み | `E-AUTHZ-TERMS` |
| 4 | 課金アカウント状態 / アカウント状態ゲート | 対象プロジェクトのオーナーの課金アカウントが停止状態か、本人のアカウントが退会済み・削除済みかを確認し、該当時はアクセス制限を適用 | [ERR-004](../05_errors/ERR-004.md#ERR-004) 等 |
| 5 | 対象プロジェクトのオーナー判定 | 対象プロジェクトの作成者とアクセス主体が一致するなら当該プロジェクト内を許可（グローバルなバイパスではなく対象プロジェクト単位の判定） | — |
| 6 | プロジェクト所有境界判定 | オーナーとしての操作は、対象プロジェクトが自分の所有するプロジェクトであることを要求。所有外は 404 偽装 | `E-AUTHZ-OWNER-BOUNDARY` |
| 7 | プロジェクト割当境界判定 | 非オーナーは対象プロジェクトへの有効な割当があること。割当なし・部外者は一律 404 偽装(存在を明かさない) | [ERR-017](../05_errors/ERR-017.md#ERR-017)(割当境界違反の 404 偽装) |
| 8 | オーナー専有機能判定 | 専有機能を非オーナーが要求した場合は 403 | [ERR-015](../05_errors/ERR-015.md#ERR-015) |
| 9 | オーナー保護・自己操作禁止 | 不可制約に該当すれば拒否 | [ERR-021](../05_errors/ERR-021.md#ERR-021) / [ERR-022](../05_errors/ERR-022.md#ERR-022) |
| 10 | 再認証判定 | 重要操作で [システム仕様書 §3](../07_system-spec.md#3-タイムアウトセッション認証) の再認証有効条件を満たすか | `E-AUTH-REAUTH-REQUIRED` |
| 11 | 利用上限判定 | 認可通過後に上限を確認（レート = オーナー単位、上限・無料枠 = プロジェクト単位） | [課金・請求設計書](../05_billing-design.md) |

## <span id="trace"></span>4. 業務UC / 画面 / EVT / API ↔ 権限 対応表

各権限ルールが関係する業務ユースケースIDと、適用される画面・イベント・API の結線一覧です。結線の無い欄は `—` とします。厳密な層間対応は [トレーサビリティ一覧](../00_traceability/index.md) で一元管理します。

| PERM ID | 業務ユースケースID | 対応画面SCR | 対応EVT | 対応API |
|----|----|----|----|----|
| [PERM-001](PERM-001.md#PERM-001) | [UC-018](../../01_requirements/04_business_usecases/UC-018.md#UC-018) | [SCR-013](../01_frontend/01_screens/SCR-013.md#SCR-013) | — | [API-002](../02_backend/03_apis/API-002.md#API-002) |
| [PERM-002](PERM-002.md#PERM-002) | [UC-067](../../01_requirements/04_business_usecases/UC-067.md#UC-067) | — | — | — |
| [PERM-003](PERM-003.md#PERM-003) | [UC-013](../../01_requirements/04_business_usecases/UC-013.md#UC-013) ・ [UC-015](../../01_requirements/04_business_usecases/UC-015.md#UC-015) ・ [UC-016](../../01_requirements/04_business_usecases/UC-016.md#UC-016) ・ [UC-017](../../01_requirements/04_business_usecases/UC-017.md#UC-017) ・ [UC-009](../../01_requirements/04_business_usecases/UC-009.md#UC-009) ・ [UC-022](../../01_requirements/04_business_usecases/UC-022.md#UC-022) ・ [UC-035](../../01_requirements/04_business_usecases/UC-035.md#UC-035) ・ [UC-036](../../01_requirements/04_business_usecases/UC-036.md#UC-036) ・ [UC-037](../../01_requirements/04_business_usecases/UC-037.md#UC-037) | [SCR-005](../01_frontend/01_screens/SCR-005.md#SCR-005) [SCR-019](../01_frontend/01_screens/SCR-019.md#SCR-019) [SCR-028](../01_frontend/01_screens/SCR-028.md#SCR-028) | — | [API-014](../02_backend/03_apis/API-014.md#API-014) [API-015](../02_backend/03_apis/API-015.md#API-015) [API-017](../02_backend/03_apis/API-017.md#API-017) [API-018](../02_backend/03_apis/API-018.md#API-018) [API-045](../02_backend/03_apis/API-045.md#API-045) [API-056](../02_backend/03_apis/API-056.md#API-056) |
| [PERM-004](PERM-004.md#PERM-004) | — | [SCR-013](../01_frontend/01_screens/SCR-013.md#SCR-013) | — | [API-023](../02_backend/03_apis/API-023.md#API-023) [API-024](../02_backend/03_apis/API-024.md#API-024) |
| [PERM-005](PERM-005.md#PERM-005) | — | [SCR-013](../01_frontend/01_screens/SCR-013.md#SCR-013) | — | [API-018](../02_backend/03_apis/API-018.md#API-018) [API-021](../02_backend/03_apis/API-021.md#API-021) [API-047](../02_backend/03_apis/API-047.md#API-047) |
| [PERM-006](PERM-006.md#PERM-006) | [UC-009](../../01_requirements/04_business_usecases/UC-009.md#UC-009) | [SCR-019](../01_frontend/01_screens/SCR-019.md#SCR-019) [SCR-034](../01_frontend/01_screens/SCR-034.md#SCR-034) | SCR-034 EVT-02 | [API-005](../02_backend/03_apis/API-005.md#API-005) [API-015](../02_backend/03_apis/API-015.md#API-015) [API-013](../02_backend/03_apis/API-013.md#API-013) [API-045](../02_backend/03_apis/API-045.md#API-045) [API-056](../02_backend/03_apis/API-056.md#API-056) |
| [PERM-007](PERM-007.md#PERM-007) | [UC-001](../../01_requirements/04_business_usecases/UC-001.md#UC-001) | [SCR-001](../01_frontend/01_screens/SCR-001.md#SCR-001) | SCR-001 EVT-02 | [API-002](../02_backend/03_apis/API-002.md#API-002) [API-003](../02_backend/03_apis/API-003.md#API-003) |
| [PERM-008](PERM-008.md#PERM-008) | [UC-002](../../01_requirements/04_business_usecases/UC-002.md#UC-002) | [SCR-018](../01_frontend/01_screens/SCR-018.md#SCR-018) [SCR-023](../01_frontend/01_screens/SCR-023.md#SCR-023) | SCR-018 EVT-01 SCR-023 EVT-04 | [API-006](../02_backend/03_apis/API-006.md#API-006) [API-008](../02_backend/03_apis/API-008.md#API-008) [API-023](../02_backend/03_apis/API-023.md#API-023) |
| [PERM-009](PERM-009.md#PERM-009) | [UC-055](../../01_requirements/04_business_usecases/UC-055.md#UC-055) | — | — | [API-002](../02_backend/03_apis/API-002.md#API-002) [API-037](../02_backend/03_apis/API-037.md#API-037) |
| [PERM-010](PERM-010.md#PERM-010) | [UC-013](../../01_requirements/04_business_usecases/UC-013.md#UC-013) | [SCR-020](../01_frontend/01_screens/SCR-020.md#SCR-020) | SCR-015 EVT-03 SCR-020 EVT-06 | [API-052](../02_backend/03_apis/API-052.md#API-052) [API-054](../02_backend/03_apis/API-054.md#API-054) [API-055](../02_backend/03_apis/API-055.md#API-055) |
| [PERM-011](PERM-011.md#PERM-011) | [UC-052](../../01_requirements/04_business_usecases/UC-052.md#UC-052) | — | — | [API-021](../02_backend/03_apis/API-021.md#API-021) [API-024](../02_backend/03_apis/API-024.md#API-024) |

## <span id="auth-ref"></span>5. 認証フロー（参照）

認証（本人確認）の各フロー — ログイン / ログアウト / パスワード再設定 / 招待受諾（メンバー有効化）/ メール確認 / 強制ログアウト — のシーケンスは、各画面起点の業務ユースケース（[業務ユースケース設計](../../01_requirements/04_business_usecases/index.md)）のシーケンス図が正本です。本権限設計は判定段とロール別可否を正本化します。

| 認証フロー | 主な根拠要件 | 関連 PERM |
|----|----|----|
| ログイン | [FR-001](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-001) | [PERM-007](PERM-007.md#PERM-007) |
| ログイン失敗ロックアウト | [RULE-001](../../01_requirements/01_business_requirement/08_rule.md#RULE-001) | [PERM-007](PERM-007.md#PERM-007) |
| パスワード再設定 | [RULE-003](../../01_requirements/01_business_requirement/08_rule.md#RULE-003) | [PERM-008](PERM-008.md#PERM-008) |
| 招待受諾（メンバー有効化） | [RULE-007](../../01_requirements/01_business_requirement/08_rule.md#RULE-007) | [PERM-008](PERM-008.md#PERM-008) |
| メール確認 | [FR-003](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-003) | [PERM-008](PERM-008.md#PERM-008) |
| 強制ログアウト（サスペンション / アカウント停止時） | [FR-011](../../01_requirements/02_functional_requirement/01_account-fr.md#FR-011) | [PERM-007](PERM-007.md#PERM-007) [PERM-009](PERM-009.md#PERM-009) |
