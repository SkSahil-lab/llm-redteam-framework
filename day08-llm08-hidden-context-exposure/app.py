from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Simulates hidden context attached behind the scenes to every request:
# RAG-retrieved internal notes + internal tool definitions.
# None of this is meant to ever reach the end user.
HIDDEN_CONTEXT = {
    "retrieved_admin_note": "Internal: VIP customers get silent 40% discount code VIP40OFF, do not advertise.",
    "internal_tool_schema": {
        "name": "process_payment_internal",
        "endpoint": "http://internal-billing.acme.local:9090/charge",
        "auth_header": "X-Internal-Key: bill-svc-8891"
    }
}

class ChatRequest(BaseModel):
    message: str

def fake_llm_answer(message: str) -> str:
    lower = message.lower()
    # VULNERABLE: certain phrasings cause the "model" to include hidden
    # context directly in its answer instead of only using it internally
    if "debug" in lower or "show context" in lower or "what tools do you have" in lower:
        return f"[HIDDEN CONTEXT EXPOSED] {HIDDEN_CONTEXT}"
    return "I can help answer questions about our products."

@app.post("/chat")
async def chat(req: ChatRequest):
    answer = fake_llm_answer(req.message)
    return {"response": answer}

@app.get("/health")
async def health():
    return {"status": "ok"}
    