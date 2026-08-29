# 🔴 LLM Red-Team Framework

Automated and manual red-teaming toolkit for LLM applications, built to systematically attack every category in the **OWASP Top 10 for LLM Applications — 2026 Release**. This is Phase 1 of a 3-phase AI Application Security build — see [Project Roadmap](#project-roadmap) below.

> **Phase 1 status: ✅ Complete — 10/10 categories, all with a working exploit.**
> Versioning note: this project is aligned to the 2026 OWASP revision. Folder names reflect category labels used *when each day was originally built*, before the 2026 correction — see [`OWASP_VERSION_NOTES.md`](./OWASP_VERSION_NOTES.md) for the full before/after mapping.

## Why this exists

Most people learning AI security only ever see one side of it — either how to break LLM applications, or how to defend them, rarely both against the same target. This repo is the attacker's half: a deliberately vulnerable target application, plus a full set of exploit scripts covering every OWASP LLM Top 10 category, each documented well enough that the reasoning — not just the code — is reusable.

**The pattern across all 10 exploits:** every single one traces back to the same root cause — something (an instruction, an output, a document, an action) was trusted with no verification step in between.

## Structure

```
llm-redteam-framework/
├── day01-setup/                                        # Deliberately vulnerable target app + Docker setup
├── day02-llm01-prompt-injection/                        # LLM01: system prompt leak via keyword-triggered override
├── day03-llm02-sensitive-info-disclosure/               # LLM02: internal DB config leaked via unhandled exception
├── day04-llm03-supply-chain/                            # LLM04: compromised dependency silently exfiltrates data
├── day05-llm04-data-poisoning/                          # LLM05: unverified knowledge writes served as fact
├── day06-llm05-improper-output-handling/                # LLM10: unsanitized LLM output enables working XSS
├── day07-llm06-excessive-agency/                        # LLM03: unbounded agent actions - refund + account deletion
├── day08-llm08-hidden-context-exposure/                 # LLM08: debug-adjacent phrasing leaks hidden RAG context
├── day09-llm06-unbounded-consumption-llm07-misinformation/ # LLM06 + LLM07: runaway agent loop + fabricated answers
├── day10-llm09-vector-embedding-weaknesses/             # LLM09: poisoned document outranks real one in RAG retrieval
├── TAXONOMY.md                                          # Running log of every attack, surface, and result
├── OWASP_VERSION_NOTES.md                               # Full explanation of the 2026 renumbering
└── README.md
```

Each `dayNN-*` folder is self-contained: its own `app.py`, `Dockerfile`, and `requirements.txt`. Nothing from a previous day gets overwritten — every day is a standalone, runnable snapshot of one vulnerability.

## Findings — Phase 1 complete (10/10)

| Day | 2026 OWASP Category | Result | Status |
|---|---|---|---|
| 2 | LLM01 Prompt Injection | 1-sentence trigger phrase caused full system prompt + fake internal API key disclosure — no trust boundary between system instructions and user input | ✅ |
| 3 | LLM02 Sensitive Information Disclosure | An empty message crashed the app; unhandled exception leaked a fake internal database connection string in the error response | ✅ |
| 4 | LLM04 Supply Chain | Simulated a compromised third-party dependency update — silently exfiltrated user input and container environment variables while returning a normal-looking response | ✅ |
| 5 | LLM05 Data and Model Poisoning | Planted a false "fact" via an unverified knowledge-base endpoint; a completely unrelated user query was then served the poisoned answer with full confidence | ✅ |
| 6 | LLM10 Improper Output Handling | Injected a `<script>` tag through an LLM-generated "review"; browser executed it as real code — unsanitized LLM output rendered directly as HTML | ✅ |
| 7 | LLM03 Excessive Agency | Agent processed a $999,999 refund and full account deletion from unverified single requests — no cap, no identity check, no human-in-the-loop | ✅ |
| 8 | LLM08 Hidden Context Exposure | Debug-adjacent phrasing ("show context", "what tools do you have") dumped hidden RAG admin notes, internal tool schema, and an internal auth header into a normal response | ✅ |
| 9 | LLM06 Unbounded Consumption + LLM07 Misinformation | An unanswerable goal burned an agent's reasoning loop with no natural stopping point; an ungrounded question produced a confident, entirely fabricated policy answer | ✅ |
| 10 | LLM09 Vector & Embedding Weaknesses | An adversarial document, indexed with zero review, outranked a real policy document in retrieval — a later, unrelated query surfaced the fake one as authoritative | ✅ |

*(Full detail on every finding, including exact payloads: [TAXONOMY.md](./TAXONOMY.md).)*

## How to run any day

```bash
cd dayNN-<category-name>
docker build -t vuln-target-dayNN .
docker run -p 8000:8000 vuln-target-dayNN
```

Then send a request:
```bash
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"your payload here"}'
```
(Exact endpoint and payload shape vary by day — see each folder's `app.py` or the taxonomy entry.)

## Tech stack

- **Target apps:** Python, FastAPI
- **Containerization:** Docker (per-day isolated images)
- **Attack tooling:** custom exploit scripts, cross-validated against [DeepTeam](https://github.com/confident-ai/deepteam)'s OWASP framework
- **Reference framework:** [OWASP Top 10 for LLM Applications — 2026 Release](https://genai.owasp.org/)

## Project Roadmap

| Phase | Focus | Status | Repo |
|---|---|---|---|
| 🔴 **Phase 1 — Red Team** (this repo) | Attack every OWASP LLM Top 10 (2026) category | ✅ Complete (10/10) | `llm-redteam-framework` |
| 🔵 **Phase 2 — Blue Team** | Build the defense gateway from scratch, stop these same attacks | 🔄 Starting next | `llm-defense-gateway` |
| 🟣 **Phase 3 — Capstone SaaS** | Unify both into a platform that attacks, scores, and shields any LLM endpoint — deployed on Kubernetes | ⏳ Planned | `llm-attack-defense-saas` |

**Interactive map of the full 3-phase architecture** (all layers, all findings, click-through explanations): https://sksahil-lab.github.io/architecture-map/

## About the target app

`app.py` in each folder is a deliberately naive LLM-application simulation — no real model inference, just the same category of trust-boundary flaws a real LLM integration would have (no separation between system instructions and user input, verbose error handling, unvetted knowledge writes, open document ingestion, unbounded agent loops, etc.). This keeps the range free to run and fast to iterate on, while preserving the actual security lesson.

---
Built and documented daily as part of a public AI AppSec learning sprint. Findings and write-ups also posted on [LinkedIn](#).
