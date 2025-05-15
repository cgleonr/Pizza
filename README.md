# 🍕 Pizza — Your Self-Hosted Personal Assistant

Pizza is a modular, self-hosted voice/text assistant written in Python. It helps you interact with music services like Spotify, control future smart devices, and automate simple tasks. It's built for local development, personal use, and learning advanced Python development workflows.

---

## 🎯 Project Goals

- Improve Python development, Docker, and API integration skills
- Use NLP to match natural language commands to real actions
- Design a plugin system to easily add new features (like YouTube, smart TV control, etc.)
- Deploy on a Raspberry Pi 5 for always-on local assistance

---

## ✅ Features

- **Command Router**: Flexible system to map text to Python functions
- **Natural Language Parsing**: Uses `spaCy` to recognize intent and extract info
- **Spotify Plugin**: Play, pause, search, and resume Spotify tracks
- **Dynamic Plugin Loader**: Auto-load new features from the plugins directory
- **Help Command**: Lists all available commands and their descriptions
- **Test Coverage**: Uses `pytest` and `unittest.mock` for core features and plugins
- **Environment Configuration**: Reads secrets from `.env`

---

## 🧠 Example Commands

```
> play Smooth Operator
🎵 Extracted query: 'smooth operator'
▶️ Playing 'Smooth Operator' by Sade...

> now playing
🎶 Now playing: 'Smooth Operator' by Sade
📱 On device: CARLOS_SURFACE4 (Computer)

> pause
⏸️ Pausing playback...

> help
🧠 Available Commands:
...
```

---

## 🧩 Plugins

### Spotify Plugin
- `spotify_play`: Resume music
- `spotify_pause`: Pause playback
- `spotify_play_song`: Play any track by name
- `spotify_now_playing`: Show current song and device

Other plugin targets: YouTube, smart lights, email control

---

## 🔐 Environment Setup

1. Create a `.env` file in the root project directory:
```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

2. Install dependencies:
```
python -m venv .venv
source .venv/Scripts/activate  # or . .venv/bin/activate on Unix
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Run the assistant:
```
python src/main.py
```

---

## 🧪 Running Tests

Use `pytest` to run all tests:
```
python -m pytest
```

Test files are located under `/tests` and cover all major components.

---

## 📁 Project Structure

```
Pizza/
├── src/
│   ├── main.py
│   ├── core/               # Command routing, NLP logic
│   ├── config/             # Environment variable loader
│   └── plugins/            # Feature modules like spotify
├── tests/                  # Unit tests for core and plugins
├── .env                    # Local credentials (ignored by Git)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Coming Soon

- 🔊 Voice command integration (speech-to-text)
- 📺 YouTube and local video player plugin
- 🧠 LLM-based fallback for unmatched queries
- 🐳 Dockerfile and deployment script
- 🌐 Raspberry Pi startup service

---

## 📄 License

MIT — free to use, modify, and learn from.