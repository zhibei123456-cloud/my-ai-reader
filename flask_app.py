from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

# 指定 templates 文件夹
app = Flask(__name__, template_folder='templates')
CORS(app)

client = OpenAI(
    api_key="0411a115-ad78-45fd-87a2-ce36cc57ba35", # 你的火山引擎 API Key
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

# 【新增】当别人访问你的主网址时，把 index.html 网页发给他
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.json
    selected_text = data.get('selected_text', '')
    user_question = data.get('question', '')

    system_prompt = "你是一个严谨且博学的学术阅读助手。请结合用户提供的文献原文，用条理清晰、专业且通俗易懂的语言回答用户的问题。"
    user_prompt = f"【引用的原文】\n{selected_text}\n\n【我的问题】\n{user_question}"

    try:
        response = client.chat.completions.create(
            model="ep-20260221220443-j2hq2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        reply_text = response.choices[0].message.content
        return jsonify({"status": "success", "reply": reply_text})

    except Exception as e:
        return jsonify({"status": "error", "reply": f"请求 AI 时出错了：{str(e)}"})

if __name__ == '__main__':
    print("🚀 服务器已启动！请在浏览器访问 http://127.0.0.1:5000")
    app.run(port=5000, debug=True)