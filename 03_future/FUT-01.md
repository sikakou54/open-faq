# <span id="FUT-01"></span>FUT-01: 認証・セキュリティ強化

## <span id="0-文書情報"></span>0. 文書情報

| 項目         | 内容                                      |
|--------------|-------------------------------------------|
| 文書名       | FUT-01: 認証・セキュリティ強化             |
| 将来対応ID   | FUT-01                                    |
| 対象システム | FAQ AI ウィジェット SaaS / メインシステム |
| 作成日       | 2026-05-17                                |
| 版数         | v1.1                                      |
| ステータス   | 検討中(MVP 外)                            |

------------------------------------------------------------------------

## <span id="1-概要"></span>1. 概要

| 項目 | 内容 |
|----|----|
| 概要 | MVP では補完策(パスワード再入力、ロックアウト、操作通知、監査ログ、DB 操作者制限・月次棚卸し・全クエリ監査)でリスク受容している認証・セキュリティ領域について、Post-MVP で MFA / 列単位暗号化 / SSO・パスキーを順次強化する。 |
| 背景 | 単一プラン・最小構成での MVP リリース後、限定公開〜GA フェーズで利用者側の認証強度・チャット本文の機密性をエンタープライズ水準まで引き上げる必要がある。 |
| 期待効果 | アカウント乗っ取りリスクの低減、個別チャット本文漏洩時の影響範囲限定、特権操作の証跡強化、エンタープライズ契約獲得余地の拡大。 |
| 優先度(将来対応内) | 高 |
| 想定時期 | T2(ベータ判定まで)〜 T3(GA 判定まで) |

------------------------------------------------------------------------

## <span id="2-関連要件候補"></span>2. 関連要件・候補

### <span id="21-要件候補将来-fr"></span>2.1 要件候補(将来 FR)

#### <span id="認証セキュリティ"></span>認証・セキュリティ

| ID | 要件候補 | MVP の前提 | 判定時期 | 判定基準 / 完了条件 |
|----|----|----|----|----|
| FUT-REQ-SEC-001 | 個別チャット本文の列単位暗号化 | 平文保存 + DB 操作者 2 名以下・月次棚卸し・全クエリ監査の補完策 | GA | AES-256-GCM + オーナー派生鍵による列単位暗号化方式が承認され、staging 復元 E2E スモークが合格すること |
| FUT-REQ-SEC-002 | 利用者側 admin / operator MFA | パスワード再入力、ロックアウト、操作通知、監査ログでリスク受容 | 限定公開 / ベータ / GA | 限定公開で admin opt-in、ベータでオーナー単位強制可、GA で新規オーナー既定 ON とするか判定 |
| FUT-REQ-SEC-005 | SSO / ソーシャルログイン / パスキー | 自前アカウント + パスワード + メール確認 | Post-MVP | エンタープライズ要望、認証リスク低減効果、サポート負荷をもとに判定 |
| FUT-REQ-SEC-006 | データ保持期間の利用者側調整 UI(短縮 / 長期化) | MVP は NFR-046 によりシステム固定値で固定し UI を提供しない。短縮はサポート窓口経由で対応、長期化は契約調整で対応 | Post-MVP | エンタープライズ顧客のコンプライアンス要件・契約条項としてのデータ保持カスタマイズ需要、長期化承認フロー整備、電子帳簿保存法等の法定下限を下回らないガード設計を踏まえて再開判定 |
| FUT-REQ-SEC-007 | 不正利用(大量送信・Bot 疑い・規約違反)の自動検知・自動ブロック(段階導入) | MVP はプロジェクト単位レート制限(FR-095)で濫用を抑止し、自動検知・自動ブロックは提供しない | ベータ / GA | Bot 判定・規約違反検知の精度と誤検知率、自動ブロック後の即時通知・申し立て窓口運用、プロジェクト別しきい値上書きの設計が承認されること |

### <span id="22-基本設計論点"></span>2.2 基本設計論点

#### <span id="認証セキュリティ-1"></span>認証・セキュリティ

| 項目 | 基本設計で具体化すること | 関連 Future 要件 |
|----|----|----|
| 利用者側 admin / operator MFA | SCR-022 個人設定での MFA 登録・解除・リカバリ、SCR-029 設定でのオーナー単位強制状態、未設定ユーザーのログイン制御 | FUT-REQ-SEC-002 |
| SSO / パスキー | 認証プロバイダ選定、既存自前認証との併存、招待・退会・ロックアウトとの状態整合 | FUT-REQ-SEC-005 |
| 個別チャット列単位暗号化 | 鍵階層、検索・復元・監査への影響、障害時の復旧設計、運用者が本文を扱う導線の制限 | FUT-REQ-SEC-001 |

### <span id="23-詳細設計バックログ"></span>2.3 詳細設計バックログ

#### <span id="オーナー-mfa-強制ddl-候補"></span>オーナー MFA 強制(DDL 候補)

```sql
-- オーナー専有属性に追加(v1.11 で 2 マスタ完全分離: `M_OWNERS` / `M_PRJ_USERS` / `M_PRJ_USER_ASGN` へ再編済み)
ALTER TABLE M_OWNERS
  ADD COLUMN mfa_enforcement TEXT NOT NULL DEFAULT 'off'
  CHECK (mfa_enforcement IN ('off', 'admin_only', 'all_members'));

CREATE TABLE owner_mfa_policy_audit_logs (
  id                      TEXT PRIMARY KEY,
  owner_id  TEXT NOT NULL REFERENCES M_OWNERS(id) ON DELETE CASCADE,
  changed_by              TEXT REFERENCES M_OWNERS(id) ON DELETE SET NULL,
  before_policy           TEXT NOT NULL,
  after_policy            TEXT NOT NULL,
  reason                  TEXT,
  created_at              TEXT NOT NULL
);
```

