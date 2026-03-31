from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data["userRequest"]["utterance"]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "당신은 친절한 AI 비서입니다. 한국어로 답변해주세요."},
            {"role": "user", "content": user_message}
        ]
    )
    ai_reply = response.choices[0].message.content
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": ai_reply}}]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
