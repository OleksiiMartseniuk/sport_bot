from aiogram.types import InlineKeyboardMarkup

from bot.keyboard.inline import statistic_keyboard


def rate_limit(limit: int, key=None):
    """
    Decorator for configuring rate limit and key in different functions.

    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


async def get_program_menu(
    telegram_id: int
) -> tuple[InlineKeyboardMarkup, str]:
    markup, create = await statistic_keyboard.program_keyboard(
        telegram_id=telegram_id
    )
    if create:
        text = "Выберите программу:"
    else:
        text = "У вас не выбрана программа тренировок. Перейдите в /program"
    return markup, text
