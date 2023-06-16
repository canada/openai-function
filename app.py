import openai
from dotenv import load_dotenv
import os
import json

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
query = "みかんとぶどうの在庫をチェックして、その中に在庫が０の商品があったら、その商品のサプライヤーにのみ追加注文のメールを送ってください。"
query = """
与えられた商品名が1つ以上あります。
それそれについて、在庫が0であるかどうか検査し、在庫が0である場合はその商品のサプライヤーに追加注文のメールを送ってください。
在庫がある場合は何もしません。
===
みかん、ぶどう、バナナ
"""

stock = [
    {"item": "みかん", "stock": 0, "supplier_for_item": "温州コーポレーション"},
    {"item": "りんご", "stock": 10, "supplier_for_item": "ハローKiddy Industory"},
    {"item": "バナナ", "stock": 0, "supplier_for_item": "The Donkey Foods"},
    {"item": "パイナップル", "stock": 1000, "supplier_for_item": "ペンパイナッポー流通"},
    {"item": "ぶどう", "stock": 100, "supplier_for_item": "グレープ Fruits inc."},
]

# 在庫チェック関数
def inventory_search(arguments):
    # 名前で在庫を探す
    inventory_names = json.loads(arguments)["inventory_names"]
    inventories = []
    for x in inventory_names.split(","):
        inventories.append(next((item for item in stock if item["item"] == x), None))

    print ("Function:\n returns " + str(inventories) + "\n")
    return json.dumps(inventories)

# メール送信関数
def send_mail(arguments):
    args = json.loads(arguments)
    print("Function:\nreturns ")
    print({"status": "success"})
    print("""
 mail sent as follows
=====
{}さま
いつもお世話になっております。
商品名：{}
{}
よろしくお願いします。

""".format(args["supplier_name"], args["items"], args["message_body"]))
    return json.dumps({"status": "success"})

# 呼び出し可能な関数の定義
functions=[
    # 在庫チェック関数の定義
    {
        # 関数名
        "name": "inventory_search",
        # 関数の説明
        "description": "Search for inventory items. items must be separated by comma.",
        # 関数の引数の定義
        "parameters": {
            "type": "object",
            "properties": {
                "inventory_names": {
                    "type": "string",
                    "description": "Input query",
                },
            },
            # 必須引数の定義
            "required": ["input"],
        },
    },
    # メール送信関数の定義
    {
        # 関数名
        "name": "send_mail",
        # 関数の説明
        "description": "Send mail to supplier. Be sure that this function can send one mail at a time.",
        # 関数の引数の定義
        "parameters": {
            "type": "object",
            "properties": {
                "supplier_name": {
                    "type": "string",
                    "description": "suppliyer of the item",
                },
                "message_body": {
                    "type": "string",
                    "description": "message body to supplier",
                },
                "items": {
                    "type": "string",
                    "description": "an item to notify to supplier. Be sure that only one item can be notified at a time.",
                },
            },
            # 必須引数の定義
            "required": ["item_shortage"],
        },
    },
]

# JSONの16進数表現を日本語の文字列に変換する
def prettify_json(message_json):
    return json.dumps(message_json, ensure_ascii=False, indent=4)

# ユーザープロンプト
user_prompt = {"role": "user", "content": query}

# 初回問い合わせ
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[user_prompt],
    # Function callを使うことを明示
    functions=functions,
    function_call="auto",
)

# AIの返答を取得
message = response.choices[0]["message"]

messages = []

# AIの返答にFunction callがある限り繰り返す
while message.get('function_call'):
    print("AI response: ")
    print(prettify_json(message))
    print()
    messages.append(message)

    f_call = message["function_call"]

    # 関数の呼び出し、レスポンスの取得
    print("Function call: " + f_call["name"] + "()\nParams: " + f_call["arguments"] + "\n")
    function_response = globals()[f_call["name"]](f_call["arguments"])

    # messagesに関数のレスポンスを追加
    messages.append({
        "role": "function",
        "name": f_call["name"],
        "content": function_response,
    })

    # 再問い合わせ
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            user_prompt,
            # 過去のやりとりをすべて与える
            *messages
        ],
        # 関数の定義も毎回与える
        functions=functions,
        function_call="auto",
        temperature=0.0,
    )
    # AIの返答を取得
    message = response.choices[0]["message"]

# これ以上Functionを呼び出す必要がなくなった
print("Chain finished!")
print()
print("AI response: ")
print(prettify_json(message))