<!-- portal-top -->
[設計ポータル](../../README.md) ／ [基本設計](../index.md) ／ **シーケンス設計**
<!-- /portal-top -->

# シーケンス設計

> **このセクションは、業務ユースケースに対応するシーケンス図を 1 図 1 ファイル（`SEQ-NNN`）で管理します。**

*版数 v1.0 ・ 更新 2026-06-21 ・ シーケンス 107 ・ ステータス ドラフト*

## 1. 読み順

シーケンス図は業務ユースケース順（画面起点 → システム起点）に `SEQ-001` から採番しています。各図は対応する業務ユースケース・画面・API・テーブルへトレースします。

## 2. シーケンス一覧 / ユースケース対応

各シーケンス図と対応する業務ユースケース・主な関連画面の一覧です。

| SEQ ID | 名称 | 対応業務ユースケース | 主な関連画面 |
|---|---|---|---|
| <span id="SEQ-001"></span>[SEQ-001](SEQ-001.md#SEQ-001) | 初期表示 | [UC-001](../../01_requirements/02_business_usecases/UC-001.md#UC-001) | [SCR-001](../01_screens/SCR-001.md#SCR-001) |
| <span id="SEQ-002"></span>[SEQ-002](SEQ-002.md#SEQ-002) | 「ログイン」を押下 | [UC-004](../../01_requirements/02_business_usecases/UC-004.md#UC-004) | [SCR-001](../01_screens/SCR-001.md#SCR-001) ・ [SCR-012](../01_screens/SCR-012.md#SCR-012) ・ [SCR-020](../01_screens/SCR-020.md#SCR-020) ・ [SCR-021](../01_screens/SCR-021.md#SCR-021) |
| <span id="SEQ-003"></span>[SEQ-003](SEQ-003.md#SEQ-003) | 「登録して確認メールを送信する」を押下 | [UC-016](../../01_requirements/02_business_usecases/UC-016.md#UC-016) | [SCR-002](../01_screens/SCR-002.md#SCR-002) ・ [SCR-018](../01_screens/SCR-018.md#SCR-018) |
| <span id="SEQ-004"></span>[SEQ-004](SEQ-004.md#SEQ-004) | 「再設定リンクを送信」を押下 | [UC-020](../../01_requirements/02_business_usecases/UC-020.md#UC-020) | [SCR-003](../01_screens/SCR-003.md#SCR-003) |
| <span id="SEQ-005"></span>[SEQ-005](SEQ-005.md#SEQ-005) | 「メールを再送信する」を押下 | [UC-021](../../01_requirements/02_business_usecases/UC-021.md#UC-021) | [SCR-003](../01_screens/SCR-003.md#SCR-003) |
| <span id="SEQ-006"></span>[SEQ-006](SEQ-006.md#SEQ-006) | 初期表示(段階 2) | [UC-022](../../01_requirements/02_business_usecases/UC-022.md#UC-022) | [SCR-003](../01_screens/SCR-003.md#SCR-003) |
| <span id="SEQ-007"></span>[SEQ-007](SEQ-007.md#SEQ-007) | 「再送する」を押下(段階 2 エラー時) | [UC-023](../../01_requirements/02_business_usecases/UC-023.md#UC-023) | [SCR-003](../01_screens/SCR-003.md#SCR-003) |
| <span id="SEQ-008"></span>[SEQ-008](SEQ-008.md#SEQ-008) | 「新しいパスワードを設定する」を押下 | [UC-025](../../01_requirements/02_business_usecases/UC-025.md#UC-025) | [SCR-003](../01_screens/SCR-003.md#SCR-003) |
| <span id="SEQ-009"></span>[SEQ-009](SEQ-009.md#SEQ-009) | 初期表示 | [UC-028](../../01_requirements/02_business_usecases/UC-028.md#UC-028) | [SCR-004](../01_screens/SCR-004.md#SCR-004) |
| <span id="SEQ-010"></span>[SEQ-010](SEQ-010.md#SEQ-010) | 初期表示(編集モード) | [UC-034](../../01_requirements/02_business_usecases/UC-034.md#UC-034) | [SCR-005](../01_screens/SCR-005.md#SCR-005) |
| <span id="SEQ-011"></span>[SEQ-011](SEQ-011.md#SEQ-011) | 「プロジェクトを作成」を押下 | [UC-038](../../01_requirements/02_business_usecases/UC-038.md#UC-038) | [SCR-005](../01_screens/SCR-005.md#SCR-005) |
| <span id="SEQ-012"></span>[SEQ-012](SEQ-012.md#SEQ-012) | 「保存」を押下 | [UC-039](../../01_requirements/02_business_usecases/UC-039.md#UC-039) | [SCR-005](../01_screens/SCR-005.md#SCR-005) |
| <span id="SEQ-013"></span>[SEQ-013](SEQ-013.md#SEQ-013) | 「確認メールを再送」を押下 | [UC-040](../../01_requirements/02_business_usecases/UC-040.md#UC-040) | [SCR-005](../01_screens/SCR-005.md#SCR-005) |
| <span id="SEQ-014"></span>[SEQ-014](SEQ-014.md#SEQ-014) | 「プロジェクトを削除」を押下 | [UC-042](../../01_requirements/02_business_usecases/UC-042.md#UC-042) | [SCR-005](../01_screens/SCR-005.md#SCR-005) |
| <span id="SEQ-015"></span>[SEQ-015](SEQ-015.md#SEQ-015) | 初期表示 | [UC-046](../../01_requirements/02_business_usecases/UC-046.md#UC-046) | [SCR-006](../01_screens/SCR-006.md#SCR-006) |
| <span id="SEQ-016"></span>[SEQ-016](SEQ-016.md#SEQ-016) | 状況フィルタをチェック | [UC-047](../../01_requirements/02_business_usecases/UC-047.md#UC-047) | [SCR-006](../01_screens/SCR-006.md#SCR-006) |
| <span id="SEQ-017"></span>[SEQ-017](SEQ-017.md#SEQ-017) | 期間フィルタを入力 | [UC-048](../../01_requirements/02_business_usecases/UC-048.md#UC-048) | [SCR-006](../01_screens/SCR-006.md#SCR-006) |
| <span id="SEQ-018"></span>[SEQ-018](SEQ-018.md#SEQ-018) | 「CSV エクスポート」を押下 | [UC-049](../../01_requirements/02_business_usecases/UC-049.md#UC-049) | [SCR-006](../01_screens/SCR-006.md#SCR-006) |
| <span id="SEQ-019"></span>[SEQ-019](SEQ-019.md#SEQ-019) | 検索ボックスに入力 | [UC-051](../../01_requirements/02_business_usecases/UC-051.md#UC-051) | [SCR-006](../01_screens/SCR-006.md#SCR-006) |
| <span id="SEQ-020"></span>[SEQ-020](SEQ-020.md#SEQ-020) | ページを選択 | [UC-052](../../01_requirements/02_business_usecases/UC-052.md#UC-052) | [SCR-006](../01_screens/SCR-006.md#SCR-006) |
| <span id="SEQ-021"></span>[SEQ-021](SEQ-021.md#SEQ-021) | 初期表示 | [UC-054](../../01_requirements/02_business_usecases/UC-054.md#UC-054) | [SCR-007](../01_screens/SCR-007.md#SCR-007) |
| <span id="SEQ-022"></span>[SEQ-022](SEQ-022.md#SEQ-022) | 「対応中」を選択 | [UC-056](../../01_requirements/02_business_usecases/UC-056.md#UC-056) | [SCR-007](../01_screens/SCR-007.md#SCR-007) |
| <span id="SEQ-023"></span>[SEQ-023](SEQ-023.md#SEQ-023) | 確認ダイアログの「OK」を押下 | [UC-057](../../01_requirements/02_business_usecases/UC-057.md#UC-057) | [SCR-007](../01_screens/SCR-007.md#SCR-007) |
| <span id="SEQ-024"></span>[SEQ-024](SEQ-024.md#SEQ-024) | 初期表示 | [UC-062](../../01_requirements/02_business_usecases/UC-062.md#UC-062) | [SCR-008](../01_screens/SCR-008.md#SCR-008) |
| <span id="SEQ-025"></span>[SEQ-025](SEQ-025.md#SEQ-025) | キーワードを入力 | [UC-063](../../01_requirements/02_business_usecases/UC-063.md#UC-063) | [SCR-008](../01_screens/SCR-008.md#SCR-008) |
| <span id="SEQ-026"></span>[SEQ-026](SEQ-026.md#SEQ-026) | カテゴリを選択 | [UC-064](../../01_requirements/02_business_usecases/UC-064.md#UC-064) | [SCR-008](../01_screens/SCR-008.md#SCR-008) |
| <span id="SEQ-027"></span>[SEQ-027](SEQ-027.md#SEQ-027) | 並び順を変更 | [UC-065](../../01_requirements/02_business_usecases/UC-065.md#UC-065) | [SCR-008](../01_screens/SCR-008.md#SCR-008) |
| <span id="SEQ-028"></span>[SEQ-028](SEQ-028.md#SEQ-028) | 「公開する」を押下 | [UC-069](../../01_requirements/02_business_usecases/UC-069.md#UC-069) | [SCR-008](../01_screens/SCR-008.md#SCR-008) |
| <span id="SEQ-029"></span>[SEQ-029](SEQ-029.md#SEQ-029) | 「非公開化する」を押下 | [UC-070](../../01_requirements/02_business_usecases/UC-070.md#UC-070) | [SCR-008](../01_screens/SCR-008.md#SCR-008) |
| <span id="SEQ-030"></span>[SEQ-030](SEQ-030.md#SEQ-030) | 「削除する」を押下 | [UC-071](../../01_requirements/02_business_usecases/UC-071.md#UC-071) | [SCR-008](../01_screens/SCR-008.md#SCR-008) |
| <span id="SEQ-031"></span>[SEQ-031](SEQ-031.md#SEQ-031) | 「CSV をエクスポート」を押下 | [UC-074](../../01_requirements/02_business_usecases/UC-074.md#UC-074) | [SCR-008](../01_screens/SCR-008.md#SCR-008) |
| <span id="SEQ-032"></span>[SEQ-032](SEQ-032.md#SEQ-032) | 初期表示 | [UC-076](../../01_requirements/02_business_usecases/UC-076.md#UC-076) | [SCR-009](../01_screens/SCR-009.md#SCR-009) |
| <span id="SEQ-033"></span>[SEQ-033](SEQ-033.md#SEQ-033) | 自動保存 | [UC-081](../../01_requirements/02_business_usecases/UC-081.md#UC-081) | [SCR-009](../01_screens/SCR-009.md#SCR-009) |
| <span id="SEQ-034"></span>[SEQ-034](SEQ-034.md#SEQ-034) | 保存 | [UC-082](../../01_requirements/02_business_usecases/UC-082.md#UC-082) | [SCR-008](../01_screens/SCR-008.md#SCR-008) ・ [SCR-009](../01_screens/SCR-009.md#SCR-009) |
| <span id="SEQ-035"></span>[SEQ-035](SEQ-035.md#SEQ-035) | 削除確認 OK | [UC-084](../../01_requirements/02_business_usecases/UC-084.md#UC-084) | [SCR-008](../01_screens/SCR-008.md#SCR-008) ・ [SCR-009](../01_screens/SCR-009.md#SCR-009) |
| <span id="SEQ-036"></span>[SEQ-036](SEQ-036.md#SEQ-036) | 「テンプレートをダウンロード」を押下 | [UC-091](../../01_requirements/02_business_usecases/UC-091.md#UC-091) | [SCR-010](../01_screens/SCR-010.md#SCR-010) |
| <span id="SEQ-037"></span>[SEQ-037](SEQ-037.md#SEQ-037) | 「読み込みを開始」を押下 | [UC-093](../../01_requirements/02_business_usecases/UC-093.md#UC-093) | [SCR-008](../01_screens/SCR-008.md#SCR-008) ・ [SCR-010](../01_screens/SCR-010.md#SCR-010) |
| <span id="SEQ-038"></span>[SEQ-038](SEQ-038.md#SEQ-038) | 初期表示 | [UC-096](../../01_requirements/02_business_usecases/UC-096.md#UC-096) | [SCR-011](../01_screens/SCR-011.md#SCR-011) |
| <span id="SEQ-039"></span>[SEQ-039](SEQ-039.md#SEQ-039) | 「公開キーを再発行する」を押下 | [UC-104](../../01_requirements/02_business_usecases/UC-104.md#UC-104) | [SCR-011](../01_screens/SCR-011.md#SCR-011) |
| <span id="SEQ-040"></span>[SEQ-040](SEQ-040.md#SEQ-040) | 「設定を保存」を押下 | [UC-105](../../01_requirements/02_business_usecases/UC-105.md#UC-105) | [SCR-011](../01_screens/SCR-011.md#SCR-011) |
| <span id="SEQ-041"></span>[SEQ-041](SEQ-041.md#SEQ-041) | 初期表示 | [UC-107](../../01_requirements/02_business_usecases/UC-107.md#UC-107) | [SCR-012](../01_screens/SCR-012.md#SCR-012) |
| <span id="SEQ-042"></span>[SEQ-042](SEQ-042.md#SEQ-042) | 期間を選択 | [UC-108](../../01_requirements/02_business_usecases/UC-108.md#UC-108) | [SCR-012](../01_screens/SCR-012.md#SCR-012) |
| <span id="SEQ-043"></span>[SEQ-043](SEQ-043.md#SEQ-043) | 初期表示 | [UC-115](../../01_requirements/02_business_usecases/UC-115.md#UC-115) | [SCR-013](../01_screens/SCR-013.md#SCR-013) |
| <span id="SEQ-044"></span>[SEQ-044](SEQ-044.md#SEQ-044) | 検索を入力 | [UC-116](../../01_requirements/02_business_usecases/UC-116.md#UC-116) | [SCR-013](../01_screens/SCR-013.md#SCR-013) |
| <span id="SEQ-045"></span>[SEQ-045](SEQ-045.md#SEQ-045) | 招待状態フィルタを選択 | [UC-117](../../01_requirements/02_business_usecases/UC-117.md#UC-117) | [SCR-013](../01_screens/SCR-013.md#SCR-013) |
| <span id="SEQ-046"></span>[SEQ-046](SEQ-046.md#SEQ-046) | 権限なしで URL 直アクセス | [UC-121](../../01_requirements/02_business_usecases/UC-121.md#UC-121) | [SCR-013](../01_screens/SCR-013.md#SCR-013) |
| <span id="SEQ-047"></span>[SEQ-047](SEQ-047.md#SEQ-047) | 初期表示 — 編集モード | [UC-124](../../01_requirements/02_business_usecases/UC-124.md#UC-124) | [SCR-014](../01_screens/SCR-014.md#SCR-014) |
| <span id="SEQ-048"></span>[SEQ-048](SEQ-048.md#SEQ-048) | 「招待メールを送信する」を押下 | [UC-126](../../01_requirements/02_business_usecases/UC-126.md#UC-126) | [SCR-014](../01_screens/SCR-014.md#SCR-014) |
| <span id="SEQ-049"></span>[SEQ-049](SEQ-049.md#SEQ-049) | 「招待メールを再送する」を押下 | [UC-127](../../01_requirements/02_business_usecases/UC-127.md#UC-127) | [SCR-014](../01_screens/SCR-014.md#SCR-014) |
| <span id="SEQ-050"></span>[SEQ-050](SEQ-050.md#SEQ-050) | 「変更を保存する」を押下 | [UC-128](../../01_requirements/02_business_usecases/UC-128.md#UC-128) | [SCR-014](../01_screens/SCR-014.md#SCR-014) |
| <span id="SEQ-051"></span>[SEQ-051](SEQ-051.md#SEQ-051) | 割当解除の確認ダイアログで「外す」を押下 | [UC-130](../../01_requirements/02_business_usecases/UC-130.md#UC-130) | [SCR-014](../01_screens/SCR-014.md#SCR-014) |
| <span id="SEQ-052"></span>[SEQ-052](SEQ-052.md#SEQ-052) | 初期表示 | [UC-133](../../01_requirements/02_business_usecases/UC-133.md#UC-133) | [SCR-015](../01_screens/SCR-015.md#SCR-015) |
| <span id="SEQ-053"></span>[SEQ-053](SEQ-053.md#SEQ-053) | 「同意して続ける」を押下 | [UC-135](../../01_requirements/02_business_usecases/UC-135.md#UC-135) | [SCR-015](../01_screens/SCR-015.md#SCR-015) |
| <span id="SEQ-054"></span>[SEQ-054](SEQ-054.md#SEQ-054) | 初期表示 | [UC-136](../../01_requirements/02_business_usecases/UC-136.md#UC-136) | [SCR-016](../01_screens/SCR-016.md#SCR-016) |
| <span id="SEQ-055"></span>[SEQ-055](SEQ-055.md#SEQ-055) | クイックフィルタチップを選択 | [UC-137](../../01_requirements/02_business_usecases/UC-137.md#UC-137) | [SCR-016](../01_screens/SCR-016.md#SCR-016) |
| <span id="SEQ-056"></span>[SEQ-056](SEQ-056.md#SEQ-056) | 「すべてクリア」を押下 | [UC-138](../../01_requirements/02_business_usecases/UC-138.md#UC-138) | [SCR-016](../01_screens/SCR-016.md#SCR-016) |
| <span id="SEQ-057"></span>[SEQ-057](SEQ-057.md#SEQ-057) | 詳細フィルタを適用 | [UC-139](../../01_requirements/02_business_usecases/UC-139.md#UC-139) | [SCR-016](../01_screens/SCR-016.md#SCR-016) |
| <span id="SEQ-058"></span>[SEQ-058](SEQ-058.md#SEQ-058) | お知らせ ID リンクを押下 | [UC-141](../../01_requirements/02_business_usecases/UC-141.md#UC-141) | [SCR-016](../01_screens/SCR-016.md#SCR-016) ・ [SCR-017](../01_screens/SCR-017.md#SCR-017) |
| <span id="SEQ-059"></span>[SEQ-059](SEQ-059.md#SEQ-059) | 「既読化する」を押下 | [UC-142](../../01_requirements/02_business_usecases/UC-142.md#UC-142) | [SCR-016](../01_screens/SCR-016.md#SCR-016) |
| <span id="SEQ-060"></span>[SEQ-060](SEQ-060.md#SEQ-060) | 「表示中の未読を既読化」を押下 | [UC-143](../../01_requirements/02_business_usecases/UC-143.md#UC-143) | [SCR-016](../01_screens/SCR-016.md#SCR-016) |
| <span id="SEQ-061"></span>[SEQ-061](SEQ-061.md#SEQ-061) | 「すべての未読を既読化」を押下 | [UC-144](../../01_requirements/02_business_usecases/UC-144.md#UC-144) | [SCR-016](../01_screens/SCR-016.md#SCR-016) |
| <span id="SEQ-062"></span>[SEQ-062](SEQ-062.md#SEQ-062) | 「次のページ」を押下 | [UC-145](../../01_requirements/02_business_usecases/UC-145.md#UC-145) | [SCR-016](../01_screens/SCR-016.md#SCR-016) |
| <span id="SEQ-063"></span>[SEQ-063](SEQ-063.md#SEQ-063) | 初期表示 | [UC-147](../../01_requirements/02_business_usecases/UC-147.md#UC-147) | [SCR-017](../01_screens/SCR-017.md#SCR-017) |
| <span id="SEQ-064"></span>[SEQ-064](SEQ-064.md#SEQ-064) | 初期表示 | [UC-151](../../01_requirements/02_business_usecases/UC-151.md#UC-151) | [SCR-002](../01_screens/SCR-002.md#SCR-002) ・ [SCR-018](../01_screens/SCR-018.md#SCR-018) |
| <span id="SEQ-065"></span>[SEQ-065](SEQ-065.md#SEQ-065) | 「メールを再送する」を押下 | [UC-152](../../01_requirements/02_business_usecases/UC-152.md#UC-152) | [SCR-018](../01_screens/SCR-018.md#SCR-018) |
| <span id="SEQ-066"></span>[SEQ-066](SEQ-066.md#SEQ-066) | 確認ダイアログの「OK」を押下 | [UC-159](../../01_requirements/02_business_usecases/UC-159.md#UC-159) | [SCR-019](../01_screens/SCR-019.md#SCR-019) ・ [SCR-022](../01_screens/SCR-022.md#SCR-022) |
| <span id="SEQ-067"></span>[SEQ-067](SEQ-067.md#SEQ-067) | 初期表示 | [UC-164](../../01_requirements/02_business_usecases/UC-164.md#UC-164) | [SCR-020](../01_screens/SCR-020.md#SCR-020) |
| <span id="SEQ-068"></span>[SEQ-068](SEQ-068.md#SEQ-068) | 「同意して続行する」を押下 | [UC-169](../../01_requirements/02_business_usecases/UC-169.md#UC-169) | [SCR-020](../01_screens/SCR-020.md#SCR-020) |
| <span id="SEQ-069"></span>[SEQ-069](SEQ-069.md#SEQ-069) | 初期表示 | [UC-170](../../01_requirements/02_business_usecases/UC-170.md#UC-170) | [SCR-021](../01_screens/SCR-021.md#SCR-021) |
| <span id="SEQ-070"></span>[SEQ-070](SEQ-070.md#SEQ-070) | 初期表示 | [UC-173](../../01_requirements/02_business_usecases/UC-173.md#UC-173) | [SCR-022](../01_screens/SCR-022.md#SCR-022) |
| <span id="SEQ-071"></span>[SEQ-071](SEQ-071.md#SEQ-071) | 「保存する」を押下(プロフィール) | [UC-177](../../01_requirements/02_business_usecases/UC-177.md#UC-177) | [SCR-018](../01_screens/SCR-018.md#SCR-018) ・ [SCR-022](../01_screens/SCR-022.md#SCR-022) |
| <span id="SEQ-072"></span>[SEQ-072](SEQ-072.md#SEQ-072) | 「パスワードを変更する」を押下 | [UC-178](../../01_requirements/02_business_usecases/UC-178.md#UC-178) | [SCR-022](../01_screens/SCR-022.md#SCR-022) |
| <span id="SEQ-073"></span>[SEQ-073](SEQ-073.md#SEQ-073) | 初期表示 | [UC-181](../../01_requirements/02_business_usecases/UC-181.md#UC-181) | [SCR-023](../01_screens/SCR-023.md#SCR-023) |
| <span id="SEQ-074"></span>[SEQ-074](SEQ-074.md#SEQ-074) | 「登録を完了する」を押下 | [UC-190](../../01_requirements/02_business_usecases/UC-190.md#UC-190) | [SCR-023](../01_screens/SCR-023.md#SCR-023) |
| <span id="SEQ-075"></span>[SEQ-075](SEQ-075.md#SEQ-075) | 初期表示 | [UC-194](../../01_requirements/02_business_usecases/UC-194.md#UC-194) | [SCR-024](../01_screens/SCR-024.md#SCR-024) |
| <span id="SEQ-076"></span>[SEQ-076](SEQ-076.md#SEQ-076) | 初期表示 | [UC-196](../../01_requirements/02_business_usecases/UC-196.md#UC-196) | [SCR-025](../01_screens/SCR-025.md#SCR-025) |
| <span id="SEQ-077"></span>[SEQ-077](SEQ-077.md#SEQ-077) | 初期表示 | [UC-199](../../01_requirements/02_business_usecases/UC-199.md#UC-199) | [SCR-026](../01_screens/SCR-026.md#SCR-026) |
| <span id="SEQ-078"></span>[SEQ-078](SEQ-078.md#SEQ-078) | URL へ直接アクセス(権限不足) | [UC-201](../../01_requirements/02_business_usecases/UC-201.md#UC-201) | [SCR-026](../01_screens/SCR-026.md#SCR-026) |
| <span id="SEQ-079"></span>[SEQ-079](SEQ-079.md#SEQ-079) | 初期表示 | [UC-202](../../01_requirements/02_business_usecases/UC-202.md#UC-202) | [SCR-027](../01_screens/SCR-027.md#SCR-027) |
| <span id="SEQ-080"></span>[SEQ-080](SEQ-080.md#SEQ-080) | 「保存」を押下 | [UC-206](../../01_requirements/02_business_usecases/UC-206.md#UC-206) | [SCR-027](../01_screens/SCR-027.md#SCR-027) |
| <span id="SEQ-081"></span>[SEQ-081](SEQ-081.md#SEQ-081) | 初期表示 | [UC-208](../../01_requirements/02_business_usecases/UC-208.md#UC-208) | [SCR-028](../01_screens/SCR-028.md#SCR-028) |
| <span id="SEQ-082"></span>[SEQ-082](SEQ-082.md#SEQ-082) | 「支払方法を変更」を押下 | [UC-209](../../01_requirements/02_business_usecases/UC-209.md#UC-209) | [SCR-028](../01_screens/SCR-028.md#SCR-028) |
| <span id="SEQ-083"></span>[SEQ-083](SEQ-083.md#SEQ-083) | 「領収書」リンクを押下 | [UC-210](../../01_requirements/02_business_usecases/UC-210.md#UC-210) | [SCR-028](../01_screens/SCR-028.md#SCR-028) |
| <span id="SEQ-084"></span>[SEQ-084](SEQ-084.md#SEQ-084) | 「支払い方法を登録」を押下(バナー CTA) | [UC-213](../../01_requirements/02_business_usecases/UC-213.md#UC-213) | [SCR-028](../01_screens/SCR-028.md#SCR-028) |
| <span id="SEQ-085"></span>[SEQ-085](SEQ-085.md#SEQ-085) | 初期表示 | [UC-215](../../01_requirements/02_business_usecases/UC-215.md#UC-215) | [SCR-029](../01_screens/SCR-029.md#SCR-029) |
| <span id="SEQ-086"></span>[SEQ-086](SEQ-086.md#SEQ-086) | 「変更を保存」を押下 | [UC-217](../../01_requirements/02_business_usecases/UC-217.md#UC-217) | [SCR-029](../01_screens/SCR-029.md#SCR-029) |
| <span id="SEQ-087"></span>[SEQ-087](SEQ-087.md#SEQ-087) | ランチャーバッジを押下 | [UC-223](../../01_requirements/02_business_usecases/UC-223.md#UC-223) | — |
| <span id="SEQ-088"></span>[SEQ-088](SEQ-088.md#SEQ-088) | 「送信」を押下 | [UC-226](../../01_requirements/02_business_usecases/UC-226.md#UC-226) | — |
| <span id="SEQ-089"></span>[SEQ-089](SEQ-089.md#SEQ-089) | AI 回答(未解決)を受信 | [UC-227](../../01_requirements/02_business_usecases/UC-227.md#UC-227) | — |
| <span id="SEQ-090"></span>[SEQ-090](SEQ-090.md#SEQ-090) | 非同期 CSV インポートジョブ | [UC-230](../../01_requirements/02_business_usecases/UC-230.md#UC-230) | [SCR-010](../01_screens/SCR-010.md#SCR-010) |
| <span id="SEQ-091"></span>[SEQ-091](SEQ-091.md#SEQ-091) | Resend Webhook 受信(配信状態更新) | [UC-231](../../01_requirements/02_business_usecases/UC-231.md#UC-231) | — |
| <span id="SEQ-092"></span>[SEQ-092](SEQ-092.md#SEQ-092) | 90 日物理削除バッチ | [UC-232](../../01_requirements/02_business_usecases/UC-232.md#UC-232) | — |
| <span id="SEQ-093"></span>[SEQ-093](SEQ-093.md#SEQ-093) | 月次請求確定バッチ | [UC-233](../../01_requirements/02_business_usecases/UC-233.md#UC-233) | — |
| <span id="SEQ-094"></span>[SEQ-094](SEQ-094.md#SEQ-094) | 運営お知らせ配信 | [UC-234](../../01_requirements/02_business_usecases/UC-234.md#UC-234) | — |
| <span id="SEQ-095"></span>[SEQ-095](SEQ-095.md#SEQ-095) | 運用イベントのシステム通知自動生成 | [UC-235](../../01_requirements/02_business_usecases/UC-235.md#UC-235) | — |
| <span id="SEQ-096"></span>[SEQ-096](SEQ-096.md#SEQ-096) | メンバー割当変更通知 | [UC-236](../../01_requirements/02_business_usecases/UC-236.md#UC-236) | — |
| <span id="SEQ-097"></span>[SEQ-097](SEQ-097.md#SEQ-097) | 質問数上限アラート通知 | [UC-237](../../01_requirements/02_business_usecases/UC-237.md#UC-237) | — |
| <span id="SEQ-098"></span>[SEQ-098](SEQ-098.md#SEQ-098) | 通知再送 | [UC-238](../../01_requirements/02_business_usecases/UC-238.md#UC-238) | — |
| <span id="SEQ-099"></span>[SEQ-099](SEQ-099.md#SEQ-099) | 利用量リアルタイム集計・UI 反映 | [UC-239](../../01_requirements/02_business_usecases/UC-239.md#UC-239) | — |
| <span id="SEQ-100"></span>[SEQ-100](SEQ-100.md#SEQ-100) | 上限到達ウィジェット受付停止 | [UC-240](../../01_requirements/02_business_usecases/UC-240.md#UC-240) | — |
| <span id="SEQ-101"></span>[SEQ-101](SEQ-101.md#SEQ-101) | 決済失敗→猶予→サスペンション | [UC-241](../../01_requirements/02_business_usecases/UC-241.md#UC-241) | — |
| <span id="SEQ-102"></span>[SEQ-102](SEQ-102.md#SEQ-102) | セッション失効・再認証 | [UC-242](../../01_requirements/02_business_usecases/UC-242.md#UC-242) | — |
| <span id="SEQ-103"></span>[SEQ-103](SEQ-103.md#SEQ-103) | ログイン失敗ロックアウト・解除 | [UC-243](../../01_requirements/02_business_usecases/UC-243.md#UC-243) | — |
| <span id="SEQ-104"></span>[SEQ-104](SEQ-104.md#SEQ-104) | 契約停止時セッション一斉無効化 | [UC-244](../../01_requirements/02_business_usecases/UC-244.md#UC-244) | — |
| <span id="SEQ-105"></span>[SEQ-105](SEQ-105.md#SEQ-105) | AI しきい値変更の伝播・フォールバック | [UC-245](../../01_requirements/02_business_usecases/UC-245.md#UC-245) | — |
| <span id="SEQ-106"></span>[SEQ-106](SEQ-106.md#SEQ-106) | 受信箱の重複集約 | [UC-246](../../01_requirements/02_business_usecases/UC-246.md#UC-246) | — |
| <span id="SEQ-107"></span>[SEQ-107](SEQ-107.md#SEQ-107) | 監査ログ整合性検証(日次) | [UC-247](../../01_requirements/02_business_usecases/UC-247.md#UC-247) | — |

---

<!-- portal-bottom -->
[基本設計](../index.md) ・ [↑ 設計ポータル](../../README.md)
<!-- /portal-bottom -->
