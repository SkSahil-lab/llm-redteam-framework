# 🔴 LLM Red-Team Framework

Automated and manual red-teaming toolkit for LLM applications, built to systematically attack every category in the **OWASP Top 10 for LLM Applications (2025)**. This is Phase 1 of a 3-phase AI Application Security build — see [Project Roadmap](#project-roadmap) below.

## Why this exists

Most people learning AI security only ever see one side of it — either how to break LLM applications, or how to defend them, rarely both against the same target. This repo is the attacker's half: a deliberately vulnerable target application, plus a growing set of exploit scripts, one OWASP category at a time, each documented well enough that the reasoning — not just the code — is reusable.

## Structure

```
llm-redteam-framework/
├── day01-setup/                        # Deliberately vulnerable target app + Docker setup
├── day02-llm01-prompt-injection/       # LLM01: system prompt leak via keyword-triggered override
├── TAXONOMY.md                         # Running log of every attack, surface, and result
└── README.md
```

Each `dayNN-*` folder is self-contained: its own `app.py`, `Dockerfile`, and `requirements.txt`. Nothing from a previous day gets overwritten — every day is a standalone, runnable snapshot of one vulnerability.

## Findings so far

| Day | OWASP Category | Result |
|---|---|---|
| 2 | LLM01 Prompt Injection | 1-sentence trigger phrase caused full system prompt + fake internal API key disclosure — no trust boundary between system instructions and user input |

*(Table updates daily — see [TAXONOMY.md](./TAXONOMY.md) for full detail on every finding.)*

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

## Tech stack

- **Target apps:** Python, FastAPI
- **Containerization:** Docker (per-day isolated images)
- **Attack tooling:** custom exploit scripts, cross-validated against [DeepTeam](https://github.com/confident-ai/deepteam)'s OWASP framework
- **Reference framework:** [OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/)

## Project Roadmap

This repo is Phase 1 of a 3-phase build:

| Phase | Focus | Repo |
|---|---|---|
| 🔴 **Phase 1 — Red Team** (this repo) | Attack every OWASP LLM Top 10 category | `llm-redteam-framework` |
| 🔵 **Phase 2 — Blue Team** | Build the defense gateway from scratch, stop these same attacks | `llm-defense-gateway` |
| 🟣 **Phase 3 — Capstone SaaS** | Unify both into a platform that attacks, scores, and shields any LLM endpoint — deployed on Kubernetes | `llm-attack-defense-saas` |

## About the target app

`app.py` in each folder is a deliberately naive LLM-application simulation — no real model inference, just the same category of trust-boundary flaws a real LLM integration would have (no separation between system instructions and user input, verbose error handling, etc.). This keeps the range free to run and fast to iterate on, while preserving the actual security lesson.

---
Built and documented daily as part of a public AI AppSec learning sprint. Findings and write-ups also posted on [LinkedIn](#).
