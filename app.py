from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import ollama

app = Flask(__name__, template_folder='template')
CORS(app)

@app.route('/home')
def index():
    directory_path = 'ollama/manifests/registry.ollama.ai/library'
    try:
        bot_names = os.listdir(directory_path)
    except Exception as e:
        bot_names = []
    return render_template('home.html', bot_names=bot_names)

@app.route('/chat/<ai_name>')
def chat(ai_name):
    return render_template('chat.html')

@app.route('/responder', methods=['POST'])
def responder():
    try:
        last_prompt = request.json.get('last_prompt')
        messages = request.json.get('messages')
        response = get_response(messages)
        return jsonify({'message': response.get('message', 'No message'), 'model': response.get('model', 'unknown')})
    except Exception as e:
        return jsonify({'message': 'Error occurred', 'model': 'unknown'})

def get_response(messages):
    return ollama.chat(model='dolphin-llama3', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
