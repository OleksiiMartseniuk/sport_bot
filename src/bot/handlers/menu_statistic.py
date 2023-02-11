import logging


from aiogram import Dispatcher, types

from statistic.service import get_current_statistic
from bot.utils import rate_limit


logger = logging.getLogger(__name__)


@rate_limit(3)
async def statistic_start(message: types.Message):
    text = await get_current_statistic(
        telegram_user_id=message.from_user.id
    )
    if text:
        description = "\n✅ / ❌ Статус выполнения упражнения\n"\
                      "🕔 Время завершения упражнения\n"
        text += description
    else:
        text = "Что-то пошло не так!!!"

    await message.answer(text=text, parse_mode=types.ParseMode.HTML)


def register_handlers_statistic(dp: Dispatcher):
    dp.register_message_handler(statistic_start, commands="statistic")
