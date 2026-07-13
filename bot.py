from flask import Flask, request, render_template_string, jsonify
from g4f.client import Client

app = Flask(__name__)
client = Client()

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html dir="rtl">
    <body>
        <div id="chat"></div>
        <input id="msg">
        <button onclick="send()">إرسال</button>
        <script>
            function send() {
                let m = document.getElementById('msg').value;
                fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({msg: m})
                })
                .then(r => r.json())
                .then(d => {
                    document.getElementById('chat').innerHTML += '<p>البوت: '+d.reply+'</p>';
                });
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('msg')
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": msg}]
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "خطأ: " + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
