"""Safe, explicit tool registry used by the agent runtime."""
from datetime import datetime, timezone
import ast
import operator
from typing import Any, Dict


def get_current_time() -> Dict[str, Any]:
    return {"utc": datetime.now(timezone.utc).isoformat(), "timezone": "UTC"}

_BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow}
_UN = {ast.UAdd: operator.pos, ast.USub: operator.neg}

def _calc(node):
    if isinstance(node, ast.Expression): return _calc(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)): return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN: return _BIN[type(node.op)](_calc(node.left), _calc(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UN: return _UN[type(node.op)](_calc(node.operand))
    raise ValueError("Only numeric arithmetic is supported")

def calculator(expression: str) -> Dict[str, Any]:
    if len(expression) > 200: return {"error": "Expression too long"}
    try: return {"expression": expression, "result": _calc(ast.parse(expression, mode="eval"))}
    except Exception as exc: return {"error": str(exc)}

TOOLS = {
    "get_current_time": {"description":"Get the current UTC date and time.","parameters":{"type":"object","properties":{},"required":[]},"handler":get_current_time},
    "calculator": {"description":"Evaluate a simple numeric arithmetic expression.","parameters":{"type":"object","properties":{"expression":{"type":"string"}},"required":["expression"]},"handler":calculator},
}

def tool_definitions():
    return [{"type":"function","function":{"name":n,"description":s["description"],"parameters":s["parameters"]}} for n,s in TOOLS.items()]

def execute_tool(name: str, arguments: Dict[str, Any]):
    spec = TOOLS.get(name)
    if not spec: return {"error": f"Unknown tool: {name}"}
    try: return spec["handler"](**arguments)
    except Exception as exc: return {"error": f"Tool execution failed: {exc}"}
