from flask import Flask, render_template, request, jsonify,redirect,session
from flask_cors import CORS
import sys
import os
import ollama

app = Flask(__name__, template_folder='template')
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')
CORS(app)

sys.path.insert(1, 'database')
from chatbot_db import get_bot_data
from chat_db import insert_message,get_chat_history,clear_chat_history
from users_db import add_to_used_chatbots,get_used_chatbots,check_user

sys.path.insert(1, 'helpers')
from functions_helpers import parse_json,hash_password
from session_helpers import get_session_user_id, is_user_logged_in,clear_session

@app.route('/')
def index():
    directory_path = 'ollama/manifests/registry.ollama.ai/library'
    try:
        bot_names = os.listdir(directory_path)
    except Exception as e:
        bot_names = []
    return render_template('home.html', bot_names=bot_names)

@app.route('/login')
def login_page():
    redirectTo = request.args.get('redirectTo', '')
    data = {"redirectTo":redirectTo}
    return render_template('login.html', data=data)

@app.route('/login_action', methods=['POST'])
def login_action():
    if 'username' in session:
        return jsonify({"type":"error","response":"you have already logged in!"})
    user = check_user(request.form['username'],hash_password(request.form['password']))
    if user:
        session['user_data'] = parse_json(user)
        redirectTo = '/'
        if request.form['redirectTo']:
            redirectTo = request.form['redirectTo']
        return redirect(redirectTo)
    else:
        return redirect("/login")

@app.route('/logout')
def logout():
    clear_session()
    return redirect('/')

@app.route('/chat/<model_nickname>')
def chat(model_nickname):
    if not is_user_logged_in():
        return redirect("/login?redirectTo=/chat/"+model_nickname)
    bot_data = get_bot_data(model_nickname)
    add_to_used_chatbots(bot_data["_id"])
    used_chatbots = parse_json(get_used_chatbots())
    chat_history = parse_json(get_chat_history(model_nickname))
    data = {"bot_data":bot_data,"used_chatbots":used_chatbots,"chat_history":chat_history}
    return render_template('chat.html',data=data)

@app.route('/clear_model_chat_history', methods=['POST'])
def clear_model_chat_history():
    result = clear_chat_history(request.json.get('bot_nickname'))
    return parse_json({"result":result})
@app.route('/responder', methods=['POST'])
def responder():
    try:
        response = get_response(request.json.get('messages'),request.json.get('bot_nickname'))
        insert_message(request.json.get('last_prompt'),response,request.json.get('date'))
        return jsonify({'message': response.get('message', 'No message'), 'model': response.get('model', 'unknown'), 'created_at': response.get('created_at', 'unknown')})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error occurred', 'model': 'unknown'})

def get_response(messages,bot_nickname):
    return ollama.chat(model=bot_nickname, messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
