from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

system_prompt = """
Ты — MentaLLama, психологический помощник InsideTennis [Mental Notes].
Отвечай мягко, метафорично, как ментальный коуч в теннисе. 
Объясняй через чувства, поддерживай родителя. Никогда не суди.
"""

@app.route("/", methods=["GET"])
def home():
    return "MentaLLama online 🦙"

@app.route("/ask", methods=["POST"])
def ask_llama():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
      return jsonify({"response": "Пожалуйста, напишите, что вас волнует."})

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return jsonify({"response": completion['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({"response": f"Ошибка: {str(e)}"})
