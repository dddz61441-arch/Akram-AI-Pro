from flask import Flask, request, jsonify, render_template_string
import g4f

app = Flask(__name__)

# [هنا ضع كود HTML الذي صممناه سابقاً كما هو دون تغيير]
# (تأكد أن لا تكون هناك أي كلمة عربية داخل الأكواد البرمجية بالإنجليزية)

@app.route('/chat', methods=['POST'])
def chat():
    m = request.json.get('msg')
    try:
        # استخدام طريقة مباشرة أكثر استقراراً
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": m}],
        )
        return jsonify({"reply": response})
    except Exception as e:
        return jsonify({"reply": "الخادم مشغول الآن، انتظر لحظة وأرسل مرة أخرى."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
