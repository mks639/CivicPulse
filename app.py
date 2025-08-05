from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

import os
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/report", methods=["POST"])
def report_issue():
    data = request.get_json()
    user_input = data["user_input"]

    prompt = f"""
    Analyze the following civic issue reported by a citizen. Provide a summary, possible cause, and recommend which authority (e.g., municipal, PWD, water board) should handle it. Be concise and use bullet points.

    Issue: {user_input}
    """

    response = model.generate_content(prompt)
    return jsonify({"response": response.text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # fallback for local use
    app.run(host="0.0.0.0", port=port)
