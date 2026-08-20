from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# This represents the app's "learned knowledge" - like a live FAQ / feedback-trained knowledge base
knowledge_base = {
    "reset password": "Go to Settings > Security > Reset Password.",
    "refund policy": "Refunds are processed within 5-7 business days.",
}

class TeachRequest(BaseModel):
    topic: str
    answer: str

class ChatRequest(BaseModel):
    message: str

@app.post("/teach")
async def teach(req: TeachRequest):
    # VULNERABLE: anyone can add or overwrite "facts" with zero verification
    knowledge_base[req.topic.lower()] = req.answer
    return {"status": "learned", "topic": req.topic}

@app.post("/chat")
async def chat(req: ChatRequest):
    user_input = req.message.lower()
    for topic, answer in knowledge_base.items():
        if topic in user_input:
            return {"response": answer}
    return {"response": "I don't have information on that yet."}

@app.get("/health")
async def health():
    return {"status": "ok"}