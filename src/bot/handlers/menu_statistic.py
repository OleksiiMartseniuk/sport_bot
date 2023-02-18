import logging


from aiogram import Dispatcher, types

from bot.utils import rate_limit
from bot.keyboard.inline import statistic_keyboard
from statistic import service as service_statistic


logger = logging.getLogger(__name__)


@rate_limit(3)
async def statistic_start(message: types.Message):
    await list_program(message)


async def list_program(massage: types.Message | types.CallbackQuery, **kwargs):
    text = "Выберите программу:"
    if isinstance(massage, types.Message):
        markup = await statistic_keyboard.program_keyboard(
            telegram_id=massage.from_user.id
        )
        await massage.answer(
            text=text,
            parse_mode=types.ParseMode.HTML,
            reply_markup=markup
        )
    elif isinstance(massage, types.CallbackQuery):
        callback: types.CallbackQuery = massage
        markup = await statistic_keyboard.program_keyboard(
            telegram_id=massage.from_user.id
        )
        await callback.message.edit_text(
            text=text,
            reply_markup=markup,
            parse_mode=types.ParseMode.HTML
        )


async def get_statistics(
    callback: types.CallbackQuery,
    programs_statistic: int,
    offset: int,
    cache_time: int
):
    await callback.answer(cache_time=cache_time)
    markup = await statistic_keyboard.statistic_keyboard(
        programs_statistic=programs_statistic,
        offset=offset
    )
    text = await service_statistic.get_current_statistic(
        telegram_user_id=callback.from_user.id,
        offset=offset
    )
    description = "\n✅ / ❌ Статус выполнения упражнения\n"\
                  "🕔 Время завершения упражнения\n"
    text += description
    await callback.message.edit_text(
        text=text,
        reply_markup=markup,
        parse_mode=types.ParseMode.HTML
    )


async def navigate(call: types.CallbackQuery, callback_data: dict):
    CACHE_TIME = 1

    current_level = callback_data.get("level", "0")
    programs_statistic = callback_data.get("programs_statistic", 0)
    offset = callback_data.get("offset", 0)

    levels = {
        "0": list_program,
        "1": get_statistics,
    }

    current_level_function = levels[current_level]

    await current_level_function(
        call,
        programs_statistic=int(programs_statistic),
        offset=int(offset),
        cache_time=CACHE_TIME
    )


def register_handlers_statistic(dp: Dispatcher):
    dp.register_message_handler(statistic_start, commands="statistic")
    dp.register_callback_query_handler(
        navigate,
        statistic_keyboard.menu_pr.filter()
    )
