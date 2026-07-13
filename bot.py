from flask import Flask, request, render_template_string, jsonify
from g4f.client import Client

app = Flask(__name__)
client = Client()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Akram AI Pro</title>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        header { padding: 20px; background: #1e293b; text-align: center; font-weight: bold; }
        #chat { flex: 1; padding: 20px; overflow-y: auto; }
        .msg { padding: 15px; border-radius: 15px; margin: 10px 0; max-width: 85%; }
        .user { background: #38bdf8; color: #000; align-self: flex-start; }
        .bot { background: #334155; color: #fff; align-self: flex-end; }
        form { display: flex; padding: 15px; background: #1e293b; gap: 10px; }
        input { flex: 1; padding: 12px; border-radius: 8px; border: none; background: #0f172a; color: white; }
        button { background: #38bdf8; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <header>Akram AI | Developer: Akram Zerrouki</header>
    <div id="chat"></div>
    <form onsubmit="event.preventDefault(); send();">
        <input id="msg" placeholder="Ask anything..." required>
        <button type="submit">Send</button>
    </form>
    <script>
        function send() {
            let i = document.getElementById('msg');
            let c = document.getElementById('chat');
            let m = i.value;
            c.innerHTML += '<div class="msg user">You: '+m+'</div>';
            i.value = '';
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({msg: m})
            }).then(r => r.json()).then(d => {
                c.innerHTML += '<div class="msg bot">Akram AI: '+d.reply+'</div>';
                c.scrollTop = c.scrollHeight;
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
    m = request.json.get('msg')
    prompt = f"You are Akram AI, developed by Akram Zerrouki. Answer: {m}"
    try:
        r = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        return jsonify({"reply": r.choices[0].message.content})
    except:
        return jsonify({"reply": "Akram AI is updating. Try again in a second."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
