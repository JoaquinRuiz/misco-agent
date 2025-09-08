# 🤖 misco-agent

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/) 
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) 
[![Made with](https://img.shields.io/badge/made%20with-Python%20%26%20AI-orange.svg)](#)

**misco-agent** is a minimal AI agent template built with Python.  
It’s designed so **anyone** can run and extend it — even with little programming knowledge.

✨ Features:
- Chat with an AI model using an OpenAI-compatible API (OpenAI, OpenRouter, Together, or local **Ollama**).  
- Comes with two simple tools:  
  - 🧮 `misco_calculator` → safe arithmetic evaluator.  
  - 📝 `misco_notes` → save and list personal notes.  
- Easy to add your own tools with just a few lines of code.  
- Runs in the terminal with a clean **Rich** interface.  

---

## 📂 Project structure
```bash
misco-agent/
├─ misco_app.py # Agent loop (CLI)
├─ misco_tools.py # Tool definitions (calculator, notes)
├─ prompts/
│ └─ misco_system.md # System prompt (agent instructions)
├─ .env.example # Example environment variables
├─ requirements.txt # Minimal dependencies
└─ README.md # Project documentation
```
---

## ⚙️ Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/misco-agent.git
   cd misco-agent
   ```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy the environment file and set your API key:

```bash
cp .env.example .env
```

Edit .env and fill in:

```ini
MISCO_BASE_URL=https://api.openai.com/v1
MISCO_API_KEY=your_api_key_here
MISCO_MODEL=gpt-4o-mini
```
If you want to use Ollama locally, set:
```ini
MISCO_BASE_URL=http://localhost:11434/v1
MISCO_MODEL=llama3.1 (or another installed model).
MISCO_API_KEY can stay empty for local use.
```

---

## ▶️ Run misco-agent
```bash
python misco_app.py
```You’ll see:

```pgsql
misco-agent ready. Type your message. (Ctrl+C to exit)
> 
```

Examples:

- Calculate 12*(3+7)/2
- Add a note: buy milk
- List my notes

## 🛠 Add your own misco_tool
1. Open misco_tools.py.
2. Create a new function like this:

```python
def _misco_upper(args):
    text = str(args.get("text", "")).strip()
    if not text:
        return "Error: missing 'text'."
    return text.upper()

MiscoTool(
    name="misco_uppercase",
    description="Converts text to UPPERCASE.",
    params={"type":"object","properties":{"text":{"type":"string"}},"required":["text"]},
    func=_misco_upper,
)
```
3. Add it to the MISCO_TOOLS list.

4. Restart misco_app.py. The agent will automatically discover the new tool. 🚀

---

## 📚 Learn More

This project is inspired by the ideas I share in my book:

*Programming with Artificial Intelligence: How to integrate Agents, MCP, and Vibe Coding into your workflow to lead AI-first development*

In this book, I explain how AI is transforming programming forever — from conversational coding to Model-Centric Programming (MCP) and Vibe Coding.
It’s not just about prompts: it’s about learning how to integrate vibe coding, MCP, agents, and workflows into your daily development process so you can stay ahead in the AI-first era.
- [Programming with Artificial Intelligence: How to integrate Agents, MCP, and Vibe Coding into your workflow to lead AI-first development](https://a.co/d/hRpBMvb)
- [Programar con Inteligencia Artificial: Cómo integrar agentes, MCP y Vibe Coding en tu flujo de trabajo para liderar el desarrollo AI-first (Spanish version)](https://amzn.eu/d/7kZkYEb)

👉 If you’re a developer, tech lead, or software architect, this guide will help you understand what to delegate to AI, what to keep under your control, and how to build real-world projects with AI.

---

## ❓ FAQ
*Do I need to be a programmer?*
Not really. Just copy the files, set your MISCO_API_KEY in .env, and run python misco_app.py.

*Can I use it without an API key?*
Yes — if you run Ollama locally with an OpenAI-compatible model.

*Is the calculator safe?*
Yes, it only accepts digits and basic math symbols. No external code is executed.

*Can I build a web UI?*
Absolutely. Add Streamlit or Gradio on top of the misco-agent loop.

---

## 📜 License
MIT License. Free to use and adapt.
Built with ❤️ by [JokiRuiz](https://jokiruiz.com).