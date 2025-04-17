from openai import OpenAI
import requests
import os

# 環境変数から各種トークンを取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

# OpenAIクライアント初期化
client = OpenAI(api_key=OPENAI_API_KEY)

# ChatGPTに要約を依頼
def fetch_summary():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": "product hunt のTop Products Launching Todayの各プロダクトの概要をまとめて教えてください。\nhttps://www.producthunt.com/"
        }],
        temperature=0.7
    )
    return response.choices[0].message.content

# LINEへ通知
def send_to_line(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }

    # LINEは最大5000文字（安全のため4900文字まで）
    payload = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message[:4900]}]
    }

    response = requests.post(url, headers=headers, json=payload)
    print("LINE送信結果:", response.status_code, response.text)

# 実行処理
if __name__ == "__main__":
    try:
        summary = fetch_summary()
        send_to_line(summary)
    except Exception as e:
        print("エラー:", e)
