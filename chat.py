from flask import Flask, request, jsonify
from flask_cors import CORS
from responder.main import get_response

app = Flask(__name__)
CORS(app)  # Tüm rotalarda CORS'u etkinleştirir


@app.route('/chat', methods=['POST'])
def chat():
    last_prompt = request.json.get('last_prompt')
    messages = request.json.get('messages')
    response_message = f"{get_response(last_prompt,messages)}"
    return jsonify({'response': response_message})

if __name__ == '__main__':
    app.run(port=5000)
