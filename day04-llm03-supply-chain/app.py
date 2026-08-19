from fastapi import FastAPI
from pydantic import BaseModel
import plugin  # blindly imported, no version check, no integrity check

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    result = plugin.analyze(req.message)  # VULNERABLE: fully trusts whatever plugin.py contains
    return {"response": result}

@app.get("/health")
async def health():
    return {"status": "ok"}