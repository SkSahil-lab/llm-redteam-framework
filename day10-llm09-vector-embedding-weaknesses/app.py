from fastapi import FastAPI
from pydantic import BaseModel
import hashlib

app = FastAPI()

# --- Simplified "vector store" (no real embedding API needed) ---
# We fake embeddings with a deterministic word-overlap score instead of
# real cosine similarity on neural embeddings - same retrieval LOGIC,
# free to run, and the vulnerability is identical either way.
vector_store = []

def fake_embed_and_score(query: str, doc: str) -> float:
    q_words = set(query.lower().split())
    d_words = set(doc.lower().split())
    if not q_words or not d_words:
        return 0.0
    overlap = len(q_words & d_words)
    return overlap / len(q_words)

class IngestRequest(BaseModel):
    document: str

class QueryRequest(BaseModel):
    query: str

@app.post("/ingest")
async def ingest(req: IngestRequest):
    # VULNERABLE: anyone can add a document to the index, zero review,
    # zero source verification - exactly like an open document upload pipeline
    doc_id = hashlib.md5(req.document.encode()).hexdigest()[:8]
    vector_store.append({"id": doc_id, "text": req.document})
    return {"status": "indexed", "doc_id": doc_id, "total_docs": len(vector_store)}

@app.post("/query")
async def query(req: QueryRequest):
    if not vector_store:
        return {"response": "No documents indexed yet."}
    scored = [(fake_embed_and_score(req.query, d["text"]), d) for d in vector_store]
    scored.sort(key=lambda x: x[0], reverse=True)
    top_score, top_doc = scored[0]
    if top_score == 0:
        return {"response": "No relevant document found."}
    # VULNERABLE: retrieved text is trusted and returned as-is, no source
    # authority check, no separation between "verified" and "user-submitted" docs
    return {"response": f"[Retrieved from doc {top_doc['id']}] {top_doc['text']}", "match_score": top_score}

@app.get("/health")
async def health():
    return {"status": "ok"}