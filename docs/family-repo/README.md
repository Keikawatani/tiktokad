# 家族用リポジトリ プロジェクト

家族（Keikawatani 一家）で共有ノートとして使う GitHub リポジトリを新しく立ち上げる、という取り組みの記録です。
このフォルダは tiktokad リポジトリに間借りしているだけで、**家族用リポジトリが実際にできたら中身をそちらへ移す**想定です。

## このフォルダの中身

| ファイル | 内容 |
|---|---|
| [setup-steps.md](setup-steps.md) | 家族用リポジトリの作り方（命名・公開設定・初期構成・招待・2FA） |
| [family-github-guide.md](family-github-guide.md) | 家族に配る用のガイド。GitHub とは何か、書き込み方、注意点 |

## 現在地（2026-09-22 時点）

- 家族用リポジトリは **まだ作成していない**。リポジトリ名が未決のため。
- オーナーの GitHub アカウント `Keikawatani` に **2要素認証（2FA）が未設定**。
  `github.com/new` を開くと 2FA 設定画面に割り込まれる状態。猶予は残り8日（= 2026-09-30 頃が期限）。
  → リポジトリ作成より先に 2FA を設定するのが早い。
- 家族向けガイドは Claude のドキュメントとしても公開済み:
  https://claude.ai/code/artifact/58e2d250-29c1-4be8-85f6-21630d66f871

## 次にやること

1. `Keikawatani` アカウントで 2FA を設定する（[setup-steps.md](setup-steps.md) の「2FA の設定」参照）
2. リポジトリ名を決める（候補: `family` / `kawatani-family` / `home-ops`）
3. Private でリポジトリを作成し、初期構成を push する
4. 家族を Collaborator として招待する
5. [family-github-guide.md](family-github-guide.md) を新リポジトリの `docs/` に移し、家族に共有する

## 決まっていないこと

- **リポジトリ名**
- **オーナー**: 個人アカウント `Keikawatani` か、家族用 Organization を作るか（現時点では個人アカウント推奨）
- **主な用途**: 買い物リスト・レシピ中心か、家の手続き・契約の覚え書き中心か。
  フォルダ構成をどちらに寄せるかがこれで変わる。
- **招待する家族メンバー**とその GitHub アカウント
