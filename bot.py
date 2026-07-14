import os
from flask import Flask, request, jsonify, render_template_string
from huggingface_hub import InferenceClient

app = Flask(__name__)
# تأكد من أنك وضعت المفتاح هنا، أو في إعدادات Render باسم HF_TOKEN
client = InferenceClient(token=os.environ.get("HF_TOKEN", "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"))

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; padding: 20px; }
        #chat { border: 1px solid #ccc; height: 300px; overflow-y: scroll; margin-bottom: 10px; padding: 10px; }
        input { width: 70%; padding: 10px; }
        button { padding: 10px; }
    </style>
</head>
<body>
    <h3>بوت أكرم الذكي</h3>
    <div id="chat"></div>
    <input id="msg" placeholder="اكتب سؤالك هنا...">
    <button onclick="send()">إرسال</button>
    <script>
        async function send() {
            let msgInput = document.getElementById('msg');
            let chat = document.getElementById('chat');
            let m = msgInput.value;
            chat.innerHTML += '<p><b>أنت:</b> ' + m + '</p>';
            msgInput.value = '';
            
            let r = await fetch('/chat', {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({msg: m})
            });
            let d = await r.json();
            chat.innerHTML += '<p><b>البوت:</b> ' + d.reply + '</p>';
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        msg = request.json.get("msg")
        response = client.text_generation(msg, model="mistralai/Mistral-7B-Instruct-v0.3")
        return jsonify({"reply": response})
    except Exception as e:
        return jsonify({"reply": "حدث خطأ: " + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