#### <span id="個別チャット本文の列単位暗号化ddl-候補"></span>個別チャット本文の列単位暗号化(DDL 候補)

```sql
ALTER TABLE chat_messages
  ADD COLUMN body_ciphertext BLOB,
  ADD COLUMN body_nonce TEXT,
  ADD COLUMN body_key_version INTEGER;

CREATE TABLE owner_key_versions (
  id                      TEXT PRIMARY KEY,
  owner_id  TEXT NOT NULL REFERENCES M_OWNERS(id) ON DELETE CASCADE,
  key_version             INTEGER NOT NULL,
  status                  TEXT NOT NULL,
  created_at              TEXT NOT NULL,
  rotated_at              TEXT,
  UNIQUE (owner_id, key_version),
  CHECK (status IN ('active', 'retired'))
);
```

#### <span id="実装設計バックログ関連分"></span>実装設計バックログ(関連分)

| ID | 対象 | 実装設計で具体化すること | 関連 Future 要件 |
|----|----|----|----|
| FUT-DD-SEC-001 | 個別チャット列単位暗号化 | 暗号化カラム、鍵派生、ローテーション、バックフィル、復元手順、検索制約、監査ログ | FUT-REQ-SEC-001 |
| FUT-DD-SEC-002 | 利用者側 MFA | `M_OWNERS.mfa_enforcement`、MFA 登録 API、回復コード、未設定時ログイン制御、監査ログ | FUT-REQ-SEC-002 |

#### <span id="api--worker-候補関連分"></span>API / Worker 候補(関連分)

| 領域 | 候補 |
|----|----|
| オーナー MFA | `POST /api/v1/settings/mfa-policy`、`POST /api/v1/auth/mfa/setup`、`POST /api/v1/auth/mfa/recovery-code` |

#### <span id="テスト検証候補関連分"></span>テスト・検証候補(関連分)

| 領域 | 検証項目 |
|----|----|
| MFA | 未登録ユーザーのログイン遮断、回復コード、強制 ON 変更時の既存セッション扱い、監査ログ |
| 暗号化 | key rotation、dual read、復元、検索不可項目のエラー、バックフィル再実行性 |

------------------------------------------------------------------------

## <span id="3-影響範囲"></span>3. 影響範囲

| 種別 | 影響内容 |
|----|----|
| 要件 | FR-005(MFA 段階導入)、NFR-028(個別チャット平文 → 暗号化)、SSO / パスキーは新規要件として追加 |
| 画面 | SCR-022 個人設定(MFA 登録・解除・回復コード)、SCR-029 設定(MFA 強制ポリシー)、ログイン画面(MFA 入力)、招待受諾フロー(オーナー単位強制下) |
| API | `POST /api/v1/settings/mfa-policy`、`POST /api/v1/auth/mfa/setup`、`POST /api/v1/auth/mfa/recovery-code`、SSO 連携 OAuth / OIDC エンドポイント |
| テーブル | `M_OWNERS.mfa_enforcement` 列追加、`owner_mfa_policy_audit_logs`、`chat_messages.body_ciphertext` / `body_nonce` / `body_key_version`、`owner_key_versions` |
| 運用 | MFA 未設定者向けの猶予期間運用、回復コード再発行手順、鍵ローテーション Runbook、列単位暗号化への dual read 期間運用、SSO IdP との連携運用 |

------------------------------------------------------------------------

## <span id="4-実施条件"></span>4. 実施条件

| 項目 | 内容 |
|----|----|
| 実施判断条件 | 限定公開での admin MFA opt-in 率(50% 以上)、AES-256-GCM 列単位暗号化方式の設計承認、staging 復元 E2E 合格 |
| 期限 | T2(MFA opt-in、招待トークン期限短縮判定)、T3(MFA オーナー単位強制 ON、列単位暗号化)、Post-MVP(SSO / パスキー) |
| 依存関係 | 共有概念の 2 マスタ完全分離ユーザーモデル(`M_OWNERS` / `M_PRJ_USERS` / `M_PRJ_USER_ASGN`)拡張、PII 暗号化(メイン正本)・暗号鍵管理(メイン正本)との整合 |

------------------------------------------------------------------------

## <span id="5-関連設計"></span>5. 関連設計

| 種別 | 参照先 |
|----|----|
| 要件 | [../01_requirements/index.md](../01_requirements/index.md) |
| 基本設計 | [../02_basic_design/index.md](../02_basic_design/index.md) |

------------------------------------------------------------------------

## <span id="6-未確定事項確認事項"></span>6. 未確定事項・確認事項

| 確認事項ID | 確認内容 | 優先度 | ステータス |
|----|----|----|----|
| FUT-SEC-Q-001 | MFA オーナー単位強制 ON 時の既存ユーザー猶予期間と通知方式 | 高 | 検討中 |
| FUT-SEC-Q-002 | 個別チャット列単位暗号化の dual read 期間とバックフィル実行ウィンドウ | 高 | 検討中 |
| FUT-SEC-Q-003 | SSO / パスキー導入時の自前アカウントとの併存方式(同一メールでの統合可否) | 中 | 検討中 |
