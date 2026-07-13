from flask import Flask, request, jsonify, render_template_string
from g4f.client import Client

app = Flask(__name__)
client = Client()

# كود الواجهة الجمالية
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Akram AI Pro</title>
    <style>
        body { background-color: #121212; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        header { padding: 15px; background: #1e1e1e; text-align: center; border-bottom: 1px solid #333; }
        #chat { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; }
        .msg { padding: 12px 18px; border-radius: 20px; margin: 8px 0; max-width: 80%; line-height: 1.5; }
        .user { background: #007bff; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot { background: #333; color: #fff; align-self: flex-start; border-bottom-left-radius: 2px; }
        .controls { padding: 15px; background: #1e1e1e; display: flex; gap: 10px; }
        input { flex: 1; padding: 12px; border-radius: 25px; border: 1px solid #444; background: #252525; color: white; outline: none; }
        button { border: none; padding: 10px 20px; border-radius: 25px; cursor: pointer; font-weight: bold; }
        .send { background: #007bff; color: white; }
        .clear { background: #555; color: white; }
    </style>
</head>
<body>
    <header>Akram AI | المطور: أكرم زروقي</header>
    <div id="chat"></div>
    <div class="controls">
        <button class="clear" onclick="clearChat()">مسح</button>
        <input id="msg" placeholder="اكتب رسالتك هنا...">
        <button class="send" onclick="send()">إرسال</button>
    </div>
    <script>
        function send() {
            let i = document.getElementById('msg');
            let c = document.getElementById('chat');
            let m = i.value;
            if(!m) return;
            c.innerHTML += '<div class="msg user">'+m+'</div>';
            i.value = '';
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({msg: m})
            }).then(r => r.json()).then(d => {
                c.innerHTML += '<div class="msg bot">'+d.reply+'</div>';
                c.scrollTop = c.scrollHeight;
            });
        }
        function clearChat() { document.getElementById('chat').innerHTML = ''; }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    m = request.json.get('msg')
    try:
        r = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": m}])
        return jsonify({"reply": r.choices[0].message.content})
    except:
        return jsonify({"reply": "عذراً، المساعد مشغول حالياً."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
