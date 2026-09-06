"""Minimal local document ingestion and lexical retrieval pipeline."""
from pathlib import Path
import re
from typing import List, Dict
from pypdf import PdfReader


def load_documents(directory: str = "data") -> List[Dict]:
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    docs = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.suffix.lower() == ".pdf":
                text = "\n".join((p.extract_text() or "") for p in PdfReader(str(path)).pages)
            elif path.suffix.lower() in {".txt", ".md", ".csv"}:
                text = path.read_text(encoding="utf-8", errors="ignore")
            else:
                continue
            docs.append({"source": str(path), "text": text})
        except Exception:
            continue
    return docs


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> List[str]:
    words = text.split()
    chunks = []
    step = max(1, chunk_size - overlap)
    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + chunk_size])
        if chunk:
            chunks.append(chunk)
        if start + chunk_size >= len(words):
            break
    return chunks


def _tokens(text: str):
    return set(re.findall(r"[a-z0-9]{2,}", text.lower()))


def retrieve(query: str, directory: str = "data", top_k: int = 4) -> List[Dict]:
    query_tokens = _tokens(query)
    scored = []
    for doc in load_documents(directory):
        for i, chunk in enumerate(chunk_text(doc["text"])):
            tokens = _tokens(chunk)
            score = len(query_tokens & tokens) / max(1, len(query_tokens))
            if score > 0:
                scored.append({"source": doc["source"], "chunk": i, "score": round(score, 4), "text": chunk})
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:top_k]


def format_context(results: List[Dict]) -> str:
    if not results:
        return "No matching documents were found."
    return "\n\n".join(f"[Source: {r['source']} | chunk {r['chunk']}]\n{r['text']}" for r in results)
