from pathlib import Path
from rag import chunk_text, retrieve

def test_chunking():
    chunks = chunk_text("one two three four five six", chunk_size=3, overlap=1)
    assert len(chunks) == 3
    assert chunks[0] == "one two three"

def test_retrieval(tmp_path: Path):
    (tmp_path / "notes.txt").write_text("Python agents use tools to perform actions.", encoding="utf-8")
    results = retrieve("tools actions", str(tmp_path))
    assert results
    assert results[0]["source"].endswith("notes.txt")
