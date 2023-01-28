from aiogram import Bot
from aiogram.types import BotCommand


async def setup_bot_commands(bot: Bot):
    bot_commands = [
        BotCommand(
            command="/program",
            description="Выберите программу тренировок"
        ),
    ]
    await bot.set_my_commands(bot_commands)
