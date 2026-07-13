import os
from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# وضع مفتاحك مباشرة (حل مؤقت لنتأكد من عمله)
genai.configure(api_key="AQ.Ab8RN6KxP4UtJOBLHTScRcBBQD2tBPifRk_qIu7EHGXOez8XCw")
model = genai.GenerativeModel('gemini-1.5-flash')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>Akram AI</title></head>
<body>
    <div id="chat"></div>
    <input id="msg" placeholder="اكتب سؤالك...">
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
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json.get("msg")
    try:
        response = model.generate_content(msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "خطأ في الاتصال، تأكد من المفتاح في الكود."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
