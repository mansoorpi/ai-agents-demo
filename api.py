from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from agent import chat
from rag import retrieve, format_context
from memory import load_messages, save_message
from config import DATA_DIR

app=FastAPI(title='TAGI Agent API',version='1.0.0'); Path(DATA_DIR).mkdir(exist_ok=True)
class ChatRequest(BaseModel):
    message:str=Field(min_length=1,max_length=10000); session_id:str='default'; history:list[dict]=Field(default_factory=list)
class ChatResponse(BaseModel):
    response:str; sources:list[dict]=Field(default_factory=list)
@app.get('/health')
def health(): return {'status':'ok','service':'tagi-agent'}
@app.post('/chat',response_model=ChatResponse)
def chat_endpoint(req:ChatRequest):
    prior=load_messages(req.session_id); results=retrieve(req.message,DATA_DIR); context=format_context(results)
    system={'role':'system','content':'Answer using document context when relevant. Cite source filenames. If context is insufficient, say so.\n\nDOCUMENT CONTEXT:\n'+context}
    try: answer=chat([system]+(prior or req.history)+[{'role':'user','content':req.message}])
    except Exception as exc: raise HTTPException(503,detail=str(exc)) from exc
    save_message(req.session_id,'user',req.message); save_message(req.session_id,'assistant',answer); return ChatResponse(response=answer,sources=results)
@app.post('/documents')
async def upload_document(file:UploadFile=File(...)):
    suffix=Path(file.filename or '').suffix.lower()
    if suffix not in {'.pdf','.txt','.md','.csv'}: raise HTTPException(400,'Supported files: PDF, TXT, MD, CSV')
    name=f'{uuid4().hex}{suffix}'; (Path(DATA_DIR)/name).write_bytes(await file.read()); return {'filename':name,'status':'ingested'}
@app.post('/index')
def index_documents():
    from vector_rag import index_documents as build_index
    try: build_index(); return {'status':'indexed'}
    except Exception as exc: raise HTTPException(503,detail=f'Embedding index failed: {exc}') from exc
@app.get('/',include_in_schema=False)
def index(): return FileResponse('static/index.html')
