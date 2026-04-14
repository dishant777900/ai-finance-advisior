import os
import requests
from dotenv import load_dotenv
from memory import get_memory

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_ai_response(user_input):
    past = get_memory()

    # Build memory context
    context = ""
    for item in past:
        context += f"User: {item['input']}\nAI: {item['response']}\n"

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen/qwen3-32b",
        "messages": [
            {
                "role": "system",
                "content": "You are a finance advisor. Always speak directly using 'you'. Give only 3-4 short bullet points. No paragraphs. No explanations."
            },
            {
                "role": "user",
                "content": context + "\nUser: " + user_input
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return f"Error: {response.text}"

    result = response.json()
    answer = result["choices"][0]["message"]["content"]

    # 🔥 FORCE CLEAN OUTPUT
    lines = answer.split("\n")
    final = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # replace "they" with "you"
        line = line.replace("they", "you")
        line = line.replace("The user", "You")

        # ensure bullet format
        if not line.startswith("-"):
            line = "- " + line

        final.append(line)

    return "\n".join(final[:4])  # limit to 4 points