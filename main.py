import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from config import TOKEN
from handlers.user_handlers import router as user_router
from database.db import init_db

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)  # TOKEN is loaded from .env via config.py
dp = Dispatcher()

# Register routers
dp.include_router(user_router)

# Main router
main_router = Router()

@main_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Handle the /start command."""
    from translations import get_text
    
    name = message.from_user.full_name if message.from_user else 'Guest'
    await message.answer(get_text("welcome_message", name=name))
    
    # Send main menu
    from keyboards.keyboards import get_main_menu_keyboard
    await message.answer(get_text("choose_menu_item"), reply_markup=get_main_menu_keyboard())

dp.include_router(main_router)

async def main() -> None:
    # Initialize database
    await init_db()
    
    # Start the bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.info("Starting bot")
    asyncio.run(main())