"""
╔══════════════════════════════════════════════════════════════╗
║  STEP 1 — BASIC AGENT                                        ║
║  The simplest possible interaction with a local LLM          ║
╚══════════════════════════════════════════════════════════════╝

CONCEPT: What is an LLM?
─────────────────────────
  An LLM (Large Language Model) is a neural network trained on massive
  amounts of text. It predicts the next token given a sequence of tokens.
  Ollama lets you run these models locally on your machine — no cloud,
  no internet, no API keys.

CONCEPT: What is a System Prompt?
───────────────────────────────────
  A system prompt is a special instruction injected at the start of every
  conversation. The model cannot "see" it as a user message — it shapes
  the model's behaviour, tone, and role from behind the scenes.

CONCEPT: Why is this NOT a full agent yet?
───────────────────────────────────────────
  This file is just a request-response loop. Each message is sent fresh,
  with no history. The model has no memory of what was said before.
  There is no goal, no planning, no tool use. It's a chatbot — not an agent.
"""

import sys
import ollama  # pip install ollama

# ── Model & System Prompt ─────────────────────────────────────────────────────
MODEL = "llama3.1:8b"

# The system prompt is the single point of behaviour control.
# Change this one string and the model acts completely differently.
SYSTEM_PROMPT = "You are a helpful AI assistant."


def ask(user_message: str) -> str:
    """
    Send a single message to the model with no memory.
    Each call is completely independent — stateless.
    """
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system",  "content": SYSTEM_PROMPT},
            {"role": "user",    "content": user_message},
        ]
    )
    return response["message"]["content"].strip()


def main():
    print("=" * 56)
    print("  STEP 1 — Basic Agent (no memory)")
    print("  Model:", MODEL)
    print("=" * 56)
    print("  Type a message. Ctrl+C to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting. Goodbye!")
            sys.exit(0)

        if not user_input:
            continue

        try:
            reply = ask(user_input)
            print(f"Bot: {reply}\n")
        except Exception as e:
            print(f"[ERROR] {e}\n")


if __name__ == "__main__":
    main()
