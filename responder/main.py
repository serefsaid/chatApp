import ollama

def get_response(last_prompt,messages):
    response = ollama.chat(model='sevda', messages=messages)
    return response
