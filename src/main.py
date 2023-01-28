import logging

from aiogram import Bot, Dispatcher, executor

from bot.handlers.menu_program import register_handlers_program
from bot.handlers.commands import setup_bot_commands

from config import TELEGRAM_TOKEN


logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Register Handlers
register_handlers_program(dp)


async def on_startup(dp: Dispatcher):
    await setup_bot_commands(bot)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
