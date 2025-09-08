# misco_tools.py
from dataclasses import dataclass
from typing import Any, Callable, Dict, List
import json
import os

@dataclass
class MiscoTool:
    name: str
    description: str
    params: Dict[str, Any]
    func: Callable[[Dict[str, Any]], str]

# ---------- Tool 1: safe calculator ----------
def _misco_calc(args: Dict[str, Any]) -> str:
    """
    Evaluates simple arithmetic expressions safely.
    args: {"expression": "2 + 2 * 3"}
    """
    expr = str(args.get("expression", "")).strip()
    if not expr:
        return "Error: missing 'expression'."
    allowed = set("0123456789+-*/()., ")
    if any(ch not in allowed for ch in expr):
        return "Error: found forbidden characters in expression."
    try:
        # NOTE: eval is restricted to digits/operators only (no builtins, no names)
        result = eval(expr, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Calc error: {e}"

# ---------- Tool 2: persistent notes ----------
MISCO_NOTES_FILE = "misco_notes.json"

def _misco_notes(args: Dict[str, Any]) -> str:
    """
    Stores and lists simple notes.
    args:
      action: "add" | "list"
      text?: string (when action=add)
    """
    action = args.get("action", "list")
    os.makedirs(os.path.dirname(MISCO_NOTES_FILE) or ".", exist_ok=True)

    if not os.path.exists(MISCO_NOTES_FILE):
        with open(MISCO_NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(MISCO_NOTES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if action == "add":
        text = str(args.get("text", "")).strip()
        if not text:
            return "Error: missing 'text' to add a note."
        data.append(text)
        with open(MISCO_NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return "Note saved."
    else:
        if not data:
            return "(no notes yet)"
        return "\n".join(f"- {n}" for n in data)

# ---------- Catalog of tools ----------
MISCO_TOOLS: List[MiscoTool] = [
    MiscoTool(
        name="misco_calculator",
        description="Solves simple arithmetic expressions (+, -, *, /, parentheses).",
        params={
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
        func=_misco_calc,
    ),
    MiscoTool(
        name="misco_notes",
        description="Stores or lists notes. Use action='add' with text, or action='list'.",
        params={
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["add", "list"]},
                "text": {"type": "string"},
            },
            "required": ["action"],
        },
        func=_misco_notes,
    ),
]

def misco_tools_schema() -> List[Dict[str, Any]]:
    """
    Returns tools in OpenAI 'tools' schema for /v1/chat/completions.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.params,
            },
        }
        for t in MISCO_TOOLS
    ]

def misco_call_tool(tool_name: str, tool_args: Dict[str, Any]) -> str:
    for t in MISCO_TOOLS:
        if t.name == tool_name:
            return t.func(tool_args or {})
    return f"Error: unknown tool '{tool_name}'."
