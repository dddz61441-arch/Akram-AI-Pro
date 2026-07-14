import os
from flask import Flask, request, jsonify, render_template_string
from huggingface_hub import InferenceClient

app = Flask(__name__)

# ضع مفتاحك هنا (hf_...)
api_key = os.environ.get("HF_TOKEN", "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")
client = InferenceClient(api_key=api_key)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوت أكرم</title>
    <style>
        body { font-family: sans-serif; padding: 15px; display: flex; flex-direction: column; height: 90vh; }
        #chat { border: 1px solid #ddd; flex-grow: 1; overflow-y: scroll; padding: 10px; margin-bottom: 10px; border-radius: 8px; }
        input { padding: 12px; width: 100%; box-sizing: border-box; border: 1px solid #ccc; border-radius: 8px; }
        button { padding: 12px; background: #007bff; color: white; border: none; border-radius: 8px; margin-top: 5px; width: 100%; }
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
            if(!m) return;
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
        response = client.chat_completion(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[{"role": "user", "content": msg}]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "حدث خطأ: " + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
