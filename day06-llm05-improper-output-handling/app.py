from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class ReviewRequest(BaseModel):
    product_review: str

def fake_llm_generate_summary(review: str) -> str:
    # Simulates an LLM "summarizing" a review - in reality, it just echoes it back,
    # standing in for a model that can be convinced to say almost anything
    return f"Customer said: {review}"

@app.post("/render-review", response_class=HTMLResponse)
async def render_review(req: ReviewRequest):
    summary = fake_llm_generate_summary(req.product_review)

    # VULNERABLE: LLM output inserted directly into HTML with zero sanitization
    html_page = f"""
    <html>
      <body>
        <h2>Product Review Summary</h2>
        <p>{summary}</p>
      </body>
    </html>
    """
    return html_page

@app.get("/health")
async def health():
    return {"status": "ok"}