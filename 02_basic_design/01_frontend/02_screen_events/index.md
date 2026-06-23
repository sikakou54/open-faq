<!-- portal-top -->
[設計ポータル](../../../README.md) ／ [基本設計](../../index.md) ／ [フロントエンド設計](../index.md) ／ **画面イベント設計**
<!-- /portal-top -->

# 画面イベント設計

> **このセクションは、各画面(SCR)の画面イベントを `EVT-NNN` として個別に定義します。** 1 画面イベント = 1 ファイル。各 EVT は対応画面・対応業務UC(UC)・対象項目・呼出API・遷移先・処理内容を持ちます。

*版数 v1.0 ・ 更新 2026-06-21 ・ イベント数 229 ・ 再構成 P3*

## 1. 画面別 EVT 一覧

画面(SCR)ごとに、その画面イベント `EVT-NNN` を列挙します。

### <span id="SCR-001"></span>SCR-001 ログイン

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-001`](EVT-001.md#EVT-001) | 初期表示 | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-002`](EVT-002.md#EVT-002) | メールアドレスを入力 | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-003`](EVT-003.md#EVT-003) | パスワードを入力 | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-004`](EVT-004.md#EVT-004) | 「ログイン」を押下 | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-005`](EVT-005.md#EVT-005) | 「パスワードを忘れた場合」を押下 | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) |
| [`EVT-006`](EVT-006.md#EVT-006) | 「アカウント登録」を押下 | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |

### <span id="SCR-002"></span>SCR-002 アカウント登録

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-007`](EVT-007.md#EVT-007) | 初期表示 | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-008`](EVT-008.md#EVT-008) | メールアドレスを入力 | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-009`](EVT-009.md#EVT-009) | パスワードを入力 | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-010`](EVT-010.md#EVT-010) | パスワード(確認)を入力 | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-011`](EVT-011.md#EVT-011) | 業種を選択 | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-012`](EVT-012.md#EVT-012) | 「利用規約に同意する」をチェック | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-013`](EVT-013.md#EVT-013) | 「プライバシーポリシーに同意する」をチェック | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-014`](EVT-014.md#EVT-014) | 「利用規約を別ウィンドウで表示」を押下 | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-015`](EVT-015.md#EVT-015) | 「プライバシーポリシーを別ウィンドウで表示」を押下 | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-016`](EVT-016.md#EVT-016) | 「登録して確認メールを送信する」を押下 | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-017`](EVT-017.md#EVT-017) | 「ログインする」を押下 | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-018`](EVT-018.md#EVT-018) | Turnstile 検証を完了 | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |

### <span id="SCR-003"></span>SCR-003 パスワード再設定

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-019`](EVT-019.md#EVT-019) | 初期表示(段階 1) | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) |
| [`EVT-020`](EVT-020.md#EVT-020) | 「再設定リンクを送信」を押下 | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) |
| [`EVT-021`](EVT-021.md#EVT-021) | 「メールを再送信する」を押下 | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) |
| [`EVT-022`](EVT-022.md#EVT-022) | 初期表示(段階 2) | [UC-005](../../../01_requirements/04_business_usecases/UC-005.md#UC-005) |
| [`EVT-023`](EVT-023.md#EVT-023) | 「再送する」を押下(段階 2 エラー時) | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) |
| [`EVT-024`](EVT-024.md#EVT-024) | 新パスワードを入力 | [UC-005](../../../01_requirements/04_business_usecases/UC-005.md#UC-005) |
| [`EVT-025`](EVT-025.md#EVT-025) | 「新しいパスワードを設定する」を押下 | [UC-005](../../../01_requirements/04_business_usecases/UC-005.md#UC-005) |
| [`EVT-026`](EVT-026.md#EVT-026) | 「ログインする」を押下 | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-027`](EVT-027.md#EVT-027) | 「ログインに戻る」を押下 | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) |

### <span id="SCR-004"></span>SCR-004 プロジェクト

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-028`](EVT-028.md#EVT-028) | 初期表示 | [UC-014](../../../01_requirements/04_business_usecases/UC-014.md#UC-014) |
| [`EVT-029`](EVT-029.md#EVT-029) | 「+ 新規プロジェクトを作成」を押下 | [UC-014](../../../01_requirements/04_business_usecases/UC-014.md#UC-014) |
| [`EVT-030`](EVT-030.md#EVT-030) | プロジェクト名リンクを押下 | [UC-014](../../../01_requirements/04_business_usecases/UC-014.md#UC-014) |
| [`EVT-031`](EVT-031.md#EVT-031) | 管理範囲を切り替え | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-032`](EVT-032.md#EVT-032) | 空状態の「+ 新規プロジェクトを作成」を押下 | [UC-014](../../../01_requirements/04_business_usecases/UC-014.md#UC-014) |

### <span id="SCR-005"></span>SCR-005 プロジェクト作成・編集モーダル

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-033`](EVT-033.md#EVT-033) | 初期表示(新規モード) | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) |
| [`EVT-034`](EVT-034.md#EVT-034) | 初期表示(編集モード) | [UC-016](../../../01_requirements/04_business_usecases/UC-016.md#UC-016) |
| [`EVT-035`](EVT-035.md#EVT-035) | プロジェクト名を入力 | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) |
| [`EVT-036`](EVT-036.md#EVT-036) | 許可ドメインを入力 | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) |
| [`EVT-037`](EVT-037.md#EVT-037) | プロジェクト連絡先メールを入力 | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) |
| [`EVT-038`](EVT-038.md#EVT-038) | 「プロジェクトを作成」を押下 | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) |
| [`EVT-039`](EVT-039.md#EVT-039) | 「保存」を押下 | [UC-016](../../../01_requirements/04_business_usecases/UC-016.md#UC-016) |
| [`EVT-040`](EVT-040.md#EVT-040) | 「確認メールを再送」を押下 | [UC-016](../../../01_requirements/04_business_usecases/UC-016.md#UC-016) |
| [`EVT-041`](EVT-041.md#EVT-041) | 削除確認名称を入力 | [UC-017](../../../01_requirements/04_business_usecases/UC-017.md#UC-017) |
| [`EVT-042`](EVT-042.md#EVT-042) | 「プロジェクトを削除」を押下 | [UC-017](../../../01_requirements/04_business_usecases/UC-017.md#UC-017) |
| [`EVT-043`](EVT-043.md#EVT-043) | 「キャンセル」を押下 | [UC-016](../../../01_requirements/04_business_usecases/UC-016.md#UC-016) |
| [`EVT-044`](EVT-044.md#EVT-044) | 「コピー」を押下(プロジェクト ID) | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) |
| [`EVT-045`](EVT-045.md#EVT-045) | × を押下 | [UC-016](../../../01_requirements/04_business_usecases/UC-016.md#UC-016) |

### <span id="SCR-006"></span>SCR-006 要対応の質問一覧

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-046`](EVT-046.md#EVT-046) | 初期表示 | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-047`](EVT-047.md#EVT-047) | 状況フィルタをチェック | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-048`](EVT-048.md#EVT-048) | 期間フィルタを入力 | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-049`](EVT-049.md#EVT-049) | 「CSV エクスポート」を押下 | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-050`](EVT-050.md#EVT-050) | 問い合わせ ID リンクを押下 | [UC-031](../../../01_requirements/04_business_usecases/UC-031.md#UC-031) |
| [`EVT-051`](EVT-051.md#EVT-051) | 検索ボックスに入力 | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-052`](EVT-052.md#EVT-052) | ページを選択 | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-053`](EVT-053.md#EVT-053) | 「ウィジェット設定を見る」を押下 | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |

### <span id="SCR-007"></span>SCR-007 要対応の質問詳細

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-054`](EVT-054.md#EVT-054) | 初期表示 | [UC-031](../../../01_requirements/04_business_usecases/UC-031.md#UC-031) |
| [`EVT-055`](EVT-055.md#EVT-055) | 「対応済み」を選択 | [UC-032](../../../01_requirements/04_business_usecases/UC-032.md#UC-032) |
| [`EVT-056`](EVT-056.md#EVT-056) | 「対応中」を選択 | [UC-032](../../../01_requirements/04_business_usecases/UC-032.md#UC-032) |
| [`EVT-057`](EVT-057.md#EVT-057) | 確認ダイアログの「OK」を押下 | [UC-032](../../../01_requirements/04_business_usecases/UC-032.md#UC-032) |
| [`EVT-058`](EVT-058.md#EVT-058) | 確認ダイアログの「キャンセル」を押下 | [UC-032](../../../01_requirements/04_business_usecases/UC-032.md#UC-032) |
| [`EVT-059`](EVT-059.md#EVT-059) | 登録先 FAQ リンクを押下 | [UC-031](../../../01_requirements/04_business_usecases/UC-031.md#UC-031) |
| [`EVT-060`](EVT-060.md#EVT-060) | 候補 FAQ リンクを押下 | [UC-031](../../../01_requirements/04_business_usecases/UC-031.md#UC-031) |
| [`EVT-061`](EVT-061.md#EVT-061) | 「FAQ 登録へ」を押下 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |

### <span id="SCR-008"></span>SCR-008 FAQ 一覧

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-062`](EVT-062.md#EVT-062) | 初期表示 | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) |
| [`EVT-063`](EVT-063.md#EVT-063) | キーワードを入力 | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) |
| [`EVT-064`](EVT-064.md#EVT-064) | カテゴリを選択 | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) |
| [`EVT-065`](EVT-065.md#EVT-065) | 並び順を変更 | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) |
| [`EVT-066`](EVT-066.md#EVT-066) | 行を選択 | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) |
| [`EVT-067`](EVT-067.md#EVT-067) | 「+ 新規作成」を押下 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-068`](EVT-068.md#EVT-068) | FAQ ID リンクを押下 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-069`](EVT-069.md#EVT-069) | 「公開する」を押下 | [UC-027](../../../01_requirements/04_business_usecases/UC-027.md#UC-027) |
| [`EVT-070`](EVT-070.md#EVT-070) | 「非公開化する」を押下 | [UC-027](../../../01_requirements/04_business_usecases/UC-027.md#UC-027) |
| [`EVT-071`](EVT-071.md#EVT-071) | 「削除する」を押下 | [UC-026](../../../01_requirements/04_business_usecases/UC-026.md#UC-026) |
| [`EVT-072`](EVT-072.md#EVT-072) | 「選択を解除」を押下 | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) |
| [`EVT-073`](EVT-073.md#EVT-073) | 「CSV をインポート」を押下 | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-074`](EVT-074.md#EVT-074) | 「CSV をエクスポート」を押下 | [UC-029](../../../01_requirements/04_business_usecases/UC-029.md#UC-029) |
| [`EVT-075`](EVT-075.md#EVT-075) | 空状態の「+ 新規作成」を押下 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |

### <span id="SCR-009"></span>SCR-009 FAQ 編集

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-076`](EVT-076.md#EVT-076) | 初期表示 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-077`](EVT-077.md#EVT-077) | 質問を入力 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-078`](EVT-078.md#EVT-078) | 回答を入力 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-079`](EVT-079.md#EVT-079) | カテゴリを入力 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-080`](EVT-080.md#EVT-080) | 「状態」を選択 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-081`](EVT-081.md#EVT-081) | 自動保存タイマー発火(30 秒間隔) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-082`](EVT-082.md#EVT-082) | 「保存」を押下 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-083`](EVT-083.md#EVT-083) | 「削除」を押下 | [UC-026](../../../01_requirements/04_business_usecases/UC-026.md#UC-026) |
| [`EVT-084`](EVT-084.md#EVT-084) | 削除確認ダイアログの「OK」を押下 | [UC-026](../../../01_requirements/04_business_usecases/UC-026.md#UC-026) |
| [`EVT-085`](EVT-085.md#EVT-085) | 「キャンセル」を押下 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-086`](EVT-086.md#EVT-086) | 「登録元未解決質問」リンクを押下 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-087`](EVT-087.md#EVT-087) | 削除確認ダイアログの「キャンセル」を押下 | [UC-026](../../../01_requirements/04_business_usecases/UC-026.md#UC-026) |
| [`EVT-088`](EVT-088.md#EVT-088) | キャンセル確認ダイアログの「OK」を押下 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-089`](EVT-089.md#EVT-089) | キャンセル確認ダイアログの「キャンセル」を押下 | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |

### <span id="SCR-010"></span>SCR-010 FAQ CSV インポートモーダル

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-090`](EVT-090.md#EVT-090) | 初期表示 | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-091`](EVT-091.md#EVT-091) | 「テンプレートをダウンロード」を押下 | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-092`](EVT-092.md#EVT-092) | ファイル選択にファイルを投入 | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-093`](EVT-093.md#EVT-093) | 「読み込みを開始」を押下 | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-094`](EVT-094.md#EVT-094) | 「キャンセル」を押下 | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-095`](EVT-095.md#EVT-095) | 「×」を押下 | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |

### <span id="SCR-011"></span>SCR-011 ウィジェット設定

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-096`](EVT-096.md#EVT-096) | 初期表示 | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-097`](EVT-097.md#EVT-097) | 「コピー」を押下(公開キー) | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-098`](EVT-098.md#EVT-098) | 「コードをコピー」を押下(埋め込みコード) | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-099`](EVT-099.md#EVT-099) | テーマカラーを選択 | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-100`](EVT-100.md#EVT-100) | 主色(HEX)を入力 | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-101`](EVT-101.md#EVT-101) | 表示位置を選択 | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-102`](EVT-102.md#EVT-102) | 見出しを入力 | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-103`](EVT-103.md#EVT-103) | 初期メッセージを入力 | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-104`](EVT-104.md#EVT-104) | 「公開キーを再発行する」を押下 | [UC-041](../../../01_requirements/04_business_usecases/UC-041.md#UC-041) |
| [`EVT-105`](EVT-105.md#EVT-105) | 「設定を保存」を押下 | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-106`](EVT-106.md#EVT-106) | 「概要」を押下 | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |

### <span id="SCR-012"></span>SCR-012 概要(プロジェクト)

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-107`](EVT-107.md#EVT-107) | 初期表示 | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-108`](EVT-108.md#EVT-108) | 期間を選択 | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-109`](EVT-109.md#EVT-109) | 質問数カードを押下 | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-110`](EVT-110.md#EVT-110) | 未解決数カードを押下 | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-111`](EVT-111.md#EVT-111) | 公開 FAQ 件数カードを押下 | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-112`](EVT-112.md#EVT-112) | 「支払方法を更新」を押下(オーナー) | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-113`](EVT-113.md#EVT-113) | 「支払い方法を登録」を押下(オーナー) | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-114`](EVT-114.md#EVT-114) | 「利用量と上限へ」を押下 | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |

### <span id="SCR-013"></span>SCR-013 メンバー(プロジェクト)

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-115`](EVT-115.md#EVT-115) | 初期表示 | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) |
| [`EVT-116`](EVT-116.md#EVT-116) | 検索を入力 | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) |
| [`EVT-117`](EVT-117.md#EVT-117) | 招待状態フィルタを選択 | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) |
| [`EVT-118`](EVT-118.md#EVT-118) | 「+ メンバーを招待」を押下 | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) |
| [`EVT-119`](EVT-119.md#EVT-119) | (空状態)「+ メンバーを招待」を押下 | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) |
| [`EVT-120`](EVT-120.md#EVT-120) | 利用者表示名リンクを押下 | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) |
| [`EVT-121`](EVT-121.md#EVT-121) | 権限なしで URL 直アクセス | [UC-048](../../../01_requirements/04_business_usecases/UC-048.md#UC-048) |
| [`EVT-122`](EVT-122.md#EVT-122) | 「ダッシュボードへ戻る」を押下 | [UC-048](../../../01_requirements/04_business_usecases/UC-048.md#UC-048) |

### <span id="SCR-014"></span>SCR-014 メンバー招待 / 編集モーダル(プロジェクト単位)

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-123`](EVT-123.md#EVT-123) | 初期表示 — 招待モード | [UC-019](../../../01_requirements/04_business_usecases/UC-019.md#UC-019) |
| [`EVT-124`](EVT-124.md#EVT-124) | 初期表示 — 編集モード | [UC-020](../../../01_requirements/04_business_usecases/UC-020.md#UC-020) |
| [`EVT-125`](EVT-125.md#EVT-125) | メールアドレスを入力 | [UC-019](../../../01_requirements/04_business_usecases/UC-019.md#UC-019) |
| [`EVT-126`](EVT-126.md#EVT-126) | 「招待メールを送信する」を押下 | [UC-019](../../../01_requirements/04_business_usecases/UC-019.md#UC-019) |
| [`EVT-127`](EVT-127.md#EVT-127) | 「招待メールを再送する」を押下 | [UC-019](../../../01_requirements/04_business_usecases/UC-019.md#UC-019) |
| [`EVT-128`](EVT-128.md#EVT-128) | 「変更を保存する」を押下 | [UC-020](../../../01_requirements/04_business_usecases/UC-020.md#UC-020) |
| [`EVT-129`](EVT-129.md#EVT-129) | 「プロジェクトから外す」を押下 | [UC-021](../../../01_requirements/04_business_usecases/UC-021.md#UC-021) |
| [`EVT-130`](EVT-130.md#EVT-130) | 割当解除の確認ダイアログで「外す」を押下 | [UC-021](../../../01_requirements/04_business_usecases/UC-021.md#UC-021) |
| [`EVT-131`](EVT-131.md#EVT-131) | 「×」を押下してモーダルを閉じる | [UC-020](../../../01_requirements/04_business_usecases/UC-020.md#UC-020) |
| [`EVT-132`](EVT-132.md#EVT-132) | 「キャンセル」を押下 | [UC-020](../../../01_requirements/04_business_usecases/UC-020.md#UC-020) |

### <span id="SCR-015"></span>SCR-015 利用規約閲覧

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-133`](EVT-133.md#EVT-133) | 初期表示 | [UC-011](../../../01_requirements/04_business_usecases/UC-011.md#UC-011) |
| [`EVT-134`](EVT-134.md#EVT-134) | 「再同意へ」リンクを押下 | [UC-011](../../../01_requirements/04_business_usecases/UC-011.md#UC-011) |
| [`EVT-135`](EVT-135.md#EVT-135) | 「同意して続ける」を押下 | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |

### <span id="SCR-016"></span>SCR-016 お知らせ一覧

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-136`](EVT-136.md#EVT-136) | 初期表示 | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-137`](EVT-137.md#EVT-137) | クイックフィルタチップを選択 | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-138`](EVT-138.md#EVT-138) | 「すべてクリア」を押下 | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-139`](EVT-139.md#EVT-139) | 詳細フィルタを適用 | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-140`](EVT-140.md#EVT-140) | 行を選択 | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-141`](EVT-141.md#EVT-141) | お知らせ ID リンクを押下 | [UC-047](../../../01_requirements/04_business_usecases/UC-047.md#UC-047) |
| [`EVT-142`](EVT-142.md#EVT-142) | 「既読化する」を押下 | [UC-047](../../../01_requirements/04_business_usecases/UC-047.md#UC-047) |
| [`EVT-143`](EVT-143.md#EVT-143) | 「表示中の未読を既読化」を押下 | [UC-047](../../../01_requirements/04_business_usecases/UC-047.md#UC-047) |
| [`EVT-144`](EVT-144.md#EVT-144) | 「すべての未読を既読化」を押下 | [UC-047](../../../01_requirements/04_business_usecases/UC-047.md#UC-047) |
| [`EVT-145`](EVT-145.md#EVT-145) | 「次のページ」を押下 | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-146`](EVT-146.md#EVT-146) | 「選択を解除」を押下 | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |

### <span id="SCR-017"></span>SCR-017 お知らせ詳細

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-147`](EVT-147.md#EVT-147) | 初期表示 | [UC-046](../../../01_requirements/04_business_usecases/UC-046.md#UC-046) |
| [`EVT-148`](EVT-148.md#EVT-148) | 「一覧へ戻る」を押下 | [UC-046](../../../01_requirements/04_business_usecases/UC-046.md#UC-046) |
| [`EVT-149`](EVT-149.md#EVT-149) | 「前のお知らせ」を押下 | [UC-046](../../../01_requirements/04_business_usecases/UC-046.md#UC-046) |
| [`EVT-150`](EVT-150.md#EVT-150) | 「次のお知らせ」を押下 | [UC-046](../../../01_requirements/04_business_usecases/UC-046.md#UC-046) |

### <span id="SCR-018"></span>SCR-018 メール確認

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-151`](EVT-151.md#EVT-151) | 初期表示 | [UC-003](../../../01_requirements/04_business_usecases/UC-003.md#UC-003) |
| [`EVT-152`](EVT-152.md#EVT-152) | 「メールを再送する」を押下 | [UC-003](../../../01_requirements/04_business_usecases/UC-003.md#UC-003) |
| [`EVT-153`](EVT-153.md#EVT-153) | 「メールアドレスを変更する」を押下 | [UC-003](../../../01_requirements/04_business_usecases/UC-003.md#UC-003) |
| [`EVT-154`](EVT-154.md#EVT-154) | 「新規登録からやり直す」を押下 | [UC-003](../../../01_requirements/04_business_usecases/UC-003.md#UC-003) |
| [`EVT-155`](EVT-155.md#EVT-155) | 「ログインする」を押下 | [UC-003](../../../01_requirements/04_business_usecases/UC-003.md#UC-003) |

### <span id="SCR-019"></span>SCR-019 退会申請

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-156`](EVT-156.md#EVT-156) | 初期表示 | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-157`](EVT-157.md#EVT-157) | 退会理由を入力 | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-158`](EVT-158.md#EVT-158) | 「退会を申請する」を押下 | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-159`](EVT-159.md#EVT-159) | 確認ダイアログの「OK」を押下 | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-160`](EVT-160.md#EVT-160) | 「個人設定へ戻る」を押下 | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-161`](EVT-161.md#EVT-161) | 契約名を入力 | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-162`](EVT-162.md#EVT-162) | パスワードを入力(再認証) | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-163`](EVT-163.md#EVT-163) | 「キャンセル」を押下 | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |

### <span id="SCR-020"></span>SCR-020 規約再同意割込み

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-164`](EVT-164.md#EVT-164) | 初期表示 | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |
| [`EVT-165`](EVT-165.md#EVT-165) | 「利用規約」リンクを押下 | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |
| [`EVT-166`](EVT-166.md#EVT-166) | 「プライバシーポリシー」リンクを押下 | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |
| [`EVT-167`](EVT-167.md#EVT-167) | 利用規約同意をチェック | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |
| [`EVT-168`](EVT-168.md#EVT-168) | プライバシーポリシー同意をチェック | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |
| [`EVT-169`](EVT-169.md#EVT-169) | 「同意して続行する」を押下 | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |

### <span id="SCR-021"></span>SCR-021 利用状況

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-170`](EVT-170.md#EVT-170) | 初期表示 | [UC-036](../../../01_requirements/04_business_usecases/UC-036.md#UC-036) |
| [`EVT-171`](EVT-171.md#EVT-171) | 「請求を確認」を押下 | [UC-036](../../../01_requirements/04_business_usecases/UC-036.md#UC-036) |
| [`EVT-172`](EVT-172.md#EVT-172) | 「プロジェクトへ」を押下 | [UC-036](../../../01_requirements/04_business_usecases/UC-036.md#UC-036) |

### <span id="SCR-022"></span>SCR-022 個人設定

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-173`](EVT-173.md#EVT-173) | 初期表示 | [UC-008](../../../01_requirements/04_business_usecases/UC-008.md#UC-008) |
| [`EVT-174`](EVT-174.md#EVT-174) | タブを押下(プロフィール / セキュリティ / 参加プロジェクト) | [UC-008](../../../01_requirements/04_business_usecases/UC-008.md#UC-008) |
| [`EVT-175`](EVT-175.md#EVT-175) | 表示名を入力 | [UC-009](../../../01_requirements/04_business_usecases/UC-009.md#UC-009) |
| [`EVT-176`](EVT-176.md#EVT-176) | メールアドレスを入力 | [UC-009](../../../01_requirements/04_business_usecases/UC-009.md#UC-009) |
| [`EVT-177`](EVT-177.md#EVT-177) | 「保存する」を押下(プロフィール) | [UC-009](../../../01_requirements/04_business_usecases/UC-009.md#UC-009) |
| [`EVT-178`](EVT-178.md#EVT-178) | 「パスワードを変更する」を押下 | [UC-010](../../../01_requirements/04_business_usecases/UC-010.md#UC-010) |
| [`EVT-179`](EVT-179.md#EVT-179) | 「変更を破棄」を押下 | [UC-009](../../../01_requirements/04_business_usecases/UC-009.md#UC-009) |
| [`EVT-180`](EVT-180.md#EVT-180) | 参加プロジェクト名リンクを押下 | [UC-008](../../../01_requirements/04_business_usecases/UC-008.md#UC-008) |

### <span id="SCR-023"></span>SCR-023 メンバーアカウント有効化

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-181`](EVT-181.md#EVT-181) | 初期表示 | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-182`](EVT-182.md#EVT-182) | 氏名(表示名)を入力 | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-183`](EVT-183.md#EVT-183) | 初回パスワードを入力 | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-184`](EVT-184.md#EVT-184) | パスワード(確認)を入力 | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-185`](EVT-185.md#EVT-185) | 「利用規約に同意します」をチェック | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-186`](EVT-186.md#EVT-186) | 利用規約の「全文を見る」を押下 | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-187`](EVT-187.md#EVT-187) | 「プライバシーポリシーに同意します」をチェック | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-188`](EVT-188.md#EVT-188) | プライバシーポリシーの「全文を見る」を押下 | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-189`](EVT-189.md#EVT-189) | Turnstile を実行 | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-190`](EVT-190.md#EVT-190) | 「登録を完了する」を押下 | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-191`](EVT-191.md#EVT-191) | 「ログインする」を押下(完了画面) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-192`](EVT-192.md#EVT-192) | 「ログインへ」を押下(トークン無効 / 期限切れエラー画面) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-193`](EVT-193.md#EVT-193) | 「ログインへ」を押下(既使用エラー画面) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |

### <span id="SCR-024"></span>SCR-024 プロジェクト連絡先メール確認完了

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-194`](EVT-194.md#EVT-194) | 初期表示 | [UC-007](../../../01_requirements/04_business_usecases/UC-007.md#UC-007) |
| [`EVT-195`](EVT-195.md#EVT-195) | 「閉じる」を押下 | [UC-007](../../../01_requirements/04_business_usecases/UC-007.md#UC-007) |

### <span id="SCR-025"></span>SCR-025 プライバシーポリシー閲覧

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-196`](EVT-196.md#EVT-196) | 初期表示 | [UC-012](../../../01_requirements/04_business_usecases/UC-012.md#UC-012) |
| [`EVT-197`](EVT-197.md#EVT-197) | 「再同意する」を押下(未同意バッジのリンク) | [UC-012](../../../01_requirements/04_business_usecases/UC-012.md#UC-012) |
| [`EVT-198`](EVT-198.md#EVT-198) | 「利用規約」を押下 | [UC-011](../../../01_requirements/04_business_usecases/UC-011.md#UC-011) |

### <span id="SCR-026"></span>SCR-026 利用量と上限(プロジェクト単位)

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-199`](EVT-199.md#EVT-199) | 初期表示 | [UC-034](../../../01_requirements/04_business_usecases/UC-034.md#UC-034) |
| [`EVT-200`](EVT-200.md#EVT-200) | 「アラート設定」を押下 | [UC-034](../../../01_requirements/04_business_usecases/UC-034.md#UC-034) |
| [`EVT-201`](EVT-201.md#EVT-201) | URL へ直接アクセス(権限不足) | [UC-048](../../../01_requirements/04_business_usecases/UC-048.md#UC-048) |

### <span id="SCR-027"></span>SCR-027 質問数上限設定モーダル

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-202`](EVT-202.md#EVT-202) | 初期表示 | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) |
| [`EVT-203`](EVT-203.md#EVT-203) | 上限設定トグルを切り替え | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) |
| [`EVT-204`](EVT-204.md#EVT-204) | 「今月の利用上限」を入力 | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) |
| [`EVT-205`](EVT-205.md#EVT-205) | アラート閾値をチェック | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) |
| [`EVT-206`](EVT-206.md#EVT-206) | 「保存」を押下 | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) |
| [`EVT-207`](EVT-207.md#EVT-207) | 「キャンセル」を押下 | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) |

### <span id="SCR-028"></span>SCR-028 請求

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-208`](EVT-208.md#EVT-208) | 初期表示 | [UC-037](../../../01_requirements/04_business_usecases/UC-037.md#UC-037) |
| [`EVT-209`](EVT-209.md#EVT-209) | 「支払方法を変更」を押下 | [UC-038](../../../01_requirements/04_business_usecases/UC-038.md#UC-038) |
| [`EVT-210`](EVT-210.md#EVT-210) | 「領収書」リンクを押下 | [UC-037](../../../01_requirements/04_business_usecases/UC-037.md#UC-037) |
| [`EVT-211`](EVT-211.md#EVT-211) | 「利用量と上限を確認」リンクを押下 | [UC-037](../../../01_requirements/04_business_usecases/UC-037.md#UC-037) |
| [`EVT-212`](EVT-212.md#EVT-212) | 「退会手続きへ」リンクを押下 | [UC-037](../../../01_requirements/04_business_usecases/UC-037.md#UC-037) |
| [`EVT-213`](EVT-213.md#EVT-213) | 「支払い方法を登録」を押下(バナー CTA) | [UC-038](../../../01_requirements/04_business_usecases/UC-038.md#UC-038) |
| [`EVT-214`](EVT-214.md#EVT-214) | 「プランを変更」を押下 | [UC-039](../../../01_requirements/04_business_usecases/UC-039.md#UC-039) |

### <span id="SCR-029"></span>SCR-029 設定

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-215`](EVT-215.md#EVT-215) | 初期表示 | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) |
| [`EVT-216`](EVT-216.md#EVT-216) | 請求・重要通知メールを入力 | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) |
| [`EVT-217`](EVT-217.md#EVT-217) | 「変更を保存」を押下 | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) |
| [`EVT-218`](EVT-218.md#EVT-218) | 「退会手続きへ」を押下 | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) |
| [`EVT-219`](EVT-219.md#EVT-219) | 「請求」を押下 | [UC-037](../../../01_requirements/04_business_usecases/UC-037.md#UC-037) |
| [`EVT-220`](EVT-220.md#EVT-220) | タイムゾーンを選択 | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) |
| [`EVT-221`](EVT-221.md#EVT-221) | 「変更を破棄」を押下 | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) |

### <span id="SCR-030"></span>SCR-030 エンドユーザー向け FAQ ウィジェット

| EVT-ID | イベント名 | 対応業務UC |
|---|---|---|
| [`EVT-222`](EVT-222.md#EVT-222) | 初期表示 | [UC-042](../../../01_requirements/04_business_usecases/UC-042.md#UC-042) |
| [`EVT-223`](EVT-223.md#EVT-223) | ランチャーバッジを押下 | [UC-042](../../../01_requirements/04_business_usecases/UC-042.md#UC-042) |
| [`EVT-224`](EVT-224.md#EVT-224) | ヘッダーの閉じるボタンを押下 | [UC-042](../../../01_requirements/04_business_usecases/UC-042.md#UC-042) |
| [`EVT-225`](EVT-225.md#EVT-225) | 質問を入力 | [UC-043](../../../01_requirements/04_business_usecases/UC-043.md#UC-043) |
| [`EVT-226`](EVT-226.md#EVT-226) | 「送信」を押下 | [UC-043](../../../01_requirements/04_business_usecases/UC-043.md#UC-043) |
| [`EVT-227`](EVT-227.md#EVT-227) | AI 回答(未解決)を受信 | [UC-044](../../../01_requirements/04_business_usecases/UC-044.md#UC-044) |
| [`EVT-228`](EVT-228.md#EVT-228) | 受付制限(429)を受信 | [UC-044](../../../01_requirements/04_business_usecases/UC-044.md#UC-044) |
| [`EVT-229`](EVT-229.md#EVT-229) | 処理エラーを受信 | [UC-044](../../../01_requirements/04_business_usecases/UC-044.md#UC-044) |

## 2. EVT ↔ 業務UC 対応表

画面イベント `EVT-NNN` と業務ユースケース `UC-PPP` の 1:1 対応です。

| EVT-ID | 対応画面 | 対応業務UC |
|---|---|---|
| [`EVT-001`](EVT-001.md#EVT-001) | [SCR-001](../01_screens/SCR-001.md#SCR-001) | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-002`](EVT-002.md#EVT-002) | [SCR-001](../01_screens/SCR-001.md#SCR-001) | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-003`](EVT-003.md#EVT-003) | [SCR-001](../01_screens/SCR-001.md#SCR-001) | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-004`](EVT-004.md#EVT-004) | [SCR-001](../01_screens/SCR-001.md#SCR-001) | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-005`](EVT-005.md#EVT-005) | [SCR-001](../01_screens/SCR-001.md#SCR-001) | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) |
| [`EVT-006`](EVT-006.md#EVT-006) | [SCR-001](../01_screens/SCR-001.md#SCR-001) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-007`](EVT-007.md#EVT-007) | [SCR-002](../01_screens/SCR-002.md#SCR-002) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-008`](EVT-008.md#EVT-008) | [SCR-002](../01_screens/SCR-002.md#SCR-002) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-009`](EVT-009.md#EVT-009) | [SCR-002](../01_screens/SCR-002.md#SCR-002) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-010`](EVT-010.md#EVT-010) | [SCR-002](../01_screens/SCR-002.md#SCR-002) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-011`](EVT-011.md#EVT-011) | [SCR-002](../01_screens/SCR-002.md#SCR-002) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-012`](EVT-012.md#EVT-012) | [SCR-002](../01_screens/SCR-002.md#SCR-002) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-013`](EVT-013.md#EVT-013) | [SCR-002](../01_screens/SCR-002.md#SCR-002) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-014`](EVT-014.md#EVT-014) | [SCR-002](../01_screens/SCR-002.md#SCR-002) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-015`](EVT-015.md#EVT-015) | [SCR-002](../01_screens/SCR-002.md#SCR-002) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-016`](EVT-016.md#EVT-016) | [SCR-002](../01_screens/SCR-002.md#SCR-002) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-017`](EVT-017.md#EVT-017) | [SCR-002](../01_screens/SCR-002.md#SCR-002) | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-018`](EVT-018.md#EVT-018) | [SCR-002](../01_screens/SCR-002.md#SCR-002) | [UC-002](../../../01_requirements/04_business_usecases/UC-002.md#UC-002) |
| [`EVT-019`](EVT-019.md#EVT-019) | [SCR-003](../01_screens/SCR-003.md#SCR-003) | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) |
| [`EVT-020`](EVT-020.md#EVT-020) | [SCR-003](../01_screens/SCR-003.md#SCR-003) | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) |
| [`EVT-021`](EVT-021.md#EVT-021) | [SCR-003](../01_screens/SCR-003.md#SCR-003) | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) |
| [`EVT-022`](EVT-022.md#EVT-022) | [SCR-003](../01_screens/SCR-003.md#SCR-003) | [UC-005](../../../01_requirements/04_business_usecases/UC-005.md#UC-005) |
| [`EVT-023`](EVT-023.md#EVT-023) | [SCR-003](../01_screens/SCR-003.md#SCR-003) | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) |
| [`EVT-024`](EVT-024.md#EVT-024) | [SCR-003](../01_screens/SCR-003.md#SCR-003) | [UC-005](../../../01_requirements/04_business_usecases/UC-005.md#UC-005) |
| [`EVT-025`](EVT-025.md#EVT-025) | [SCR-003](../01_screens/SCR-003.md#SCR-003) | [UC-005](../../../01_requirements/04_business_usecases/UC-005.md#UC-005) |
| [`EVT-026`](EVT-026.md#EVT-026) | [SCR-003](../01_screens/SCR-003.md#SCR-003) | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-027`](EVT-027.md#EVT-027) | [SCR-003](../01_screens/SCR-003.md#SCR-003) | [UC-004](../../../01_requirements/04_business_usecases/UC-004.md#UC-004) |
| [`EVT-028`](EVT-028.md#EVT-028) | [SCR-004](../01_screens/SCR-004.md#SCR-004) | [UC-014](../../../01_requirements/04_business_usecases/UC-014.md#UC-014) |
| [`EVT-029`](EVT-029.md#EVT-029) | [SCR-004](../01_screens/SCR-004.md#SCR-004) | [UC-014](../../../01_requirements/04_business_usecases/UC-014.md#UC-014) |
| [`EVT-030`](EVT-030.md#EVT-030) | [SCR-004](../01_screens/SCR-004.md#SCR-004) | [UC-014](../../../01_requirements/04_business_usecases/UC-014.md#UC-014) |
| [`EVT-031`](EVT-031.md#EVT-031) | [SCR-004](../01_screens/SCR-004.md#SCR-004) | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-032`](EVT-032.md#EVT-032) | [SCR-004](../01_screens/SCR-004.md#SCR-004) | [UC-014](../../../01_requirements/04_business_usecases/UC-014.md#UC-014) |
| [`EVT-033`](EVT-033.md#EVT-033) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) |
| [`EVT-034`](EVT-034.md#EVT-034) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-016](../../../01_requirements/04_business_usecases/UC-016.md#UC-016) |
| [`EVT-035`](EVT-035.md#EVT-035) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) |
| [`EVT-036`](EVT-036.md#EVT-036) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) |
| [`EVT-037`](EVT-037.md#EVT-037) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) |
| [`EVT-038`](EVT-038.md#EVT-038) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) |
| [`EVT-039`](EVT-039.md#EVT-039) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-016](../../../01_requirements/04_business_usecases/UC-016.md#UC-016) |
| [`EVT-040`](EVT-040.md#EVT-040) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-016](../../../01_requirements/04_business_usecases/UC-016.md#UC-016) |
| [`EVT-041`](EVT-041.md#EVT-041) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-017](../../../01_requirements/04_business_usecases/UC-017.md#UC-017) |
| [`EVT-042`](EVT-042.md#EVT-042) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-017](../../../01_requirements/04_business_usecases/UC-017.md#UC-017) |
| [`EVT-043`](EVT-043.md#EVT-043) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-016](../../../01_requirements/04_business_usecases/UC-016.md#UC-016) |
| [`EVT-044`](EVT-044.md#EVT-044) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-015](../../../01_requirements/04_business_usecases/UC-015.md#UC-015) |
| [`EVT-045`](EVT-045.md#EVT-045) | [SCR-005](../01_screens/SCR-005.md#SCR-005) | [UC-016](../../../01_requirements/04_business_usecases/UC-016.md#UC-016) |
| [`EVT-046`](EVT-046.md#EVT-046) | [SCR-006](../01_screens/SCR-006.md#SCR-006) | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-047`](EVT-047.md#EVT-047) | [SCR-006](../01_screens/SCR-006.md#SCR-006) | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-048`](EVT-048.md#EVT-048) | [SCR-006](../01_screens/SCR-006.md#SCR-006) | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-049`](EVT-049.md#EVT-049) | [SCR-006](../01_screens/SCR-006.md#SCR-006) | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-050`](EVT-050.md#EVT-050) | [SCR-006](../01_screens/SCR-006.md#SCR-006) | [UC-031](../../../01_requirements/04_business_usecases/UC-031.md#UC-031) |
| [`EVT-051`](EVT-051.md#EVT-051) | [SCR-006](../01_screens/SCR-006.md#SCR-006) | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-052`](EVT-052.md#EVT-052) | [SCR-006](../01_screens/SCR-006.md#SCR-006) | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-053`](EVT-053.md#EVT-053) | [SCR-006](../01_screens/SCR-006.md#SCR-006) | [UC-030](../../../01_requirements/04_business_usecases/UC-030.md#UC-030) |
| [`EVT-054`](EVT-054.md#EVT-054) | [SCR-007](../01_screens/SCR-007.md#SCR-007) | [UC-031](../../../01_requirements/04_business_usecases/UC-031.md#UC-031) |
| [`EVT-055`](EVT-055.md#EVT-055) | [SCR-007](../01_screens/SCR-007.md#SCR-007) | [UC-032](../../../01_requirements/04_business_usecases/UC-032.md#UC-032) |
| [`EVT-056`](EVT-056.md#EVT-056) | [SCR-007](../01_screens/SCR-007.md#SCR-007) | [UC-032](../../../01_requirements/04_business_usecases/UC-032.md#UC-032) |
| [`EVT-057`](EVT-057.md#EVT-057) | [SCR-007](../01_screens/SCR-007.md#SCR-007) | [UC-032](../../../01_requirements/04_business_usecases/UC-032.md#UC-032) |
| [`EVT-058`](EVT-058.md#EVT-058) | [SCR-007](../01_screens/SCR-007.md#SCR-007) | [UC-032](../../../01_requirements/04_business_usecases/UC-032.md#UC-032) |
| [`EVT-059`](EVT-059.md#EVT-059) | [SCR-007](../01_screens/SCR-007.md#SCR-007) | [UC-031](../../../01_requirements/04_business_usecases/UC-031.md#UC-031) |
| [`EVT-060`](EVT-060.md#EVT-060) | [SCR-007](../01_screens/SCR-007.md#SCR-007) | [UC-031](../../../01_requirements/04_business_usecases/UC-031.md#UC-031) |
| [`EVT-061`](EVT-061.md#EVT-061) | [SCR-007](../01_screens/SCR-007.md#SCR-007) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-062`](EVT-062.md#EVT-062) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) |
| [`EVT-063`](EVT-063.md#EVT-063) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) |
| [`EVT-064`](EVT-064.md#EVT-064) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) |
| [`EVT-065`](EVT-065.md#EVT-065) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) |
| [`EVT-066`](EVT-066.md#EVT-066) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) |
| [`EVT-067`](EVT-067.md#EVT-067) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-068`](EVT-068.md#EVT-068) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-069`](EVT-069.md#EVT-069) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-027](../../../01_requirements/04_business_usecases/UC-027.md#UC-027) |
| [`EVT-070`](EVT-070.md#EVT-070) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-027](../../../01_requirements/04_business_usecases/UC-027.md#UC-027) |
| [`EVT-071`](EVT-071.md#EVT-071) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-026](../../../01_requirements/04_business_usecases/UC-026.md#UC-026) |
| [`EVT-072`](EVT-072.md#EVT-072) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-024](../../../01_requirements/04_business_usecases/UC-024.md#UC-024) |
| [`EVT-073`](EVT-073.md#EVT-073) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-074`](EVT-074.md#EVT-074) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-029](../../../01_requirements/04_business_usecases/UC-029.md#UC-029) |
| [`EVT-075`](EVT-075.md#EVT-075) | [SCR-008](../01_screens/SCR-008.md#SCR-008) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-076`](EVT-076.md#EVT-076) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-077`](EVT-077.md#EVT-077) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-078`](EVT-078.md#EVT-078) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-079`](EVT-079.md#EVT-079) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-080`](EVT-080.md#EVT-080) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-081`](EVT-081.md#EVT-081) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-082`](EVT-082.md#EVT-082) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-083`](EVT-083.md#EVT-083) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-026](../../../01_requirements/04_business_usecases/UC-026.md#UC-026) |
| [`EVT-084`](EVT-084.md#EVT-084) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-026](../../../01_requirements/04_business_usecases/UC-026.md#UC-026) |
| [`EVT-085`](EVT-085.md#EVT-085) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-086`](EVT-086.md#EVT-086) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-087`](EVT-087.md#EVT-087) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-026](../../../01_requirements/04_business_usecases/UC-026.md#UC-026) |
| [`EVT-088`](EVT-088.md#EVT-088) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-089`](EVT-089.md#EVT-089) | [SCR-009](../01_screens/SCR-009.md#SCR-009) | [UC-025](../../../01_requirements/04_business_usecases/UC-025.md#UC-025) |
| [`EVT-090`](EVT-090.md#EVT-090) | [SCR-010](../01_screens/SCR-010.md#SCR-010) | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-091`](EVT-091.md#EVT-091) | [SCR-010](../01_screens/SCR-010.md#SCR-010) | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-092`](EVT-092.md#EVT-092) | [SCR-010](../01_screens/SCR-010.md#SCR-010) | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-093`](EVT-093.md#EVT-093) | [SCR-010](../01_screens/SCR-010.md#SCR-010) | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-094`](EVT-094.md#EVT-094) | [SCR-010](../01_screens/SCR-010.md#SCR-010) | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-095`](EVT-095.md#EVT-095) | [SCR-010](../01_screens/SCR-010.md#SCR-010) | [UC-028](../../../01_requirements/04_business_usecases/UC-028.md#UC-028) |
| [`EVT-096`](EVT-096.md#EVT-096) | [SCR-011](../01_screens/SCR-011.md#SCR-011) | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-097`](EVT-097.md#EVT-097) | [SCR-011](../01_screens/SCR-011.md#SCR-011) | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-098`](EVT-098.md#EVT-098) | [SCR-011](../01_screens/SCR-011.md#SCR-011) | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-099`](EVT-099.md#EVT-099) | [SCR-011](../01_screens/SCR-011.md#SCR-011) | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-100`](EVT-100.md#EVT-100) | [SCR-011](../01_screens/SCR-011.md#SCR-011) | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-101`](EVT-101.md#EVT-101) | [SCR-011](../01_screens/SCR-011.md#SCR-011) | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-102`](EVT-102.md#EVT-102) | [SCR-011](../01_screens/SCR-011.md#SCR-011) | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-103`](EVT-103.md#EVT-103) | [SCR-011](../01_screens/SCR-011.md#SCR-011) | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-104`](EVT-104.md#EVT-104) | [SCR-011](../01_screens/SCR-011.md#SCR-011) | [UC-041](../../../01_requirements/04_business_usecases/UC-041.md#UC-041) |
| [`EVT-105`](EVT-105.md#EVT-105) | [SCR-011](../01_screens/SCR-011.md#SCR-011) | [UC-040](../../../01_requirements/04_business_usecases/UC-040.md#UC-040) |
| [`EVT-106`](EVT-106.md#EVT-106) | [SCR-011](../01_screens/SCR-011.md#SCR-011) | [UC-001](../../../01_requirements/04_business_usecases/UC-001.md#UC-001) |
| [`EVT-107`](EVT-107.md#EVT-107) | [SCR-012](../01_screens/SCR-012.md#SCR-012) | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-108`](EVT-108.md#EVT-108) | [SCR-012](../01_screens/SCR-012.md#SCR-012) | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-109`](EVT-109.md#EVT-109) | [SCR-012](../01_screens/SCR-012.md#SCR-012) | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-110`](EVT-110.md#EVT-110) | [SCR-012](../01_screens/SCR-012.md#SCR-012) | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-111`](EVT-111.md#EVT-111) | [SCR-012](../01_screens/SCR-012.md#SCR-012) | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-112`](EVT-112.md#EVT-112) | [SCR-012](../01_screens/SCR-012.md#SCR-012) | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-113`](EVT-113.md#EVT-113) | [SCR-012](../01_screens/SCR-012.md#SCR-012) | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-114`](EVT-114.md#EVT-114) | [SCR-012](../01_screens/SCR-012.md#SCR-012) | [UC-033](../../../01_requirements/04_business_usecases/UC-033.md#UC-033) |
| [`EVT-115`](EVT-115.md#EVT-115) | [SCR-013](../01_screens/SCR-013.md#SCR-013) | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) |
| [`EVT-116`](EVT-116.md#EVT-116) | [SCR-013](../01_screens/SCR-013.md#SCR-013) | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) |
| [`EVT-117`](EVT-117.md#EVT-117) | [SCR-013](../01_screens/SCR-013.md#SCR-013) | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) |
| [`EVT-118`](EVT-118.md#EVT-118) | [SCR-013](../01_screens/SCR-013.md#SCR-013) | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) |
| [`EVT-119`](EVT-119.md#EVT-119) | [SCR-013](../01_screens/SCR-013.md#SCR-013) | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) |
| [`EVT-120`](EVT-120.md#EVT-120) | [SCR-013](../01_screens/SCR-013.md#SCR-013) | [UC-018](../../../01_requirements/04_business_usecases/UC-018.md#UC-018) |
| [`EVT-121`](EVT-121.md#EVT-121) | [SCR-013](../01_screens/SCR-013.md#SCR-013) | [UC-048](../../../01_requirements/04_business_usecases/UC-048.md#UC-048) |
| [`EVT-122`](EVT-122.md#EVT-122) | [SCR-013](../01_screens/SCR-013.md#SCR-013) | [UC-048](../../../01_requirements/04_business_usecases/UC-048.md#UC-048) |
| [`EVT-123`](EVT-123.md#EVT-123) | [SCR-014](../01_screens/SCR-014.md#SCR-014) | [UC-019](../../../01_requirements/04_business_usecases/UC-019.md#UC-019) |
| [`EVT-124`](EVT-124.md#EVT-124) | [SCR-014](../01_screens/SCR-014.md#SCR-014) | [UC-020](../../../01_requirements/04_business_usecases/UC-020.md#UC-020) |
| [`EVT-125`](EVT-125.md#EVT-125) | [SCR-014](../01_screens/SCR-014.md#SCR-014) | [UC-019](../../../01_requirements/04_business_usecases/UC-019.md#UC-019) |
| [`EVT-126`](EVT-126.md#EVT-126) | [SCR-014](../01_screens/SCR-014.md#SCR-014) | [UC-019](../../../01_requirements/04_business_usecases/UC-019.md#UC-019) |
| [`EVT-127`](EVT-127.md#EVT-127) | [SCR-014](../01_screens/SCR-014.md#SCR-014) | [UC-019](../../../01_requirements/04_business_usecases/UC-019.md#UC-019) |
| [`EVT-128`](EVT-128.md#EVT-128) | [SCR-014](../01_screens/SCR-014.md#SCR-014) | [UC-020](../../../01_requirements/04_business_usecases/UC-020.md#UC-020) |
| [`EVT-129`](EVT-129.md#EVT-129) | [SCR-014](../01_screens/SCR-014.md#SCR-014) | [UC-021](../../../01_requirements/04_business_usecases/UC-021.md#UC-021) |
| [`EVT-130`](EVT-130.md#EVT-130) | [SCR-014](../01_screens/SCR-014.md#SCR-014) | [UC-021](../../../01_requirements/04_business_usecases/UC-021.md#UC-021) |
| [`EVT-131`](EVT-131.md#EVT-131) | [SCR-014](../01_screens/SCR-014.md#SCR-014) | [UC-020](../../../01_requirements/04_business_usecases/UC-020.md#UC-020) |
| [`EVT-132`](EVT-132.md#EVT-132) | [SCR-014](../01_screens/SCR-014.md#SCR-014) | [UC-020](../../../01_requirements/04_business_usecases/UC-020.md#UC-020) |
| [`EVT-133`](EVT-133.md#EVT-133) | [SCR-015](../01_screens/SCR-015.md#SCR-015) | [UC-011](../../../01_requirements/04_business_usecases/UC-011.md#UC-011) |
| [`EVT-134`](EVT-134.md#EVT-134) | [SCR-015](../01_screens/SCR-015.md#SCR-015) | [UC-011](../../../01_requirements/04_business_usecases/UC-011.md#UC-011) |
| [`EVT-135`](EVT-135.md#EVT-135) | [SCR-015](../01_screens/SCR-015.md#SCR-015) | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |
| [`EVT-136`](EVT-136.md#EVT-136) | [SCR-016](../01_screens/SCR-016.md#SCR-016) | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-137`](EVT-137.md#EVT-137) | [SCR-016](../01_screens/SCR-016.md#SCR-016) | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-138`](EVT-138.md#EVT-138) | [SCR-016](../01_screens/SCR-016.md#SCR-016) | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-139`](EVT-139.md#EVT-139) | [SCR-016](../01_screens/SCR-016.md#SCR-016) | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-140`](EVT-140.md#EVT-140) | [SCR-016](../01_screens/SCR-016.md#SCR-016) | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-141`](EVT-141.md#EVT-141) | [SCR-016](../01_screens/SCR-016.md#SCR-016) | [UC-047](../../../01_requirements/04_business_usecases/UC-047.md#UC-047) |
| [`EVT-142`](EVT-142.md#EVT-142) | [SCR-016](../01_screens/SCR-016.md#SCR-016) | [UC-047](../../../01_requirements/04_business_usecases/UC-047.md#UC-047) |
| [`EVT-143`](EVT-143.md#EVT-143) | [SCR-016](../01_screens/SCR-016.md#SCR-016) | [UC-047](../../../01_requirements/04_business_usecases/UC-047.md#UC-047) |
| [`EVT-144`](EVT-144.md#EVT-144) | [SCR-016](../01_screens/SCR-016.md#SCR-016) | [UC-047](../../../01_requirements/04_business_usecases/UC-047.md#UC-047) |
| [`EVT-145`](EVT-145.md#EVT-145) | [SCR-016](../01_screens/SCR-016.md#SCR-016) | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-146`](EVT-146.md#EVT-146) | [SCR-016](../01_screens/SCR-016.md#SCR-016) | [UC-045](../../../01_requirements/04_business_usecases/UC-045.md#UC-045) |
| [`EVT-147`](EVT-147.md#EVT-147) | [SCR-017](../01_screens/SCR-017.md#SCR-017) | [UC-046](../../../01_requirements/04_business_usecases/UC-046.md#UC-046) |
| [`EVT-148`](EVT-148.md#EVT-148) | [SCR-017](../01_screens/SCR-017.md#SCR-017) | [UC-046](../../../01_requirements/04_business_usecases/UC-046.md#UC-046) |
| [`EVT-149`](EVT-149.md#EVT-149) | [SCR-017](../01_screens/SCR-017.md#SCR-017) | [UC-046](../../../01_requirements/04_business_usecases/UC-046.md#UC-046) |
| [`EVT-150`](EVT-150.md#EVT-150) | [SCR-017](../01_screens/SCR-017.md#SCR-017) | [UC-046](../../../01_requirements/04_business_usecases/UC-046.md#UC-046) |
| [`EVT-151`](EVT-151.md#EVT-151) | [SCR-018](../01_screens/SCR-018.md#SCR-018) | [UC-003](../../../01_requirements/04_business_usecases/UC-003.md#UC-003) |
| [`EVT-152`](EVT-152.md#EVT-152) | [SCR-018](../01_screens/SCR-018.md#SCR-018) | [UC-003](../../../01_requirements/04_business_usecases/UC-003.md#UC-003) |
| [`EVT-153`](EVT-153.md#EVT-153) | [SCR-018](../01_screens/SCR-018.md#SCR-018) | [UC-003](../../../01_requirements/04_business_usecases/UC-003.md#UC-003) |
| [`EVT-154`](EVT-154.md#EVT-154) | [SCR-018](../01_screens/SCR-018.md#SCR-018) | [UC-003](../../../01_requirements/04_business_usecases/UC-003.md#UC-003) |
| [`EVT-155`](EVT-155.md#EVT-155) | [SCR-018](../01_screens/SCR-018.md#SCR-018) | [UC-003](../../../01_requirements/04_business_usecases/UC-003.md#UC-003) |
| [`EVT-156`](EVT-156.md#EVT-156) | [SCR-019](../01_screens/SCR-019.md#SCR-019) | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-157`](EVT-157.md#EVT-157) | [SCR-019](../01_screens/SCR-019.md#SCR-019) | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-158`](EVT-158.md#EVT-158) | [SCR-019](../01_screens/SCR-019.md#SCR-019) | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-159`](EVT-159.md#EVT-159) | [SCR-019](../01_screens/SCR-019.md#SCR-019) | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-160`](EVT-160.md#EVT-160) | [SCR-019](../01_screens/SCR-019.md#SCR-019) | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-161`](EVT-161.md#EVT-161) | [SCR-019](../01_screens/SCR-019.md#SCR-019) | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-162`](EVT-162.md#EVT-162) | [SCR-019](../01_screens/SCR-019.md#SCR-019) | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-163`](EVT-163.md#EVT-163) | [SCR-019](../01_screens/SCR-019.md#SCR-019) | [UC-023](../../../01_requirements/04_business_usecases/UC-023.md#UC-023) |
| [`EVT-164`](EVT-164.md#EVT-164) | [SCR-020](../01_screens/SCR-020.md#SCR-020) | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |
| [`EVT-165`](EVT-165.md#EVT-165) | [SCR-020](../01_screens/SCR-020.md#SCR-020) | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |
| [`EVT-166`](EVT-166.md#EVT-166) | [SCR-020](../01_screens/SCR-020.md#SCR-020) | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |
| [`EVT-167`](EVT-167.md#EVT-167) | [SCR-020](../01_screens/SCR-020.md#SCR-020) | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |
| [`EVT-168`](EVT-168.md#EVT-168) | [SCR-020](../01_screens/SCR-020.md#SCR-020) | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |
| [`EVT-169`](EVT-169.md#EVT-169) | [SCR-020](../01_screens/SCR-020.md#SCR-020) | [UC-013](../../../01_requirements/04_business_usecases/UC-013.md#UC-013) |
| [`EVT-170`](EVT-170.md#EVT-170) | [SCR-021](../01_screens/SCR-021.md#SCR-021) | [UC-036](../../../01_requirements/04_business_usecases/UC-036.md#UC-036) |
| [`EVT-171`](EVT-171.md#EVT-171) | [SCR-021](../01_screens/SCR-021.md#SCR-021) | [UC-036](../../../01_requirements/04_business_usecases/UC-036.md#UC-036) |
| [`EVT-172`](EVT-172.md#EVT-172) | [SCR-021](../01_screens/SCR-021.md#SCR-021) | [UC-036](../../../01_requirements/04_business_usecases/UC-036.md#UC-036) |
| [`EVT-173`](EVT-173.md#EVT-173) | [SCR-022](../01_screens/SCR-022.md#SCR-022) | [UC-008](../../../01_requirements/04_business_usecases/UC-008.md#UC-008) |
| [`EVT-174`](EVT-174.md#EVT-174) | [SCR-022](../01_screens/SCR-022.md#SCR-022) | [UC-008](../../../01_requirements/04_business_usecases/UC-008.md#UC-008) |
| [`EVT-175`](EVT-175.md#EVT-175) | [SCR-022](../01_screens/SCR-022.md#SCR-022) | [UC-009](../../../01_requirements/04_business_usecases/UC-009.md#UC-009) |
| [`EVT-176`](EVT-176.md#EVT-176) | [SCR-022](../01_screens/SCR-022.md#SCR-022) | [UC-009](../../../01_requirements/04_business_usecases/UC-009.md#UC-009) |
| [`EVT-177`](EVT-177.md#EVT-177) | [SCR-022](../01_screens/SCR-022.md#SCR-022) | [UC-009](../../../01_requirements/04_business_usecases/UC-009.md#UC-009) |
| [`EVT-178`](EVT-178.md#EVT-178) | [SCR-022](../01_screens/SCR-022.md#SCR-022) | [UC-010](../../../01_requirements/04_business_usecases/UC-010.md#UC-010) |
| [`EVT-179`](EVT-179.md#EVT-179) | [SCR-022](../01_screens/SCR-022.md#SCR-022) | [UC-009](../../../01_requirements/04_business_usecases/UC-009.md#UC-009) |
| [`EVT-180`](EVT-180.md#EVT-180) | [SCR-022](../01_screens/SCR-022.md#SCR-022) | [UC-008](../../../01_requirements/04_business_usecases/UC-008.md#UC-008) |
| [`EVT-181`](EVT-181.md#EVT-181) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-182`](EVT-182.md#EVT-182) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-183`](EVT-183.md#EVT-183) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-184`](EVT-184.md#EVT-184) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-185`](EVT-185.md#EVT-185) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-186`](EVT-186.md#EVT-186) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-187`](EVT-187.md#EVT-187) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-188`](EVT-188.md#EVT-188) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-189`](EVT-189.md#EVT-189) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-190`](EVT-190.md#EVT-190) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-191`](EVT-191.md#EVT-191) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-192`](EVT-192.md#EVT-192) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-193`](EVT-193.md#EVT-193) | [SCR-023](../01_screens/SCR-023.md#SCR-023) | [UC-006](../../../01_requirements/04_business_usecases/UC-006.md#UC-006) |
| [`EVT-194`](EVT-194.md#EVT-194) | [SCR-024](../01_screens/SCR-024.md#SCR-024) | [UC-007](../../../01_requirements/04_business_usecases/UC-007.md#UC-007) |
| [`EVT-195`](EVT-195.md#EVT-195) | [SCR-024](../01_screens/SCR-024.md#SCR-024) | [UC-007](../../../01_requirements/04_business_usecases/UC-007.md#UC-007) |
| [`EVT-196`](EVT-196.md#EVT-196) | [SCR-025](../01_screens/SCR-025.md#SCR-025) | [UC-012](../../../01_requirements/04_business_usecases/UC-012.md#UC-012) |
| [`EVT-197`](EVT-197.md#EVT-197) | [SCR-025](../01_screens/SCR-025.md#SCR-025) | [UC-012](../../../01_requirements/04_business_usecases/UC-012.md#UC-012) |
| [`EVT-198`](EVT-198.md#EVT-198) | [SCR-025](../01_screens/SCR-025.md#SCR-025) | [UC-011](../../../01_requirements/04_business_usecases/UC-011.md#UC-011) |
| [`EVT-199`](EVT-199.md#EVT-199) | [SCR-026](../01_screens/SCR-026.md#SCR-026) | [UC-034](../../../01_requirements/04_business_usecases/UC-034.md#UC-034) |
| [`EVT-200`](EVT-200.md#EVT-200) | [SCR-026](../01_screens/SCR-026.md#SCR-026) | [UC-034](../../../01_requirements/04_business_usecases/UC-034.md#UC-034) |
| [`EVT-201`](EVT-201.md#EVT-201) | [SCR-026](../01_screens/SCR-026.md#SCR-026) | [UC-048](../../../01_requirements/04_business_usecases/UC-048.md#UC-048) |
| [`EVT-202`](EVT-202.md#EVT-202) | [SCR-027](../01_screens/SCR-027.md#SCR-027) | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) |
| [`EVT-203`](EVT-203.md#EVT-203) | [SCR-027](../01_screens/SCR-027.md#SCR-027) | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) |
| [`EVT-204`](EVT-204.md#EVT-204) | [SCR-027](../01_screens/SCR-027.md#SCR-027) | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) |
| [`EVT-205`](EVT-205.md#EVT-205) | [SCR-027](../01_screens/SCR-027.md#SCR-027) | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) |
| [`EVT-206`](EVT-206.md#EVT-206) | [SCR-027](../01_screens/SCR-027.md#SCR-027) | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) |
| [`EVT-207`](EVT-207.md#EVT-207) | [SCR-027](../01_screens/SCR-027.md#SCR-027) | [UC-035](../../../01_requirements/04_business_usecases/UC-035.md#UC-035) |
| [`EVT-208`](EVT-208.md#EVT-208) | [SCR-028](../01_screens/SCR-028.md#SCR-028) | [UC-037](../../../01_requirements/04_business_usecases/UC-037.md#UC-037) |
| [`EVT-209`](EVT-209.md#EVT-209) | [SCR-028](../01_screens/SCR-028.md#SCR-028) | [UC-038](../../../01_requirements/04_business_usecases/UC-038.md#UC-038) |
| [`EVT-210`](EVT-210.md#EVT-210) | [SCR-028](../01_screens/SCR-028.md#SCR-028) | [UC-037](../../../01_requirements/04_business_usecases/UC-037.md#UC-037) |
| [`EVT-211`](EVT-211.md#EVT-211) | [SCR-028](../01_screens/SCR-028.md#SCR-028) | [UC-037](../../../01_requirements/04_business_usecases/UC-037.md#UC-037) |
| [`EVT-212`](EVT-212.md#EVT-212) | [SCR-028](../01_screens/SCR-028.md#SCR-028) | [UC-037](../../../01_requirements/04_business_usecases/UC-037.md#UC-037) |
| [`EVT-213`](EVT-213.md#EVT-213) | [SCR-028](../01_screens/SCR-028.md#SCR-028) | [UC-038](../../../01_requirements/04_business_usecases/UC-038.md#UC-038) |
| [`EVT-214`](EVT-214.md#EVT-214) | [SCR-028](../01_screens/SCR-028.md#SCR-028) | [UC-039](../../../01_requirements/04_business_usecases/UC-039.md#UC-039) |
| [`EVT-215`](EVT-215.md#EVT-215) | [SCR-029](../01_screens/SCR-029.md#SCR-029) | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) |
| [`EVT-216`](EVT-216.md#EVT-216) | [SCR-029](../01_screens/SCR-029.md#SCR-029) | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) |
| [`EVT-217`](EVT-217.md#EVT-217) | [SCR-029](../01_screens/SCR-029.md#SCR-029) | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) |
| [`EVT-218`](EVT-218.md#EVT-218) | [SCR-029](../01_screens/SCR-029.md#SCR-029) | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) |
| [`EVT-219`](EVT-219.md#EVT-219) | [SCR-029](../01_screens/SCR-029.md#SCR-029) | [UC-037](../../../01_requirements/04_business_usecases/UC-037.md#UC-037) |
| [`EVT-220`](EVT-220.md#EVT-220) | [SCR-029](../01_screens/SCR-029.md#SCR-029) | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) |
| [`EVT-221`](EVT-221.md#EVT-221) | [SCR-029](../01_screens/SCR-029.md#SCR-029) | [UC-022](../../../01_requirements/04_business_usecases/UC-022.md#UC-022) |
| [`EVT-222`](EVT-222.md#EVT-222) | [SCR-030](../01_screens/SCR-030.md#SCR-030) | [UC-042](../../../01_requirements/04_business_usecases/UC-042.md#UC-042) |
| [`EVT-223`](EVT-223.md#EVT-223) | [SCR-030](../01_screens/SCR-030.md#SCR-030) | [UC-042](../../../01_requirements/04_business_usecases/UC-042.md#UC-042) |
| [`EVT-224`](EVT-224.md#EVT-224) | [SCR-030](../01_screens/SCR-030.md#SCR-030) | [UC-042](../../../01_requirements/04_business_usecases/UC-042.md#UC-042) |
| [`EVT-225`](EVT-225.md#EVT-225) | [SCR-030](../01_screens/SCR-030.md#SCR-030) | [UC-043](../../../01_requirements/04_business_usecases/UC-043.md#UC-043) |
| [`EVT-226`](EVT-226.md#EVT-226) | [SCR-030](../01_screens/SCR-030.md#SCR-030) | [UC-043](../../../01_requirements/04_business_usecases/UC-043.md#UC-043) |
| [`EVT-227`](EVT-227.md#EVT-227) | [SCR-030](../01_screens/SCR-030.md#SCR-030) | [UC-044](../../../01_requirements/04_business_usecases/UC-044.md#UC-044) |
| [`EVT-228`](EVT-228.md#EVT-228) | [SCR-030](../01_screens/SCR-030.md#SCR-030) | [UC-044](../../../01_requirements/04_business_usecases/UC-044.md#UC-044) |
| [`EVT-229`](EVT-229.md#EVT-229) | [SCR-030](../01_screens/SCR-030.md#SCR-030) | [UC-044](../../../01_requirements/04_business_usecases/UC-044.md#UC-044) |

---

<!-- portal-bottom -->
[← フロントエンド設計](../index.md) ・ [基本設計](../../index.md) ・ [↑ 設計ポータル](../../../README.md)
<!-- /portal-bottom -->
