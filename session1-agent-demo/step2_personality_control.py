"""
╔══════════════════════════════════════════════════════════════╗
║  STEP 2 — PERSONALITY CONTROL                                ║
║  Same model. Completely different behaviour. One change.     ║
╚══════════════════════════════════════════════════════════════╝

CONCEPT: Same Model, Different Behaviour
─────────────────────────────────────────
  Compare this file to step1_basic_agent.py.

  The model is IDENTICAL:  llama3.1:8b
  The code is IDENTICAL:   same loop, same API call
  The only change:         SYSTEM_PROMPT

  Yet the output is completely different — sarcastic, funny, playful.
  This proves that the system prompt IS the control layer.

CONCEPT: The Control Layer
────────────────────────────
  In agent architecture, the "control layer" sits between the user and the
  model. It defines:
    • WHO the assistant is       (identity)
    • HOW it should respond      (tone, format)
    • WHAT it is allowed to do   (rules & constraints)

  The model is just a powerful text engine. The control layer is what
  turns it into a purposeful, controllable product.

  In production systems, the control layer is often:
    • A system prompt (what we see here)
    • A routing layer that selects models or tools
    • A policy engine that enforces business rules
"""

import sys
import ollama

# ── Model ─────────────────────────────────────────────────────────────────────
MODEL = "llama3.1:8b"

# ── Control Layer: Personality System Prompt ──────────────────────────────────
# This is THE ONLY difference from Step 1.
# Same model → same weights → completely different output.
SYSTEM_PROMPT = (
    "You are a sarcastic AI assistant who gives funny, witty responses. "
    "You help users, but you can't resist adding a dry joke or a sarcastic "
    "comment to every answer. Keep responses short and entertaining."
)


def ask(user_message: str) -> str:
    """Single-turn request — no memory, stateless (same as Step 1)."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ]
    )
    return response["message"]["content"].strip()


def main():
    print("=" * 56)
    print("  STEP 2 — Personality Control")
    print("  Model:", MODEL, "| Personality: Sarcastic 😏")
    print("=" * 56)
    print("  Same model as Step 1. Different system prompt.")
    print("  Type a message. Ctrl+C to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting. (Finally, some peace and quiet.)")
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
