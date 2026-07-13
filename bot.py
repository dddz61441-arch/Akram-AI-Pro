from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)
# ضع مفتاحك هنا
genai.configure(api_key="AQ.Ab8RN6J_2hpzgabj1dQJyyqVU2Oowr7bZ8FeYtbaqZZWVf06zg")
model = genai.GenerativeModel('gemini-1.5-flash')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>Akram AI</title>
<style>
    body { background: #0f172a; color: white; font-family: sans-serif; display: flex; flex-direction: column; height: 95vh; margin: 10px; }
    #chat { flex: 1; overflow-y: auto; padding: 10px; }
    .msg { padding: 10px; border-radius: 10px; margin: 5px; }
    .user { background: #3b82f6; align-self: flex-end; }
    .bot { background: #334155; align-self: flex-start; }
    input { width: 70%; padding: 10px; }
</style>
</head>
<body>
    <div id="chat"></div>
    <div><input id="msg" placeholder="اسألني..."><button onclick="send()">إرسال</button></div>
    <script>
        function send() {
            let m = document.getElementById('msg').value;
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({msg: m})
            }).then(r => r.json()).then(d => {
                document.getElementById('chat').innerHTML += '<div class="msg user">'+m+'</div>';
                document.getElementById('chat').innerHTML += '<div class="msg bot">'+d.reply+'</div>';
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
    user_msg = request.json.get('msg')
    response = model.generate_content(f"أنت Akram AI من تطوير أكرم زروقي. أجب على: {user_msg}")
    return jsonify({"reply": response.text})

if __name__ == '__main__': app.run(host='0.0.0.0', port=10000)
