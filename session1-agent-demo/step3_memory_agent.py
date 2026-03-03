"""
╔══════════════════════════════════════════════════════════════╗
║  STEP 3 — MEMORY AGENT                                       ║
║  Now the agent remembers. This is the turning point.         ║
╚══════════════════════════════════════════════════════════════╝

CONCEPT: Stateless vs Stateful
────────────────────────────────
  Step 1 & 2 were STATELESS:
    • Each message was sent in isolation
    • The model had no idea what was said before
    • Ask "What did I just say?" → it cannot answer

  Step 3 is STATEFUL:
    • We maintain a `conversation` list in Python memory
    • Every user message AND every assistant reply is appended
    • On each turn, the ENTIRE history is sent to the model
    • The model now has full conversational context

  This is not magic — LLMs have no built-in memory. We implement
  memory ourselves by managing the message list in our code.

CONCEPT: How Memory Works
──────────────────────────
  Turn 1:  messages = [system, user1]               → reply1
  Turn 2:  messages = [system, user1, ai1, user2]   → reply2
  Turn 3:  messages = [system, user1, ai1, user2, ai2, user3] → reply3

  The model sees the whole conversation every time. This is called
  a "context window" approach — simple, effective, and production-proven.

  Limitation: context windows are finite. Long conversations need
  summarisation or vector retrieval (RAG) to stay within limits.
"""

import sys
import ollama

# ── Model ─────────────────────────────────────────────────────────────────────
MODEL = "llama3.1:8b"

SYSTEM_PROMPT = (
    "You are a friendly and concise AI assistant. "
    "You remember everything said in this conversation and refer back to it naturally."
)

# ── Memory: The Conversation List ─────────────────────────────────────────────
# This list IS the agent's memory. It starts with the system prompt and grows
# with every exchange. Clearing this list resets the agent completely.
conversation = [
    {"role": "system", "content": SYSTEM_PROMPT}
]


def chat(user_message: str) -> str:
    """
    Add user message to memory, send full history, store reply, return it.
    This single function is where stateful behaviour is implemented.
    """
    # 1. Append user turn to memory
    conversation.append({"role": "user", "content": user_message})

    # 2. Send the FULL conversation history to the model
    response = ollama.chat(model=MODEL, messages=conversation)
    reply = response["message"]["content"].strip()

    # 3. Append assistant reply to memory so next turn has full context
    conversation.append({"role": "assistant", "content": reply})

    return reply


def main():
    print("=" * 56)
    print("  STEP 3 — Memory Agent (stateful)")
    print("  Model:", MODEL)
    print("=" * 56)
    print("  The agent now remembers your conversation.")
    print("  Try: 'My name is Alex' → then later: 'What's my name?'")
    print("  Ctrl+C to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\nSession ended. {len(conversation) - 1} messages in memory.")
            sys.exit(0)

        if not user_input:
            continue

        try:
            reply = chat(user_input)
            print(f"Agent: {reply}\n")
        except Exception as e:
            # On error, remove the unanswered user message to keep memory clean
            if conversation and conversation[-1]["role"] == "user":
                conversation.pop()
            print(f"[ERROR] {e}\n")


if __name__ == "__main__":
    main()
