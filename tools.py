"""Built-in tools for the TAGI agent.

Tools are deliberately small and deterministic so the project demonstrates
agent/tool orchestration without hiding the mechanics behind a framework.
"""

from datetime import datetime, timezone
from typing import Any, Dict


def get_current_time() -> Dict[str, Any]:
    """Return the current UTC time as structured data."""
    now = datetime.now(timezone.utc)
    return {"utc": now.isoformat(), "timezone": "UTC"}


TOOLS = {
    "get_current_time": {
        "description": "Get the current UTC date and time.",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "handler": get_current_time,
    }
}


def tool_definitions():
    """Return tool definitions in Ollama-compatible function format."""
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": spec["description"],
                "parameters": spec["parameters"],
            },
        }
        for name, spec in TOOLS.items()
    ]


def execute_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a registered tool with a safe allow-list lookup."""
    spec = TOOLS.get(name)
    if not spec:
        return {"error": f"Unknown tool: {name}"}
    try:
        return spec["handler"](**arguments)
    except Exception as exc:
        return {"error": f"Tool execution failed: {exc}"}
