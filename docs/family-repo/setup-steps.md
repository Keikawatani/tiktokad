# 家族用リポジトリの作成手順

管理者（リポジトリを作る人）向けの手順書です。家族に配るガイドは [family-github-guide.md](family-github-guide.md)。

## 0. 前提: 2FA の設定

GitHub は 2023 年以降、コードを push する全ユーザーに二要素認証を必須化している。
未設定だと `github.com/new` などが 2FA 設定画面にリダイレクトされ、猶予期間を過ぎると主要機能が使えなくなる。

### 2FA の設定手順

1. `Enable 2FA now` を押す
2. 方式は **Authenticator app（認証アプリ）** が手軽。iOS 標準の「パスワード」アプリ、Google Authenticator、1Password など
3. 表示された QR コードを認証アプリでスキャン
4. アプリに出た 6 桁のコードを入力
5. **リカバリーコード（16 個の文字列）を必ず保存する。** スマホを紛失したときにアカウントへ入る唯一の手段
6. 完了

### 2FA 有効化後の注意

HTTPS での `git push` にパスワードが使えなくなる。以下のどちらかが必要:

- **Personal Access Token**（Settings → Developer settings → Personal access tokens）をパスワード代わりに使う
- **SSH 鍵**に切り替える（推奨）

既に push できている環境（トークンや SSH 設定済み）には影響しない。
招待される家族側のアカウントでも同様に 2FA が必要になる点は事前に伝えておく。

## 1. 決めること

| 項目 | 方針 |
|---|---|
| オーナー | 個人アカウント `Keikawatani` で十分。家族 3 人以上で権限管理したいなら Organization（無料） |
| リポジトリ名 | `family` / `kawatani-family` / `home-ops` など |
| 公開設定 | **Private 必須**。家族の予定・住所・手続き情報が入るため |
| README | あり。運用ルールを書く場所になる |
| ライセンス | 不要（Private なので付けない） |

## 2. リポジトリ作成（Web UI）

1. https://github.com/new を開く
2. Owner = `Keikawatani`、Repository name = 決めた名前
3. **Private** を選択
4. 「Add a README file」にチェック
5. Create repository

`gh` CLI がある環境なら 1 コマンドで済む:

```bash
gh repo create Keikawatani/family --private --add-readme --clone
```

## 3. 家族を招待

`Settings` → `Collaborators` → `Add people` で家族の GitHub アカウントを追加し、**Write 権限**を与える。
GitHub アカウントを持っていない家族には先に作ってもらう必要がある。

## 4. 初期構成

```bash
git clone https://github.com/Keikawatani/<repo-name>.git
cd <repo-name>
mkdir -p docs recipes household travel assets
```

想定するフォルダ構成:

```
README.md          # 使い方・運用ルール
docs/              # 保険・契約・手続きの覚え書き、ゴミの出し方
recipes/           # 家のレシピ、味付けのメモ
household/         # 買い物リスト、当番表、年間の予定
travel/            # 旅行の計画、持ち物リスト
assets/            # 画像など（大きいファイルは入れない）
.gitignore
```

`.gitignore` のテンプレート:

```gitignore
# OS
.DS_Store
Thumbs.db

# 個人の一時ファイル
*.tmp
~$*

# 機密情報は絶対にコミットしない
secrets/
*.key
```

```bash
git add -A && git commit -m "初期構成を追加" && git push
```

## 5. 運用の注意点

- **パスワード・マイナンバー・カード番号はコミットしない。** Private でも履歴に永久に残り、完全な削除は難しい。パスワードはパスワードマネージャへ
- **大きい写真・動画は入れない。** リポジトリが肥大化する。Google フォト等のリンクを Markdown に貼る運用にする
- 家族が Git に不慣れなら、**GitHub の Web UI で直接編集**（ファイルの鉛筆アイコン）してもらうのが一番ハードルが低い
- ブランチ保護は最初は不要。全員が `main` に直接コミットする運用で問題ない
