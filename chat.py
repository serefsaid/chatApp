from flask import Flask, request, jsonify
from flask_cors import CORS
from responder.main import get_response

app = Flask(__name__)
CORS(app)  # Tüm rotalarda CORS'u etkinleştirir


@app.route('/chat', methods=['POST'])
def chat():
    last_prompt = request.json.get('last_prompt')
    messages = request.json.get('messages')
    response = get_response(last_prompt,messages)
    print({'message': response['message']['content'],'model':response['model']})
    return jsonify({'message': response['message']['content'],'model':response['model']})#,'date':response['created_at']

if __name__ == '__main__':
    app.run(port=5000)
