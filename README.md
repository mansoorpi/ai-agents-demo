# TAGI — Agentic AI / RAG / MLOps Portfolio

TAGI is a framework-light **agentic AI reference application** built around Ollama. It demonstrates tool calling, bounded agent execution, document ingestion, semantic retrieval, persistent memory, an API/UI layer, evaluation, tracing, containers, CI, and a Cloud Run deployment path.

## Architecture

```text
Browser / Client
      |
      v
   FastAPI
      |
      +--> Persistent session memory (SQLite)
      |
      +--> RAG pipeline --> documents --> chunks --> Ollama embeddings --> vector store
      |
      +--> Agent runtime --> Ollama chat model
                   |
                   +--> calculator
                   +--> current time
                   +--> web search
```

## Features

- **Agent loop:** model-selected tools with bounded execution rounds.
- **Tool safety:** explicit allow-list; no arbitrary code execution.
- **RAG:** PDF/TXT/MD/CSV ingestion, chunking, lexical retrieval, plus optional Ollama embedding + cosine-similarity retrieval.
- **Memory:** SQLite-backed conversation history keyed by session ID.
- **Web UI:** lightweight browser interface for chat and document upload.
- **API:** FastAPI endpoints for health, chat, upload, and semantic indexing.
- **Evaluation:** JSONL test set and an executable keyword-coverage evaluation harness.
- **Observability:** OpenTelemetry spans around LLM and tool calls; console exporter for local inspection.
- **MLOps:** pytest, Ruff, GitHub Actions CI, Docker, Compose, and Cloud Run manifest.
- **Local-first:** the core system can run with Ollama and no hosted LLM API key.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama serve
ollama pull llama3.1:8b
uvicorn api:app --reload
```

Open `http://localhost:8000`.

### Semantic RAG

For semantic retrieval, also install an embedding model:

```bash
ollama pull nomic-embed-text
```

Upload documents in the UI, then call `POST /index` once to build the local vector index. The default `/chat` path remains lightweight lexical retrieval so the application still works without an embedding model.

## API

- `GET /health` — liveness check
- `POST /chat` — agent request with `message` and `session_id`
- `POST /documents` — upload PDF/TXT/MD/CSV
- `POST /index` — build the semantic index
- `GET /docs` — FastAPI/OpenAPI documentation

## Evaluation

Run the offline retrieval tests:

```bash
pytest -q
```

Run the LLM evaluation harness with Ollama running:

```bash
python evals/run_eval.py
```

The included evaluation is intentionally simple and transparent. It is a starter harness, not a claim of production-grade model quality measurement.

## Docker

```bash
docker compose up --build
```

The API is exposed on port `8000`. For production, model serving should normally be separated from the stateless API so API replicas can scale independently.

## Cloud deployment

See [`DEPLOYMENT.md`](DEPLOYMENT.md) and `cloudrun.yaml`. The Cloud Run manifest expects an externally reachable Ollama/model endpoint; Cloud Run is used for the stateless API rather than GPU model hosting.

## Project structure

```text
agent.py             Agent orchestration + tool loop
tools.py             Allow-listed tools
rag.py               Document parsing, chunking, lexical retrieval
vector_rag.py        Ollama embeddings + SQLite vector store
memory.py            Persistent conversation memory
api.py               FastAPI application
static/index.html    Browser UI
evals/               Evaluation dataset + runner
tests/               Automated tests
telemetry.py         OpenTelemetry instrumentation
Dockerfile            API container
docker-compose.yml    Local API + Ollama stack
cloudrun.yaml         Cloud Run deployment manifest
DEPLOYMENT.md         Deployment architecture and commands
.github/workflows/    CI pipeline
```

## Engineering notes

The project intentionally keeps the core agent orchestration visible instead of hiding it behind LangChain/LangGraph. This makes the repository useful for discussing tool schemas, execution bounds, failure handling, retrieval trade-offs, state, observability, testing, and deployment during an engineering interview.

Security-sensitive production deployments should add authentication, authorization, rate limiting, request-size limits, secret management, network egress controls, and a managed database/vector service as appropriate.

## License

MIT
