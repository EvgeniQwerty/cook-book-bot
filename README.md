# cook-book-bot: Telegram Recipe Management Bot

## Overview
Cook-book-bot is a Telegram bot designed to help users manage cooking recipes and get AI-powered cooking assistance. The bot allows users to browse, add, edit, and delete recipes organized by categories, as well as ask cooking-related questions to an AI assistant.

## Features

### Recipe Management
- **Browse Recipes**: View recipes organized by categories (Breakfast, Lunch, Dinner, Desserts, Snacks, Drinks)
- **Add Recipes**: Add new recipes with title, ingredients, instructions, and optional video links
- **Edit Recipes**: Modify existing recipes
- **Delete Recipes**: Remove unwanted recipes

### AI Cooking Assistant
- Ask cooking-related questions
- Get recipe suggestions based on available ingredients
- Receive step-by-step cooking instructions

### Multilingual Support
- English and Russian language interfaces
- Easily extendable to other languages

## Installation

### Prerequisites
- Python 3.7 or higher
- Telegram account and bot token (from BotFather)
- OpenRouter API key (for AI assistant functionality)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cook-bot.git
   cd cook-bot
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install aiogram aiosqlite python-dotenv aiohttp
   ```

4. Create a `.env` file in the project root with the following content:
   ```
   TOKEN=your_telegram_bot_token
   OPENROUTER_API_KEY=your_openrouter_api_key
   LANGUAGE=en  # or 'ru' for Russian
   ```

## Configuration

The bot's configuration is managed through the `config.py` file:

- **TOKEN**: Your Telegram bot token (loaded from .env)
- **OPENROUTER_API_KEY**: API key for OpenRouter (loaded from .env)
- **OPENROUTER_MODEL**: AI model used for cooking assistance
- **DATABASE_NAME**: SQLite database file name
- **LANGUAGE**: Interface language ('en' or 'ru')
- **CATEGORIES**: Recipe categories (automatically adjusted based on language)

## Usage

1. Start the bot:
   ```
   python main.py
   ```

2. Open Telegram and search for your bot by username

3. Start a conversation with the bot by sending the `/start` command

4. Use the main menu to:
   - Browse recipes by category
   - Add new recipes
   - Ask the AI assistant for cooking advice

## Project Structure

```
├── main.py                # Bot entry point
├── config.py              # Configuration settings
├── translations.py        # Multilingual text support
├── database/              # Database operations
│   ├── __init__.py
│   └── db.py              # Database functions
├── handlers/              # Message handlers
│   ├── __init__.py
│   └── user_handlers.py   # User interaction handlers
└── keyboards/             # Telegram keyboard layouts
    ├── __init__.py
    └── keyboards.py       # Keyboard generation functions
```

## Database Schema

The bot uses SQLite to store recipe data with the following schema:

```sql
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    video_link TEXT
)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [aiogram](https://github.com/aiogram/aiogram) - Telegram Bot API framework
- [OpenRouter](https://openrouter.ai/) - AI model provider