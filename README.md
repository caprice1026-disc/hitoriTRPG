# ひとりTRPG

このプロジェクトは、フロントエンドとバックエンドを含む、ひとりで遊べるTRPGゲームの開発途中のものです。誰でも改善案やプルリクエストを送信してください！

## バックエンド

Flaskを使用してAPIを構築しており、ユーザー認証、ゲームセッション管理などの機能が実装されています。

### データベース

SQLiteを使用しており、`backend/config.py`で設定されています。

## フロントエンド

Reactを使用してUIを構築しており、`frontend`ディレクトリにすべてのソースコードが含まれています。


## 注意

- このプロジェクトはまだ開発中です。現状このリポジトリはフロントエンドとバックエンドのソースコードが混在していますが、今後はそれぞれのディレクトリに分けて管理する予定です。
- このリポジトリは、学術的な目的にのみ使用することを目的としています。ゲームのルールや世界設定などは、オリジナルのものであり、著作権は私に帰属します。

# 今後の実装予定

## バックエンド

- ~~ゲームの進行状況を保存・更新するロジックの実装~~ →更新ロジックはだいたい書き上がっています。保存ロジックの方に移ります。
- OpenAI APIを呼び出す部分をlangchainやllamaindexを使用したものに変更する
- プレイヤーのステータスやインベントリの管理機能
- ゲームのルールや世界設定に関するデータモデルの拡張
- バックエンドとフロントエンドの切り離しおよびバックエンドのAPIエンドポイントの整理、ディレクトリ構成の整理など

## フロントエンド

- ユーザーインターフェースの改善と拡張
- ゲームの進行に合わせた動的なコンテンツの表示
- レスポンシブデザインの適用によるモバイル対応

## 全体

- フロントエンドとバックエンドの連携強化
- セキュリティの強化と脆弱性の修正
- ユーザーテストを通じたフィードバックの収集と機能改善
