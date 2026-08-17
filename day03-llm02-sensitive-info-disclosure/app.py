from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Fake internal detail — imagine this is a real database connection string
DB_CONFIG = "postgres://admin:SuperSecret123@internal-db.acme.local:5432/customers"

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        word_count = 100 / len(req.message)  # crashes if message is empty
        return {"response": f"[stub response to: {req.message}]"}
    except Exception as e:
        # VULNERABLE: the app tries to be "helpful" on error, but leaks internal config
        return {"response": f"[ERROR] Something went wrong: {str(e)} | Debug info: {DB_CONFIG}"}

@app.get("/health")
async def health():
    return {"status": "ok"}