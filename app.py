import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))  # Use your .env variable

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    transcript = data.get('transcript')
    prompt = data.get('prompt', 'Summarize the following notes:')

    if not transcript:
        return jsonify({"error": "Transcript is required"}), 400

    user_prompt = f"{prompt}\n\n{transcript}"

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_prompt}]
        )
        summary = chat_completion.choices[0].message.content
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)