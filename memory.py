import json
import sqlite3
from pathlib import Path

DB_PATH = Path("data/tagi.db")


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS messages (session_id TEXT, role TEXT, content TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
    return conn


def save_message(session_id: str, role: str, content: str):
    with _connect() as conn:
        conn.execute("INSERT INTO messages(session_id, role, content) VALUES(?,?,?)", (session_id, role, content))


def load_messages(session_id: str, limit: int = 20):
    with _connect() as conn:
        rows = conn.execute("SELECT role, content FROM messages WHERE session_id=? ORDER BY created_at DESC LIMIT ?", (session_id, limit)).fetchall()
    return [{"role": role, "content": content} for role, content in reversed(rows)]
