memory_store = []

def add_memory(user_input, ai_response):
    memory_store.append({
        "input": user_input,
        "response": ai_response
    })

def get_memory():
    return memory_store[-3:]  # last 3 interactions