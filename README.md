# 🍕 Pizza – A Modular Self-Hosted Assistant

**Pizza** is a personal Python-based assistant designed to be self-hosted, modular, and extensible. It's a learning-focused project aimed at building a privacy-respecting system capable of integrating with local devices, APIs, and potentially smart home environments.

Currently in early development, Pizza supports a basic command router, a plugin system, and is built with future goals including voice input, LLM integration, and cloud deployment.

---

## 🔧 Features

- 🧠 **Command Routing** – Commands are handled dynamically using a central command router
- 🔌 **Plugin Architecture** – Plugins can register commands and extend functionality
- 💡 **Environment Configuration** – Uses `.env` files for secrets and settings
- 💬 **CLI-Based Interaction** – Lightweight, terminal-driven interface

---

## 🧩 Current Plugin Examples

Plugins live in the `plugins/` directory and each defines a `register(router)` function.

Example: `hello_plugin.py`
```python
def register(router):
    def hello():
        print("👋 Hello from the Hello Plugin!")

    router.register("hello_plugin", hello)
```

---

## 📂 Project Structure

```
pizza/
├── core/                  # Core logic (command router, future internals)
│   └── command_router.py
├── plugins/               # Drop-in plugin modules
│   └── hello_plugin.py
├── main.py                # Entry point for the assistant
├── requirements.txt       # Dependencies
├── .env                   # Environment variables (not committed)
```

---

## 🚀 Getting Started

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the assistant:
   ```bash
   python main.py
   ```

---

## 🛣️ Roadmap

Planned features include:

- 🗣️ Voice command recognition (STT)
- 🔊 Text-to-speech feedback
- 🤖 Natural language command parsing via LLMs
- 📺 Smart device discovery and control
- ☁️ Optional cloud deployment with Docker
- 📦 Plugin marketplace or loader system

---

## ⚖️ License

MIT License — free to use, modify, and share.

---

## 📎 Notes

This project is under active development and serves both as a personal assistant and a platform for learning Python, Docker, APIs, and modular software design.
