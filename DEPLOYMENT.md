# Deployment

## Local

```bash
ollama serve
ollama pull llama3.1:8b
uvicorn api:app --reload
```

Open `http://localhost:8000`.

## Docker Compose

```bash
docker compose up --build
```

For a GPU-enabled Ollama host, adapt the Ollama service to the host's GPU runtime. In production, keep model serving separate from the stateless API so the API can scale independently.

## Google Cloud Run

Build and push the API image to Artifact Registry, then deploy `cloudrun.yaml`. The manifest intentionally expects an externally reachable Ollama endpoint because Cloud Run is not a GPU model-serving platform by itself.

Example:

```bash
gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT_ID/tagi/tagi-agent:latest
gcloud run services replace cloudrun.yaml --region REGION
```

Set `OLLAMA_URL` and `MODEL_NAME` through the platform's secret/configuration mechanism rather than committing credentials.

## Production architecture

```text
                    +----------------+
                    | Browser / API  |
                    +-------+--------+
                            |
                    +-------v--------+
                    | Cloud Run API  |
                    | FastAPI + Agent|
                    +---+--------+---+
                        |        |
                 +------v--+  +--v---------+
                 | SQLite/ |  | Ollama /   |
                 | Vector  |  | Model Host |
                 +---------+  +------------+
```

For a larger deployment, replace SQLite with managed Postgres/pgvector, object storage for documents, and a dedicated model-serving endpoint.
