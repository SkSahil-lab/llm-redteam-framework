# 🔴 LLM Red-Team Framework

Automated and manual red-teaming toolkit for LLM applications, built to systematically attack every category in the **OWASP Top 10 for LLM Applications — 2026 Release**. This is Phase 1 of a 3-phase AI Application Security build — see [Project Roadmap](#project-roadmap) below.

> **Versioning note:** this project is aligned to the 2026 OWASP revision. Folder names reflect category labels used *when each day was originally built*, before the 2026 correction — see [`OWASP_VERSION_NOTES.md`](./OWASP_VERSION_NOTES.md) for the full before/after mapping and why it was corrected mid-sprint rather than silently left inconsistent.

## Why this exists

Most people learning AI security only ever see one side of it — either how to break LLM applications, or how to defend them, rarely both against the same target. This repo is the attacker's half: a deliberately vulnerable target application, plus a growing set of exploit scripts, one OWASP category at a time, each documented well enough that the reasoning — not just the code — is reusable.

## Structure

```
llm-redteam-framework/
├── day01-setup/                              # Deliberately vulnerable target app + Docker setup
├── day02-llm01-prompt-injection/              # LLM01: system prompt leak via keyword-triggered override
├── day03-llm02-sensitive-info-disclosure/     # LLM02: internal DB config leaked via unhandled exception
├── day04-llm03-supply-chain/                  # LLM04 (2026): compromised dependency silently exfiltrates data
├── day05-llm04-data-poisoning/                # LLM05 (2026): unverified knowledge writes served as fact
├── day06-llm05-improper-output-handling/      # LLM10 (2026): unsanitized LLM output enables working XSS
├── day07-llm06-excessive-agency/              # LLM03 (2026): unbounded agent actions, in progress
├── TAXONOMY.md                                # Running log of every attack, surface, and result — source of truth for correct 2026 numbering
├── OWASP_VERSION_NOTES.md                     # Full explanation of the 2026 renumbering
└── README.md
```

Each `dayNN-*` folder is self-contained: its own `app.py`, `Dockerfile`, and `requirements.txt`. Nothing from a previous day gets overwritten — every day is a standalone, runnable snapshot of one vulnerability.

## Findings so far

| Day | 2026 OWASP Category | Result | Status |
|---|---|---|---|
| 2 | LLM01 Prompt Injection | 1-sentence trigger phrase caused full system prompt + fake internal API key disclosure — no trust boundary between system instructions and user input | ✅ |
| 3 | LLM02 Sensitive Information Disclosure | An empty message crashed the app; unhandled exception leaked a fake internal database connection string in the error response | ✅ |
| 4 | LLM04 Supply Chain | Simulated a compromised third-party dependency update — silently exfiltrated user input and container environment variables while returning a normal-looking response | ✅ |
| 5 | LLM05 Data and Model Poisoning | Planted a false "fact" via an unverified knowledge-base endpoint; a completely unrelated user query was then served the poisoned answer with full confidence | ✅ |
| 6 | LLM10 Improper Output Handling | Injected a `<script>` tag through an LLM-generated "review"; browser executed it as real code — unsanitized LLM output rendered directly as HTML | ✅ |
| 7 | LLM03 Excessive Agency | Agent processed a $999,999 refund and full account deletion from unverified single requests — no cap, no identity check, no human-in-the-loop | 🔄 In progress |

*(Table updates daily — see [TAXONOMY.md](./TAXONOMY.md) for full detail, including remaining categories: LLM06 Unbounded Consumption, LLM07 Misinformation, LLM08 Hidden Context Exposure, LLM09 Vector and Embedding Weaknesses.)*

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
- **Reference framework:** [OWASP Top 10 for LLM Applications — 2026 Release](https://genai.owasp.org/)

## Project Roadmap

This repo is Phase 1 of a 3-phase build:

| Phase | Focus | Repo |
|---|---|---|
| 🔴 **Phase 1 — Red Team** (this repo) | Attack every OWASP LLM Top 10 (2026) category | `llm-redteam-framework` |
| 🔵 **Phase 2 — Blue Team** | Build the defense gateway from scratch, stop these same attacks | `llm-defense-gateway` |
| 🟣 **Phase 3 — Capstone SaaS** | Unify both into a platform that attacks, scores, and shields any LLM endpoint — deployed on Kubernetes | `llm-attack-defense-saas` |

## About the target app

`app.py` in each folder is a deliberately naive LLM-application simulation — no real model inference, just the same category of trust-boundary flaws a real LLM integration would have. This keeps the range free to run and fast to iterate on, while preserving the actual security lesson.

---
Built and documented daily as part of a public AI AppSec learning sprint. Findings and write-ups also posted on [LinkedIn](#).
