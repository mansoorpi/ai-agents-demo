from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from agent import chat
from rag import retrieve, format_context
from config import DATA_DIR

app = FastAPI(title="TAGI Agent API", version="1.0.0")
Path(DATA_DIR).mkdir(exist_ok=True)

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

class ChatResponse(BaseModel):
    response: str
    sources: list[dict] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    results = retrieve(request.message, DATA_DIR)
    context = format_context(results)
    system = {"role":"system","content":"Answer using the supplied document context when relevant. Cite sources by filename. If context is insufficient, say so.\n\nDOCUMENT CONTEXT:\n" + context}
    messages = [system] + request.history + [{"role":"user","content":request.message}]
    try:
        answer = chat(messages)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return ChatResponse(response=answer, sources=results)

@app.post("/documents")
async def upload_document(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf", ".txt", ".md", ".csv"}:
        raise HTTPException(status_code=400, detail="Supported files: PDF, TXT, MD, CSV")
    safe_name = f"{uuid4().hex}{suffix}"
    destination = Path(DATA_DIR) / safe_name
    destination.write_bytes(await file.read())
    return {"filename": safe_name, "status": "ingested"}

@app.get("/", include_in_schema=False)
def index():
    return FileResponse("static/index.html")
