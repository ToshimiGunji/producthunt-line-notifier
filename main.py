import openai
import requests
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

def fetch_summary():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": "product hunt のTop Products Launching Todayの各プロダクトの概要をまとめて教えてください。\nhttps://www.producthunt.com/"
        }],
        temperature=0.7
    )
    return response.choices[0].message.content

def send_to_line(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message[:4900]}]
    }
    requests.post(url, headers=headers, json=data)

if __name__ == "__main__":
    summary = fetch_summary()
    send_to_line(summary)
