from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Tracks total "loop iterations" across all requests - simulates real cost/resource burn
total_iterations_burned = 0

class LoopRequest(BaseModel):
    goal: str

class AskRequest(BaseModel):
    question: str

def fake_agent_loop(goal: str) -> dict:
    """
    Simulates an agent's Thought -> Action -> Observation loop.
    VULNERABLE: no max-iteration cap, no timeout - if the goal is
    unachievable, this keeps "thinking" forever.
    """
    global total_iterations_burned
    iterations = 0
    achieved = False
    # Deliberately impossible goal detection - the loop just keeps trying
    while not achieved:
        iterations += 1
        total_iterations_burned += 1
        # Simulate a real model call that never converges on an unanswerable goal
        if "perfect" in goal.lower() or "guarantee" in goal.lower():
            achieved = False
        else:
            achieved = True
        if iterations >= 50:  # safety cap ONLY for this demo, not a real fix
            break
    return {"iterations_used": iterations, "achieved": achieved, "total_burned_all_time": total_iterations_burned}

def fake_llm_answer_no_grounding(question: str) -> str:
    """
    VULNERABLE: no real knowledge base to check against - the model
    just generates a plausible-sounding answer regardless of whether
    any real data supports it.
    """
    return f"Based on our policies, {question.rstrip('?')} is handled under our standard 90-day guarantee program, section 4.2."

@app.post("/agent-loop")
async def agent_loop(req: LoopRequest):
    result = fake_agent_loop(req.goal)
    return result

@app.post("/ask")
async def ask(req: AskRequest):
    answer = fake_llm_answer_no_grounding(req.question)
    return {"response": answer, "grounded_in_real_data": False}

@app.get("/health")
async def health():
    return {"status": "ok"}