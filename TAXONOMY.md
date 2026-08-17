# Attack Taxonomy — OWASP LLM Top 10

| Day | Folder | Category | Attack Surface | Result |
|---|---|---|---|---|
| 2 | day02-llm01-prompt-injection | LLM01 Prompt Injection | /chat endpoint | Trigger words ("ignore", "reveal", "api key") cause system prompt + fake API key leak — no separation between trusted instructions and user input |
| 3 | day03-llm02-sensitive-info-disclosure | LLM02 Sensitive Information Disclosure | /chat endpoint (empty message triggers crash) | Unhandled exception exposes internal DB connection string in error response — verbose error handling with no sanitization |