from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from statistic import db as db_statistic
from user import db as db_user
from programs import db as db_program


menu_pr = CallbackData("show_menu_pr", "level", "program", "offset")


def make_callback_data(
    level: int,
    program: int = 0,
    offset: int = 0,
) -> str:
    return menu_pr.new(level=level, program=program, offset=offset)


async def program_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0

    markup = InlineKeyboardMarkup()
    user = await db_user.get_user(telegram_id=telegram_id)
    programs_statistic = await db_statistic.get_list_program(user.id)

    for program_statistic in programs_statistic:
        program = await db_program.get_program(id=program_statistic.program_id)
        text = f"{program.title.capitalize()}"
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            program=program.id
        )
        markup.row(
            InlineKeyboardButton(text=text, callback_data=callback_data)
        )
    return markup


async def statistic_keyboard(
    program_id: int,
    offset: int
) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1

    markup = InlineKeyboardMarkup()
    count_exercises = await db_statistic.get_count_exercises(
        program_id=program_id
    )
    callback_data = make_callback_data(
        level=CURRENT_LEVEL,
        program=program_id
    )
    markup.insert(
        InlineKeyboardButton(text="<", callback_data=callback_data)
    )
    markup.insert(
        InlineKeyboardButton(
            text=f"{offset}/{count_exercises}",
            callback_data=callback_data
        )
    )
    markup.insert(
        InlineKeyboardButton(text=">", callback_data=callback_data)
    )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup
