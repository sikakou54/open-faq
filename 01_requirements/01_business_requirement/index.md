# 業務要件

> **このページは、業務要件(BR)と業務ルール(RULE)の一覧です。** 業務要件はカテゴリ別ファイル(`-br.md`)の HTML テーブル(1 行 = 1 要件)、業務ルールは [`08_rule.md`](08_rule.md) の節で保持する。

## 業務要件(BR)

業務要件はカテゴリ単位で 6 ファイルに一覧化している。各カテゴリの一覧(ID・名称・機能グループ・要件)はリンク先ファイルの HTML テーブルを正本とする。

| カテゴリID | カテゴリ | 件数 | 主な機能グループ |
|----|----|----|----|
| <span id="BR-ACCOUNT"></span>BR-ACCOUNT | [アカウント・ユーザー・アクセス制御](01_account-br.md) | 42 | アカウント管理 / ユーザー管理(オーナー + メンバー) / プロジェクト管理 / 課金・請求 / アクセス制御細部 |
| <span id="BR-FAQAI"></span>BR-FAQAI | [FAQ・AI 回答・未解決質問・処理エラー](02_faq-ai-br.md) | 35 | FAQ 管理 / AI 回答 / 未解決質問登録 / 未解決質問から FAQ 登録 / 処理エラー / AI 推論動作 |
| <span id="BR-USAGE"></span>BR-USAGE | [利用量・課金・ダッシュボード・運用](03_usage-br.md) | 25 | 利用量・課金 / 管理ダッシュボード / UX 細部・データ運用 |
| <span id="BR-WIDGET"></span>BR-WIDGET | [ウィジェット・検索・入出力](04_widget-br.md) | 15 | ウィジェット / 検索・全文検索 / インポート・エクスポート |
| <span id="BR-NOTIFICATION"></span>BR-NOTIFICATION | [通知・お知らせ](05_notification-br.md) | 20 | 通知 / お知らせ |
| <span id="BR-SECURITY"></span>BR-SECURITY | [セキュリティ・プライバシー](06_security-br.md) | 10 | プライバシー・データ管理 / セキュリティ |

## 業務ルール(要件)

[業務ルール(要件)(20 件)](08_rule.md)

- [RULE-001: ログイン失敗ロックアウト](08_rule.md#RULE-001)
- [RULE-002: 再認証の有効範囲](08_rule.md#RULE-002)
- [RULE-003: パスワードポリシー](08_rule.md#RULE-003)
- [RULE-004: 無操作タイムアウト](08_rule.md#RULE-004)
- [RULE-005: 絶対タイムアウト](08_rule.md#RULE-005)
- [RULE-006: 規約改定の予告・同意期限](08_rule.md#RULE-006)
- [RULE-007: 招待リンク有効期限](08_rule.md#RULE-007)
- [RULE-008: アカウント論理削除の猶予](08_rule.md#RULE-008)
- [RULE-009: プロジェクト連絡先確認メール有効期限](08_rule.md#RULE-009)
- [RULE-010: FAQ 件数上限](08_rule.md#RULE-010)
- [RULE-011: FAQ 文字数上限](08_rule.md#RULE-011)
- [RULE-012: AI しきい値既定値](08_rule.md#RULE-012)
- [RULE-013: 質問数上限の停止・追加通知](08_rule.md#RULE-013)
- [RULE-014: 質問数アラート閾値](08_rule.md#RULE-014)
- [RULE-015: 無料枠](08_rule.md#RULE-015)
- [RULE-016: 決済失敗の猶予期間](08_rule.md#RULE-016)
- [RULE-017: 課金通知の受信履歴保持](08_rule.md#RULE-017)
- [RULE-018: 公開キーローテーション猶予](08_rule.md#RULE-018)
- [RULE-019: 一括操作の上限](08_rule.md#RULE-019)
- [RULE-020: AI 推論タイムアウト](08_rule.md#RULE-020)
