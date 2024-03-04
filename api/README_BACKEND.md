# api
バックエンドを記述

## Description
FastAPIを使用してs3やChatGPTAPIを操作できるようにする.

## Installation

```bash

```

## Usage
プロジェクトの実行方法や使用方法

```bash

```

## File Structure

- main.py:

    アプリケーションのエントリーポイント
    FastAPIのインスタンスを作成

- models.py:

    データモデルとスキーマの定義
    データベースのテーブルや、APIリクエストとレスポンスのPydanticモデルを含む

- api_routes.py:

    APIのエンドポイント定義
    APIの具体的な記述はここで行う.(ChatGPTとs3以外)
    ユーザーの入力を受け取り、画像生成や車のパラメータ生成、データベースへの保存などの機能を実装

- game_logic.py:

    ゲームの進行に関わる主要なロジック
    データベースから情報を取得し、Chat GPTに入力する形に整形する機能を含む

- chat_gpt:
  
  - image_generation.py:

      ユーザーの入力に基づいて画像を生成するロジック
      画像生成サービスとの連携を担当

  - car_data.py:

      ユーザーの入力に基づいて車の設定を生成するロジック
      必要な計算やデータの形式を扱う


- s3
  - aws_handler.py
      データベース接続と操作のためのユーティリティ
      S3との通信を扱う関数や、データの保存と取得のためのロジックを含む      
      S3から画像URLの取得

  - image_interacter.py
      
      S3上にある画像のURLを返すAPI

- utils:  
    共通ユーティリティ関数やヘルパー関数  
    データの検証、形式の変換、エラーハンドリング関数などを含む
  - auth.py
    HTTPヘッダーの検証を行う
  - translation.py
    DeepLを使用して翻訳を行う.

- exceptions.py:
  
    アプリケーション独自の例外クラスを定義するファイル
    例えば、特定のHTTPステータスコードを返すカスタムエラーを定義する

- logger.py:
  
    アプリケーションのロギング設定を定義するファイル
    Pythonのloggingモジュールを使用してログのフォーマット、レベル、出力先を設定

- README_BACKEND.md:
  
    プロジェクトの説明、セットアップ手順、使用方法などを記載するドキュメント


- api_test/ :
    本番環境ではない時に使用するAPI
  - test_car_data.py
     chat_gpt/car_data.pyの代わりに使用,Next.jsの動作確認に使用.
  - test_translation.py
     DeepLの動作確認用API
