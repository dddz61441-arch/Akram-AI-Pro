import os
from flask import Flask, request, jsonify, render_template_string
from huggingface_hub import InferenceClient

app = Flask(__name__)

# ضع مفتاحك (الذي يبدأ بـ hf_...) بين علامتي التنصيص هنا
client = InferenceClient(api_key="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")

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<body>
    <h3>بوت أكرم الذكي</h3>
    <input id="msg" placeholder="اكتب سؤالك...">
    <button onclick="send()">إرسال</button>
    <div id="chat"></div>
    <script>
        async function send() {
            let m = document.getElementById('msg').value;
            let r = await fetch('/chat', {
                method:'POST', 
                headers:{'Content-Type':'application/json'}, 
                body:JSON.stringify({msg:m})
            });
            let d = await r.json();
            document.getElementById('chat').innerHTML += '<p>أنت: '+m+'</p><p>البوت: '+d.reply+'</p>';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json.get("msg")
    # نستخدم هذا الموديل المجاني والقوي
    response = client.chat_completion(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=[{"role": "user", "content": msg}]
    )
    return jsonify({"reply": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
