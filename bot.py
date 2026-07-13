import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# إعداد مفتاح الـ API من إعدادات Render
api_key = os.environ.get("AQ.Ab8RN6J_2hpzgabj1dQJyyqVU2Oowr7bZ8FeYtbaqZZWVf06zg")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "عذراً، لم أستلم أي رسالة."})
    
    try:
        # إرسال الرسالة لـ Gemini
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "حدث خطأ تقني، تأكد من مفتاح الـ API."})

if __name__ == '__main__':
    # Render يحتاج أن يعمل الكود على المنفذ الذي يحدده هو
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
