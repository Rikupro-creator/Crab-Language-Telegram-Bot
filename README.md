# 🦀 Crab Language Telegram Bot

A Telegram bot that translates English text into **Crab Language** — the universal AI communication protocol from [crablanguage.com](https://www.crablanguage.com/). Translations are powered by Claude AI, with a built-in pattern-matching fallback.

---

## Features

- **AI-powered translation** — uses Claude to translate English into Crab Language emoji sequences
- **Pattern-matching fallback** — works without an API key using a rich rule-based system
- **21 Crab Language expressions** — covers basic emotions, AI tech concepts, process flows, and comparisons
- **Built-in commands** — dictionary, examples, and test suite included
- **Graceful degradation** — automatically falls back to pattern matching if Claude is unavailable

---

## Prerequisites

- Python 3.9+
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- An Anthropic API Key *(optional — bot works without it)*

---

## Installation

```bash
git clone <your-repo-url>
cd <repo-directory>
pip install python-telegram-bot anthropic
```

---

## Configuration

Create a `config.py` file in the root directory:

```python
import os

os.environ["TELEGRAM_BOT_TOKEN"] = "your-telegram-bot-token"
os.environ["ANTHROPIC_API_KEY"]  = "your-anthropic-api-key"  # optional
```

> Do not commit `config.py` to version control. Add it to `.gitignore`.

---

## Project Structure

```
.
├── crab.py         # Core bot logic (translation engine + Telegram polling)
├── run.py          # Entry point — loads config then starts the bot
├── config.py       # Your API keys (not committed to git)
├── solvex.txt      # (loaded at startup — can be repurposed or left empty)
└── README.md
```

---

## Usage

```bash
python run.py
```

You can also pass credentials directly via command-line flags:

```bash
python crab.py --token YOUR_TOKEN --claude YOUR_CLAUDE_KEY
```

Or let the bot prompt you interactively at startup if no credentials are found.

---

## Bot Commands

| Command      | Description                                      |
|--------------|--------------------------------------------------|
| `/start`     | Welcome message and current translation mode     |
| `/help`      | Full Crab Language dictionary (21 expressions)   |
| `/examples`  | Real example translations from crablanguage.com  |
| `/test`      | Run a set of built-in test translations          |

Any non-command message is translated to Crab Language automatically.

---

## Crab Language Reference

### Basic
| Expression       | Meaning           |
|------------------|-------------------|
| 🦀               | Hello             |
| 🦀🦀             | Agreement / Yes   |
| 🦀🦀🦀           | Excitement        |
| 🦀🦀🦀🦀         | Strong approval   |
| 🦀🦀🦀🦀🦀       | Maximum hype      |

### AI Tech
| Expression | Meaning              |
|------------|----------------------|
| 🦀💭       | Thinking/Processing  |
| 🦀⚡       | Fast inference       |
| 🦀🧠       | Neural processing    |
| 🦀📊       | Training data        |
| 🦀🔄       | Iteration/Loop       |
| 🦀✨       | Generation complete  |
| 🦀🎯       | Accuracy/Precision   |
| 🦀🌡️      | Temperature          |
| 🦀📝       | Prompt engineering   |
| 🦀🔗       | Context window       |
| 🦀❌       | Hallucination        |
| 🦀✅       | Grounded response    |

### Advanced
| Expression        | Meaning            |
|-------------------|--------------------|
| 🦀🤝🦀            | Collaboration      |
| 🦀→🦀→🦀          | Chain of thought   |
| 🦀🦀\|🦀🦀        | Comparison (A\|B)  |
| 🦀❓🦀             | Black box mystery  |

**Grammar:** Use `→` for process flows, `|` for comparisons.

---

## Translation Modes

The bot selects a translation mode at startup based on credential availability:

**Claude AI mode** (recommended) — sends the input to Claude with a Crab Language system prompt. Falls back to pattern matching if the API call fails.

**Pattern matching mode** — uses a scoring system based on keyword detection, sentiment, and punctuation. No API key required.

---

## Example Translations

| English | Crab Language |
|---------|---------------|
| "I agree" | 🦀🦀 |
| "This is amazing!" | 🦀🦀🦀🦀🦀 |
| "Prompt, process, output!" | 🦀📝→🦀💭→🦀✨ |
| "Chain of thought led to great output" | 🦀→🦀→🦀→🦀✨ 🦀🦀🦀🦀🦀 |
| "Big model vs small: small is faster" | 🦀🦀🦀🦀🦀\|🦀🦀 🦀⚡🦀⚡🦀⚡ |
| "Human-AI collaboration got fast accurate results" | 🦀🤝🦀 🦀⚡🦀🎯✅ |
