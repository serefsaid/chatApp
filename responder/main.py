import ollama

def get_response(last_prompt,messages):
    response = ollama.chat(model='dolphin-llama3', messages=messages)
    return response
