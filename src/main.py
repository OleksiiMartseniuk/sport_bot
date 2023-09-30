import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.utils.executor import start_webhook
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot.handlers.menu_program import register_handlers_program
from bot.handlers.menu_statistic import register_handlers_statistic
from bot.handlers.import_file import register_handlers_import_file
from bot.handlers.base import register_handlers_base

from bot.handlers.commands import setup_bot_commands

from bot.middlewares.throttling import ThrottlingMiddleware
from bot.middlewares.registration import RegistrationMiddleware
from bot.middlewares.permission import PermissionMiddleware

from config import TELEGRAM_TOKEN


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

bot = Bot(token=TELEGRAM_TOKEN)

dp = Dispatcher(bot, storage=RedisStorage2())

# Setup middleware
dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(ThrottlingMiddleware())
dp.middleware.setup(RegistrationMiddleware())
dp.middleware.setup(PermissionMiddleware())

# Register Handlers
register_handlers_base(dp)
register_handlers_program(dp)
register_handlers_statistic(dp)
register_handlers_import_file(dp)


# webhook settings
WEBHOOK_HOST = 'http://localhost'
WEBHOOK_PATH = '/webhook/{TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001


async def on_startup(dp: Dispatcher):
    await bot.set_webhook(WEBHOOK_URL)
    await setup_bot_commands(bot)


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
