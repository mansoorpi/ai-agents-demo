# TAGI — Agentic AI / RAG / MLOps Portfolio

TAGI is a framework-light **agentic AI reference application** built around Ollama. It demonstrates tool calling, bounded execution, document ingestion, retrieval, persistent memory, an API/UI layer, evaluation, tracing, containers, CI, and a Cloud Run deployment path.

## Architecture

```text
Browser / Client -> FastAPI -> Agent Runtime -> Ollama
                         |             |
                         |             +--> calculator / time / web search
                         +--> SQLite session memory
                         +--> RAG -> chunks -> lexical retrieval
                                  \-> Ollama embeddings -> SQLite vector store
```

## Capabilities

- Agent loop with model-selected tools and execution bounds
- Explicit allow-listed tools: calculator, UTC time, public web search
- PDF/TXT/MD/CSV ingestion and chunking
- Lexical RAG plus optional semantic RAG with Ollama `nomic-embed-text`
- Persistent SQLite conversation memory by session ID
- FastAPI REST API and lightweight browser UI
- Transparent JSONL evaluation dataset and runner
- OpenTelemetry spans for LLM/tool operations
- pytest + Ruff + GitHub Actions CI
- Docker/Docker Compose
- Cloud Run deployment manifest and production architecture guidance
- Local-first operation with Ollama and no hosted LLM API key

## Quick start

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

```bash
ollama pull nomic-embed-text
```

Upload documents through the UI, then call `POST /index`. Semantic vectors are stored locally in SQLite. Chat uses the lightweight lexical retriever by default so the basic application remains usable without an embedding model.

## API

| Endpoint | Purpose |
|---|---|
| `GET /health` | Health check |
| `POST /chat` | Agent request with `message` + `session_id` |
| `POST /documents` | Upload PDF/TXT/MD/CSV |
| `POST /index` | Build semantic embedding index |
| `GET /docs` | OpenAPI documentation |

## Evaluation and quality

```bash
pytest -q
ruff check .
python evals/run_eval.py   # requires Ollama for LLM evaluation
```

The evaluation harness is intentionally small and reproducible. It demonstrates the evaluation workflow without pretending that keyword coverage is a complete measure of LLM quality.

## Docker

```bash
docker compose up --build
```

The API listens on port `8000`. In production, model serving should normally be separated from the stateless API so API replicas can scale independently.

## Cloud

See `DEPLOYMENT.md` and `cloudrun.yaml`. Cloud Run hosts the stateless API; the manifest expects an externally reachable Ollama/model endpoint. Production deployments should use managed storage, secret management, authentication, rate limiting, network controls, and a dedicated model-serving layer as appropriate.

## Project structure

```text
agent.py             Agent orchestration + tool loop
tools.py             Allow-listed tools
rag.py               Parsing, chunking, lexical retrieval
vector_rag.py        Ollama embeddings + SQLite vector store
memory.py            Persistent session memory
api.py               FastAPI application
static/index.html    Browser UI
evals/               Evaluation dataset + runner
tests/               Automated tests
telemetry.py         OpenTelemetry instrumentation
Dockerfile           API container
docker-compose.yml   Local API + Ollama stack
cloudrun.yaml        Cloud Run manifest
DEPLOYMENT.md        Deployment guide
SECURITY.md          Production security checklist
.github/workflows/   CI pipeline
```

## Portfolio talking points

This repository is deliberately framework-light so the agent protocol remains visible in an interview: **tool schema → model decision → bounded execution → tool result → grounded response**. It also demonstrates the engineering concerns around an LLM application: retrieval trade-offs, state, evaluation, observability, containerization, CI, and cloud deployment.

## Security

See `SECURITY.md`. The built-in registry does not dynamically execute arbitrary functions. The web-search tool is intentionally limited to search queries; a production implementation should add stronger egress/SSRF controls.

## License

MIT
