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
