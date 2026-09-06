import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1:8b")
MAX_TOOL_ROUNDS = int(os.getenv("MAX_TOOL_ROUNDS", "5"))
DATA_DIR = os.getenv("DATA_DIR", "data")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
