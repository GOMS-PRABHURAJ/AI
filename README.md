# Jarvis — Desktop AI Assistant with LLM Integration

An intelligent desktop assistant that combines system control with OpenAI-powered conversation.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure your API key
cp .env.example .env
# Edit .env and add your OpenAI API key

# 3. Run
python main.py --text-only        # Text mode
python main.py                    # Voice mode
python main.py --mute             # Voice in, text out
```

## Features

- **LLM-powered Q&A** — Ask anything, get intelligent answers via OpenAI
- **Conversation memory** — Maintains context across messages (auto-trimmed to last 20)
- **System commands** — Open/close apps, search web, find/create/delete files
- **Voice I/O** — Speech recognition + text-to-speech
- **Context awareness** — Detects active window

## System Commands (pattern-matched, no API key needed)

| Say | Action |
|-----|--------|
| "open chrome" | Opens Chrome |
| "search for python tutorials" | Google search |
| "find file report.pdf" | Searches home directory |
| "what time is it" | Current time |
| "clear history" | Reset conversation |

Everything else goes to the LLM for an intelligent response.

## Configuration

Edit `.env` or `config/settings.py`:
- `OPENAI_API_KEY` — Required for LLM features
- `LLM_MODEL` — Default: `gpt-4o-mini`
- `LLM_MAX_TOKENS` — Default: `1024`
- `SAFE_MODE` — Prevents destructive file operations

## Architecture

```
main.py              → Entry point & main loop
modules/
  llm_engine.py      → OpenAI chat with memory
  listener.py        → Voice recognition
  speaker.py         → Text-to-speech
  parser.py          → Command pattern matching
  executor.py        → System action execution
  context.py         → Active window detection
config/
  settings.py        → Configuration & env vars
```
