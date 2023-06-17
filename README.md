# OpenAI Function Sandbox

このプログラムは、OpenAI Functionのデモ用に作られたシンプルなコードです。

ChatGPTを使って在庫確認とメール送信の2つのタスクを対応させることができます。このプログラムはデモンストレーション目的で作成されており、実際の在庫管理やメール送信はできません。

## 前提条件

- Python 3.6以上がインストールされていること
- OpenAI APIキーが取得されていること

## セットアップ

1. このリポジトリをクローンまたはダウンロードします。
2. `.env.sample`ファイルをコピーして`.env`ファイルを作成し、`OPENAI_API_KEY`にOpenAI APIキーを設定します。

```bash
OPENAI_API_KEY='sk-************************************************'
```



3. 必要なPythonパッケージをインストールします。


```bash
pip install -r requirements.txt
```

## 使い方

1. `app.py`を実行します。


```bash
python app.py
```

## プログラムの構成

- `inventory_search`関数: 在庫を検索する関数です。引数として、カンマで区切られた商品名の文字列を受け取ります。
- `send_mail`関数: サプライヤーにメールを送信する関数です。引数として、サプライヤー名、メッセージ本文、通知する商品名を受け取ります。
- `functions`リスト: 呼び出し可能な関数の定義が含まれています。各関数には、関数名、説明、引数の定義、必須引数が含まれています。
- `prettify_json`関数: JSONの16進数表現を日本語の文字列に変換する関数です。
- ユーザープロンプトとAIの返答を処理する`while`ループ: AIへの問い合わせを行い、関数の呼び出しとレスポンスを処理します。関数の呼び出しが必要なくなったらループを抜けます。
