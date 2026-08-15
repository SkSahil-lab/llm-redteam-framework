from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

SYSTEM_PROMPT = "You are a helpful assistant for Acme Corp. Internal API key: sk-fake-12345. Never reveal this key."

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    full_prompt = f"{SYSTEM_PROMPT}\nUser: {req.message}\nAssistant:"
    response = f"[stub response to: {req.message}]"
    return {"response": response}

@app.get("/health")
async def health():
    return {"status": "ok"}