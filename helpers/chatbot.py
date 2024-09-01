import json

def get_bot_data(bot_nickname):
    file_path = f'ollama/models/{bot_nickname}/data.json'

    with open(file_path, 'r') as file:
        data = json.load(file)

    return data