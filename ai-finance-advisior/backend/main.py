from fastapi import FastAPI
from ai import get_ai_response
from memory import add_memory

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Finance Advisor Running 🚀"}

@app.get("/ask")
def ask(query: str):
    response = get_ai_response(query)
    add_memory(query, response)
    return {"response": response}