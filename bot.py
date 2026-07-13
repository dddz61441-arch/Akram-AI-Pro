import os
from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# إعداد مفتاح الـ API (يجب وضعه في إعدادات Render)
api_key = os.environ.get("AQ.Ab8RN6J_2hpzgabj1dQJyyqVU2Oowr7bZ8FeYtbaqZZWVf06zg")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

HTML_CODE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<body>
    <div id="chat"></div>
    <input id="msg" placeholder="اكتب رسالتك...">
    <button onclick="send()">إرسال</button>
    <script>
        function send() {
            let m = document.getElementById('msg').value;
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({msg: m})
            }).then(r => r.json()).then(d => {
                document.getElementById('chat').innerHTML += '<p>أنت: ' + m + '</p>';
                document.getElementById('chat').innerHTML += '<p>البوت: ' + d.reply + '</p>';
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_CODE)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("msg")
    try:
        response = model.generate_content(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "خطأ في الاتصال بجوجل، تأكد من مفتاح الـ API."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
