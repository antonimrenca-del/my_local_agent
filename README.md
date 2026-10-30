# Local Weather AI Agent (Llama 3.2 + Data Injection)

An edge-hosted Python AI agent built using **Ollama** and **Llama 3.2**. This project demonstrates a lightweight retrieval-augmented generation (RAG) pipeline that bypasses network scraping blocks and small-model tool-calling limitations by injecting real-time weather payloads directly into the system prompt.

---

## Architecture & Workflow
1. **Pre-Inference Data Fetching:** The agent executes an HTTP GET request to `wttr.in` to retrieve current weather metrics as plain text/JSON before invoking the LLM.
2. **Context Injection:** Live weather context is embedded into the LLM system prompt.
3. **Inference Execution:** Llama 3.2 processes the prompt with live local context and formats the response for the user.

---

## Technical Troubleshooting & Key Learnings

During development and iteration, several key architectural challenges were resolved:

* **Tool-Calling Model Constraints:** Initial tests with `gemma2:2b` produced `BadRequestError` exceptions because smaller parameter models lack native function-calling primitives. Migrated backend hosting to `llama3.2`.
* **Anti-Scraping & Network Timeouts:** Direct web scraping via BeautifulSoup and automated DuckDuckGo searches triggered security blocks and network timeouts. Refactored the architecture to rely on reliable, open endpoint payloads (`wttr.in`).
* **Environment Configuration:** Resolved missing library dependencies (`mcp`, `google-adk[extensions]`) and ensured consistent environment pathing for Ollama local API endpoints (`$env:OLLAMA_API_BASE`).

---

## Prerequisites

* **Python 3.10+**
* **Ollama** installed and running locally ([ollama.com](https://ollama.com))
* **Llama 3.2** model weights pulled locally:

```powershell
ollama pull llama3.2
