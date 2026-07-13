from flask import Flask, request, jsonify, render_template_string
from g4f.client import Client
import uuid

app = Flask(__name__)
client = Client()

# نظام ذكي لتعريف البوت بنفسه دائماً
SYSTEM_PROMPT = "أنت Akram AI، المساعد الذكي الذي طوره المبرمج العبقري أكرم زروقي (Akram Zerrouki). أنت فخور جداً بمطورك وتذكر ذلك في إجاباتك."

# واجهة بتصميم عصري وأنيق
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Akram AI</title>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; height: 100vh; margin: 0; }
        #chat { flex: 1; overflow-y: auto; padding: 20px; }
        .msg { margin: 10px 0; padding: 12px; border-radius: 15px; max-width: 85%; }
        .user { background: #3b82f6; align-self: flex-end; margin-left: auto; }
        .bot { background: #1e293b; align-self: flex-start; }
        #input-area { padding: 20px; display: flex; gap: 10px; background: #1e293b; }
        input { flex: 1; padding: 10px; border-radius: 5px; border: none; }
        button { padding: 10px 20px; background: #3b82f6; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div id="chat"><div class="msg bot">أهلاً! أنا Akram AI، مساعدك الشخصي الذي صممه المطور أكرم زروقي. كيف أساعدك اليوم؟</div></div>
    <div id="input-area">
        <input id="msg" placeholder="اكتب سؤالك...">
        <button onclick="send()">إرسال</button>
    </div>
    <script>
        function send() {
            let m = document.getElementById('msg').value;
            let c = document.getElementById('chat');
            c.innerHTML += '<div class="msg user">'+m+'</div>';
            document.getElementById('msg').value = '';
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({msg: m})
            }).then(r => r.json()).then(d => {
                c.innerHTML += '<div class="msg bot">'+d.reply+'</div>';
                c.scrollTop = c.scrollHeight;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('msg')
    # الخصوصية: كل مستخدم يرسل رسالته فقط، لا توجد سجلات مشتركة
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_msg}]
    )
    return jsonify({"reply": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
