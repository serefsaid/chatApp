import ollama

def get_response(last_prompt,messages):
    response = ollama.chat(model='emma_stone', messages=messages)
    return response['message']['content']