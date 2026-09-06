"""Optional semantic RAG using Ollama embeddings and a tiny SQLite vector store."""
import json, sqlite3, urllib.request
from pathlib import Path
import numpy as np
from config import OLLAMA_URL, DATA_DIR
from rag import load_documents, chunk_text

EMBED_URL=OLLAMA_URL.rsplit('/api/chat',1)[0]+'/api/embed'
DB=Path(DATA_DIR)/'vectors.db'; EMBED_MODEL='nomic-embed-text'

def embed(texts):
    req=urllib.request.Request(EMBED_URL,data=json.dumps({'model':EMBED_MODEL,'input':texts}).encode(),headers={'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req,timeout=60) as r:return np.asarray(json.loads(r.read().decode())['embeddings'],dtype=np.float32)

def index_documents():
    DB.parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(DB) as db:
        db.execute('CREATE TABLE IF NOT EXISTS chunks(source TEXT, chunk INTEGER, text TEXT, embedding BLOB)')
        for doc in load_documents(DATA_DIR):
            chunks=chunk_text(doc['text']); vectors=embed(chunks) if chunks else []
            db.execute('DELETE FROM chunks WHERE source=?',(doc['source'],))
            for i,(text,vec) in enumerate(zip(chunks,vectors)): db.execute('INSERT INTO chunks VALUES(?,?,?,?)',(doc['source'],i,text,vec.tobytes()))
        db.commit()

def semantic_retrieve(query,top_k=4):
    q=embed([query])[0]
    with sqlite3.connect(DB) as db: rows=db.execute('SELECT source,chunk,text,embedding FROM chunks').fetchall()
    scored=[]
    for source,chunk,text,blob in rows:
        v=np.frombuffer(blob,dtype=np.float32); score=float(np.dot(q,v)/(np.linalg.norm(q)*np.linalg.norm(v)+1e-8)); scored.append({'source':source,'chunk':chunk,'score':round(score,4),'text':text})
    return sorted(scored,key=lambda x:x['score'],reverse=True)[:top_k]
