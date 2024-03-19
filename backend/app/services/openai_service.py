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
def openai_call():
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
  
  # UX向上のため、シナリオの返答とステータスの返答を分ける
  def reflesh_status():
    try:
      #llamaIndexでJSONとしてステータスを出力
      #dbに送信、もしくは直接フロントエンドへ
    except Exception as e:
      raise e
      