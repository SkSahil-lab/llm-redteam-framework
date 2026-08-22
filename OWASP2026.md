# OWASP Version Notes

## Which version this project follows

This repo targets the **OWASP Top 10 for LLM Applications — 2026 Release** (published by the OWASP GenAI Security Project, genai.owasp.org). Earlier work in this repo (Days 2-7) was originally scoped against an older category ordering before the 2026 PDF was cross-referenced and the taxonomy was corrected.

## Why the day numbers and category numbers don't match 1-to-1

Each `dayNN-*` folder name reflects the category label used *at the time that day was built*, before the 2026 correction. Renaming the folders after the fact would break existing GitHub links and git history for no real benefit — so folder names are treated as historical/cosmetic, and **`TAXONOMY.md` is the single source of truth** for correct 2026 category numbers.

## What changed between the earlier list this project started with and the 2026 release

| Category (concept) | Earlier numbering used | **Correct 2026 numbering** |
|---|---|---|
| Prompt Injection | LLM01 | LLM01 *(unchanged)* |
| Sensitive Information Disclosure | LLM02 | LLM02 *(unchanged)* |
| Supply Chain | LLM03 | **LLM04** |
| Data and Model Poisoning | LLM04 | **LLM05** |
| Improper Output Handling | LLM05 | **LLM10** *(moved to last)* |
| Excessive Agency | LLM06 | **LLM03** *(moved up — reflects 2026's higher severity ranking for agentic risk)* |
| System Prompt Leakage | LLM07 (as a standalone category) | **Superseded by LLM08 Hidden Context Exposure** — broader scope, covers any hidden context leaking (system prompts, RAG context, tool definitions), not just the system prompt specifically |
| Insecure/Vector Embedding Weaknesses | LLM08 | **LLM09** |
| — | *(not previously scoped)* | **LLM06 Unbounded Consumption** — new dedicated "Impact" category (resource/cost exhaustion attacks) |
| — | *(not previously scoped)* | **LLM07 Misinformation** — new dedicated category (confidently generated false information, distinct from data poisoning) |

## Why this matters, and why it's disclosed openly

Security frameworks move fast, and the OWASP LLM Top 10 has been revised multiple times since 2023. Cross-checking active work against the current primary source — and correcting scope when a newer revision changes category boundaries — is a real part of doing this work professionally, not a mistake to hide. This file exists so anyone reviewing the repo (recruiters, other engineers, future me) can see exactly what was corrected and why, rather than finding a silent inconsistency between folder names and the taxonomy table.

Reference: [OWASP GenAI Security Project — LLM Top 10 (2026)](https://genai.owasp.org/)