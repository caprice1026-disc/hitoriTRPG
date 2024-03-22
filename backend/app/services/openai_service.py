from openai import OpenAI
# langchainだとJSONパースが微妙なことがおおい。
from llama_index import llamaindex
import json
import requests
from flask import request
import os

#ダイスロール時のOpenAI呼び出しとステータス変化時のOpenAI呼び出しを違うものとして実装
OPENAI_API_KEY =os.environ.get('OPENAI_API_KEY')
client = OpenAI
# プロンプトはあとでまとめる
'''prompt = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
'''
# 引数にユーザーの入力を受け取る
def openai_call(input):
  try:
    #ユーザーの入力をOpenAIに渡す処理
    input = request.json['input'] # フロントエンドからのリクエストを受け取る。現状プレースホルダー
    # OpenAIに、ユーザーの入力を渡して返答をもらう
    response = []
    completion = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
    {"role": "system", "content": "あなたは優秀なTRPGのGMです。ユーザーからのメッセージをもとに、シナリオの続きを作成してください。"},
    {"role": "user", "content": input}
    ],
    stream=True
    )

    for chunk in completion:
      # ストリーミング出力の内容をresponseに保存してreflesh_statusに渡す必要がある。
      response.append(chunk.choices[0].message.content.text.strip())
      
      # ユーザーの入力に対するOpenAIの返答をフロントエンドに返すように変更すること。
      print(chunk.choices[0].delta)


    # シナリオが長くなりすぎた際にまとめる処理(アシスタントAPIでも可)
    # OpenAIに、GMとしてシナリオの続きを書かせる
    #内容をreflesh_statusに渡してJSONでパースする処理
  except Exception as e:
    raise e
  
  # UX向上のため、シナリオの返答とステータスの返答を分ける。引数は暫定
def reflesh_status(response):
    try:
      completion = client.chat.completions.create(
      model="gpt-4-turbo-preview",
      response_format={ "type": "json_object" },
      messages=[
      {"role": "system", "content": "あなたは優秀なTRPGのGMです。ユーザーからのメッセージをもとに、シナリオの続きを作成してください。"},
      {"role": "user", "content": input}
      ]
    )

      #llamaIndexでJSONとしてステータスを出力
      #dbに送信、もしくは直接フロントエンドへ
    except Exception as e:
      raise e
      
''' プレイヤー状態更新用のJSONの例。コンテキストウインドウのことを考えて削ること。
{
  "status_change": {
    "STR_change": -10,
    "DEX_change": 5,
    "INT_change": 2,
    "AGI_change": 1,
    "LUCK_change": -8,
    "HP_change": 100,
    "SAN_change": 100
  },
  "conditions_change": {
    "add": {
      "poisoned": {
        "duration": 3,
        "effect": "HP decreases by 5 every turn"
      },
      "buffed": {
        "attribute": "STR",
        "increase": 5,
        "duration": 5
      }
    },
    "remove": {
      "weakened": {
        "duration": 0,
        "effect": "No longer affects the player"
      }
    }
  },
  "inventory_change": {
    "add": [
      {
        "name": "Mystic Scroll",
        "quantity": 1,
        "effect": "Unlocks secret magic when read"
      },
      {
        "name": "Healing Potion",
        "quantity": 2,
        "effect": "Restores 50 HP"
      }
    ],
    "remove": [
      {
        "name": "Old Sword",
        "quantity": 1,
        "reason": "Sold to merchant"
      }
    ],
    "update": [
      {
        "name": "Mana Potion",
        "quantity_change": 3,
        "new_total": 5,
        "effect": "Restores 30 MP"
      }
    ]
  }
}
'''