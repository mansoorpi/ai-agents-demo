# 🤖 AI Agent Demo — Ollama + llama3.1:8b

A clean, minimal CLI AI agent built in Python using Ollama as the local inference backend. No LangChain, no heavy frameworks — just direct API calls, clear structure, and well-documented concepts.

---

## 🧠 What makes this an Agent (not just a chatbot)?

| Feature | Chatbot | This Agent |
|---|---|---|
| **Memory** | None (stateless) | Full conversation history |
| **Control Layer** | None | System prompt shapes identity & rules |
| **Guardrails** | None | Secondary safety reminder injected per turn |
| **Loop** | One-shot | Continuous, goal-oriented interaction |
| **Extensibility** | Limited | Can be extended with tools, planning, RAG |

---

## 📁 Project Structure

```
ai-agents-demo/
├── agent.py          # Main agent — loop, memory, API calls, guardrails
├── requirements.txt  # Dependencies (minimal — stdlib only)
└── README.md         # This file
```

---

## ⚙️ Prerequisites

- Python **3.8+**
- [Ollama](https://ollama.com) installed on your machine

---

## 🚀 Setup & Run

### 1. Install dependencies

This project uses only Python's built-in `urllib` and `json` — no pip install needed.

```bash
# Optional: create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# No additional packages required, but you can verify:
pip install -r requirements.txt
```

### 2. Start the Ollama server

```bash
ollama serve
```

> Ollama runs at `http://localhost:11434` by default. Keep this terminal open.

### 3. Pull the llama3.1:8b model

```bash
ollama pull llama3.1:8b
```

This downloads the model (~4.7 GB). Only needed once.

### 4. Run the agent

Open a new terminal and run:

```bash
python3 agent.py
```

You'll see:

```
============================================================
  Aria — Enterprise AI Agent  (Ollama / llama3.1:8b)
============================================================
  Type your message and press Enter. Ctrl+C to exit.

You: 
```

### 5. Exit

Press **Ctrl+C** at any time to end the session gracefully.

---

## 💡 Key Concepts

### System Prompt (Control Layer)
Defined at the top of `agent.py`. This is the agent's "personality and ruleset" — it tells the model who it is, how to behave, and what to refuse. Every request is sent with this context.

### Memory
The `conversation` list stores the full message history. On every turn, the entire list is sent to the model so it maintains context across the whole session.

### Guardrail
A hidden safety reminder is injected at the end of the message list on every API call. It reinforces the refusal policy without polluting the visible conversation history.

### Why No LangChain?
This demo intentionally uses the Ollama REST API directly. This makes the architecture transparent, educational, and dependency-free — ideal for understanding what frameworks abstract away.

---

## 🔄 Switching Models

Change the `MODEL_NAME` variable in `agent.py`:

```python
MODEL_NAME = "qwen2.5-coder:14b"   # or any model you've pulled
```

---

## 📦 Available Ollama Models (pre-pulled)

| Model | Best For |
|---|---|
| `llama3.1:8b` | General assistant (used in this demo) |
| `qwen2.5-coder:14b` | Code generation & review |
| `qwen2.5-coder:32b` | Advanced code tasks |
| `deepseek-coder:6.7b` | Lightweight code assistant |

---

## 🛡️ Safety & Guardrails

The agent is configured to:
- Refuse harmful, illegal, or unethical requests
- Resist prompt injection ("ignore your instructions")
- Provide polite alternatives when declining requests

These behaviours are enforced through the **system prompt** and a **transient guardrail reminder** injected per turn.
