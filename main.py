from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data["userRequest"]["utterance"]
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_message
    )
    ai_reply = response.text
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": ai_reply}}
            ]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
