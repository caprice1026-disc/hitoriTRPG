from openai import OpenAI
# langchainだとJSONパースが微妙なことがおおい。
from llama-index  import llamaindex

#ダイスロール時のOpenAI呼び出しとステータス変化時のOpenAI呼び出しを違うものとして実装

def openai_call():
  try:
    # シナリオが長くなりすぎた際にまとめる処理(アシスタントAPIでも可)
    # OpenAIに、GMとしてシナリオの続きを書かせる
    #内容をreflesh_statusに渡してJSONでパースする処理
  except Exception as e:
    raise e
  
  def reflesh_status():
    try:
      #llamaIndexでJSONとしてステータスを出力
      #dbに送信、もしくは直接フロントエンドへ
    except Exception as e:
      raise e
      