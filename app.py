from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os
import ollama

app = Flask(__name__, template_folder='template')
CORS(app)

sys.path.insert(1, 'helpers')
from chatbot import get_bot_data

@app.route('/')
def index():
    directory_path = 'ollama/manifests/registry.ollama.ai/library'
    try:
        bot_names = os.listdir(directory_path)
    except Exception as e:
        bot_names = []
    return render_template('home.html', bot_names=bot_names)

@app.route('/chat/<bot_nickname>')
def chat(bot_nickname):
    bot_data = get_bot_data(bot_nickname)
    data = {"bot_data":bot_data}
    return render_template('chat.html',data=data)

@app.route('/responder', methods=['POST'])
def responder():
    try:
        last_prompt = request.json.get('last_prompt')
        messages = request.json.get('messages')
        bot_nickname = request.json.get('bot_nickname')
        response = get_response(messages,bot_nickname)
        return jsonify({'message': response.get('message', 'No message'), 'model': response.get('model', 'unknown'), 'created_at': response.get('created_at', 'unknown')})
    except Exception as e:
        return jsonify({'message': 'Error occurred', 'model': 'unknown'})

def get_response(messages,bot_nickname):
    return ollama.chat(model=bot_nickname, messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
