import os
from dotenv import load_dotenv
from typing import Dict, List, Any

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Token
TOKEN = os.getenv("TOKEN")

# OpenRouter API settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "google/gemma-3-1b-it:free" 

# Database settings
DATABASE_NAME = "recipes.db"

# Language settings
LANGUAGE = os.getenv("LANGUAGE", "en")  # Default language is English, can be 'en' or 'ru'

# Recipe categories
CATEGORIES = ["Завтраки", "Супы", "Обеды", "Десерты", "Закуски", "Напитки"] if LANGUAGE == "ru" else \
            ["Breakfasts", "Soups", "Lunches", "Desserts", "Snacks", "Drinks"]

# AI prompt template
AI_PROMPT_TEMPLATE = """
Привет. Ты повар мирового класса, специализирующийся на домашней еде. От твоего ответа зависит, вкусно поедят люди или нет.

---

{user_query}

---

Ответь пошагово, лаконично и убедительно.
""" if LANGUAGE == "ru" else """
Hello. You are a world-class chef specializing in home cooking. People's delicious meals depend on your answer.

---

{user_query}

---

Answer step by step, concisely and convincingly.
"""

# Maximum message length for Telegram
MAX_MESSAGE_LENGTH = 4000