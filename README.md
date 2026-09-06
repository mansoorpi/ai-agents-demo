# TAGI — Agentic AI Demo

A small, inspectable **agentic AI reference project** built around a local Ollama model. The project demonstrates the mechanics behind an AI agent without hiding the orchestration inside a large framework.

## Why this is an agent

Unlike a one-shot chatbot, TAGI has a control layer, conversation memory, an execution loop, and an allow-listed tool registry. The model can decide that it needs a tool, the runtime executes that tool, and the result is returned to the model before the final answer is produced.

```text
User
  |
  v
Agent Runtime
  |
  +--> LLM (Ollama)
  |      |
  |      +--> final answer
  |      |
  |      +--> tool call
  |             |
  |             v
  |         Tool Registry
  |             |
  |             v
  |         Tool Result
  |             |
  +-------------+
        |
        v
   grounded answer
```

## Current capabilities

- Local LLM inference through Ollama
- Conversation memory
- Native model tool calling
- Explicit tool registry and safe allow-list execution
- Structured tool results
- Bounded tool-execution loop to prevent runaway calls
- Simple safety/control prompt
- Zero heavy agent framework dependencies

## Repository

```text
ai-agents-demo/
├── agent.py          # Agent runtime and tool-calling loop
├── tools.py          # Tool registry and tool implementations
├── requirements.txt  # Runtime dependencies
└── README.md
```

## Quick start

### Prerequisites

- Python 3.8+
- Ollama installed and running
- A tool-capable Ollama model

Start Ollama and pull a suitable model:

```bash
ollama serve
ollama pull llama3.1:8b
```

Then run:

```bash
python3 agent.py
```

Try a request such as:

```text
What time is it right now?
```

The model may request the `get_current_time` tool. The runtime executes it and feeds the structured result back into the agent loop.

## Design decisions

### Native tool calling

The project uses Ollama's tool-calling interface directly. This makes the protocol visible: model response → tool selection → execution → tool result → model response.

### Tool allow-list

Only functions explicitly registered in `TOOLS` can execute. Unknown tool names return an error instead of being dynamically imported or executed.

### Bounded execution

`MAX_TOOL_ROUNDS` limits how many tool iterations can occur for one user request. This provides a simple guard against accidental infinite agent loops.

### Framework-light architecture

There is deliberately no LangChain or similar orchestration framework in the core runtime. The goal is to make the fundamentals understandable before introducing abstractions.

## Roadmap

This repository is intentionally evolving toward a production-oriented AI/MLOps portfolio project.

- [x] Agent control layer and memory
- [x] Native tool calling
- [x] Safe tool registry
- [ ] Web search tool
- [ ] Document ingestion pipeline
- [ ] RAG and vector retrieval
- [ ] Persistent conversation state
- [ ] FastAPI service
- [ ] Web UI
- [ ] Evaluation dataset and automated evals
- [ ] OpenTelemetry/LLM tracing
- [ ] Docker and Docker Compose
- [ ] CI checks
- [ ] Cloud deployment example

## License

MIT
