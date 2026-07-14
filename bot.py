import os
from flask import Flask, request, jsonify, render_template_string
from huggingface_hub import InferenceClient

app = Flask(__name__)
# التأكد من سحب المفتاح من إعدادات Render
client = InferenceClient(api_key=os.environ.get("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"))

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .msg { padding: 15px; border-radius: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); max-width: 85%; }
        .user { align-self: flex-end; background: #3b82f6; }
        .bot { align-self: flex-start; background: #1e293b; }
        .input-area { padding: 20px; background: rgba(0,0,0,0.2); display: flex; gap: 10px; }
        input { flex: 1; background: #334155; border: none; padding: 15px; border-radius: 15px; color: white; }
        button { background: #3b82f6; border: none; padding: 10px 20px; border-radius: 15px; color: white; cursor: pointer; }
        .typing { font-size: 0.8em; color: #94a3b8; margin-top: 5px; }
    </style>
</head>
<body>
    <div id="chat"></div>
    <div class="input-area">
        <input id="msg" placeholder="اكتب سؤالك هنا..." onkeydown="if(event.key==='Enter') send()">
        <button onclick="send()">إرسال</button>
    </div>
"""
    <script>
        async function send() {
            let m = document.getElementById('msg').value;
            if(!m) return;
            let chat = document.getElementById('chat');
            chat.innerHTML += `<div class="msg user">أنت: ${m}</div>`;
            document.getElementById('msg').value = '';
            chat.innerHTML += `<div id="typing" class="typing">Akram AI يفكر...</div>`;
            
            let r = await fetch('/chat', {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({msg: m})
            });
            document.getElementById('typing').remove();
            let d = await r.json();
            chat.innerHTML += `<div class="msg bot" onclick="copyText(this)">البوت: ${d.reply}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }
        function copyText(el) { navigator.clipboard.writeText(el.innerText); alert('تم النسخ!'); }
    </script>
</body>
</html>
"""@app.route('/')
def home(): return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        msg = request.json.get("msg")
        response = client.chat_completion(
            model="HuggingFaceH4/zephyr-7b-beta",
            messages=[{"role": "user", "content": msg}]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except:
        return jsonify({"reply": "عذراً، حدث خطأ تقني. حاول مرة أخرى."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

