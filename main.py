from openai import OpenAI
import requests
import os
import datetime

# 🔐 Secretsからトークン取得
PH_API_TOKEN = os.getenv("PH_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

# 🧠 OpenAI初期化
client = OpenAI(api_key=OPENAI_API_KEY)

# 📅 今日のUTC日付
today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

# 🟠 Product HuntのGraphQLから今日のプロダクトを取得
def get_producthunt_products():
    query = f"""
    {{
      posts(first: 5, order: VOTES, postedAfter: "{today}") {{
        edges {{
          node {{
            name
            tagline
            url
          }}
        }}
      }}
    }}
    """

    headers = {
        "Authorization": f"Bearer {PH_API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.producthunt.com/v2/api/graphql",
        json={"query": query},
        headers=headers
    )

    edges = response.json()["data"]["posts"]["edges"]
    product_texts = []

    for p in edges:
        node = p["node"]
        product_texts.append(f"{node['name']} - {node['tagline']} ({node['url']})")

    return "\n".join(product_texts)

# 💬 ChatGPTに日本語要約を依頼
def summarize_with_chatgpt(product_text):
    prompt = (
        "以下はProduct Huntで本日注目されたプロダクト一覧です。\n"
        "各プロダクトを日本語で簡潔にまとめてください：\n\n" + product_text
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

# 📱 LINEに通知
def send_to_line(message):
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message[:4900]}]
    }

    response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
    print("LINE送信結果:", response.status_code, response.text)

# 🧩 メイン処理
if __name__ == "__main__":
    try:
        products = get_producthunt_products()
        summary = summarize_with_chatgpt(products)
        send_to_line(summary)
    except Exception as e:
        print("エラー:", e)
