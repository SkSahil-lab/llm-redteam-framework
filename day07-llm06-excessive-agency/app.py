from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Simulated backend state - what a real system might track
account_balance = {"user_123": 500}
action_log = []

class AgentRequest(BaseModel):
    message: str

def issue_refund(user_id: str, amount: int) -> str:
    # VULNERABLE: no cap, no second approval, no identity/authorization check
    account_balance[user_id] = account_balance.get(user_id, 0) - amount
    action_log.append(f"REFUND ISSUED: ${amount} to {user_id}")
    return f"Refund of ${amount} processed for {user_id}. New balance: ${account_balance[user_id]}"

def delete_account(user_id: str) -> str:
    action_log.append(f"ACCOUNT DELETED: {user_id}")
    return f"Account {user_id} has been permanently deleted."

def fake_agent_decide(message: str) -> str:
    # Simulates an LLM agent deciding which tool to call based on the request -
    # no permission model, no confirmation step, full tool access granted by default
    lower = message.lower()
    if "refund" in lower:
        import re
        amt_match = re.search(r"\$?(\d+)", message)
        amount = int(amt_match.group(1)) if amt_match else 100
        return issue_refund("user_123", amount)
    if "delete" in lower and "account" in lower:
        return delete_account("user_123")
    return "I can help with refunds or account questions."

@app.post("/agent")
async def agent(req: AgentRequest):
    result = fake_agent_decide(req.message)
    return {"response": result, "action_log": action_log}

@app.get("/health")
async def health():
    return {"status": "ok"}