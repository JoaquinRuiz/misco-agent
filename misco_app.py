# misco_app.py
import os
import json
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

from misco_tools import misco_tools_schema, misco_call_tool, MISCO_TOOLS

console = Console()
load_dotenv()

BASE_URL = os.getenv("MISCO_BASE_URL", "http://localhost:11434/v1").rstrip("/")
API_KEY  = os.getenv("MISCO_API_KEY", "")
MODEL    = os.getenv("MISCO_MODEL", "qwen3:4b")

HEADERS = {"Content-Type": "application/json"}
if API_KEY:
    HEADERS["Authorization"] = f"Bearer {API_KEY}"

SYSTEM_PATH = os.path.join("prompts", "misco_system.md")
with open(SYSTEM_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

TOOLS = misco_tools_schema()

def chat_completion(payload: dict) -> dict:
    url = f"{BASE_URL}/chat/completions"
    resp = requests.post(url, headers=HEADERS, data=json.dumps(payload), timeout=60)
    if resp.status_code >= 400:
        raise RuntimeError(f"API error {resp.status_code}: {resp.text[:1000]}")
    return resp.json()

def misco_turn(user_input: str):
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.4,
        "tools": TOOLS,          # advertise available tools
        "tool_choice": "auto",   # let the model decide
    }

    data = chat_completion(payload)
    choice = data.get("choices", [{}])[0]
    msg = choice.get("message", {})

    # If the model wants to call tools
    if msg.get("tool_calls"):
        tool_outputs = []
        for tc in msg["tool_calls"]:
            fn = tc["function"]
            name = fn["name"]
            args_json = fn.get("arguments", "{}")
            try:
                args = json.loads(args_json)
            except Exception:
                args = {}

            console.print(f"[bold cyan]→ Running misco_tool:[/bold cyan] {name} {args}")
            result = misco_call_tool(name, args)

            # Return tool result back to the model
            tool_outputs.append({
                "role": "tool",
                "tool_call_id": tc.get("id", "tool_1"),
                "name": name,
                "content": result,
            })

        # Append the assistant message that requested tools, then the tool results
        messages.append({"role": "assistant", "content": msg.get("content", ""), "tool_calls": msg.get("tool_calls")})
        messages.extend(tool_outputs)

        # Second call so the model can craft the final answer with tool results
        payload2 = {
            "model": MODEL,
            "messages": messages,
            "temperature": 0.4,
        }
        data2 = chat_completion(payload2)
        final_msg = data2.get("choices", [{}])[0].get("message", {})
        content = final_msg.get("content", "(no response)")
        messages.append({"role": "assistant", "content": content})
        console.print(Markdown(content))
    else:
        # No tool calls: just print the answer
        content = msg.get("content", "(no response)")
        messages.append({"role": "assistant", "content": content})
        console.print(Markdown(content))

if __name__ == "__main__":
    console.print("[bold green]misco-agent ready.[/bold green] Type your message. (Ctrl+C to exit)\n")
    try:
        while True:
            user = console.input("[bold]> [/bold]")
            if user.strip().lower() in {"salir", "exit", "quit"}:
                break
            misco_turn(user)
    except KeyboardInterrupt:
        console.print("\nBye 👋")
