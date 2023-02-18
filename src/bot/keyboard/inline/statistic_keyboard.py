from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from statistic import db as db_statistic
from user import db as db_user
from programs import db as db_program


menu_pr = CallbackData("show_menu_pr", "level", "programs_statistic", "offset")


def make_callback_data(
    level: int,
    programs_statistic: int = 0,
    offset: int = 0,
) -> str:
    return menu_pr.new(
        level=level,
        programs_statistic=programs_statistic,
        offset=offset
    )


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
            programs_statistic=program_statistic.id,
        )
        markup.row(
            InlineKeyboardButton(text=text, callback_data=callback_data)
        )
    return markup


async def statistic_keyboard(
    programs_statistic: int,
    offset: int,
    limit: int = 8
) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1

    markup = InlineKeyboardMarkup()

    count = await db_statistic.get_count_exercises(
        statistics_program_id=programs_statistic
    )

    def max_offset() -> int:
        return int(count / limit) * limit

    next = 0 if offset + limit >= count else offset + limit
    previous = max_offset() if offset - limit < 0 else offset - limit

    markup.insert(
        InlineKeyboardButton(
            text="<",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL,
                programs_statistic=programs_statistic,
                offset=previous
            )
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text=f"{int(offset/limit) + 1}/{int(count/limit) + 1}",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL,
                programs_statistic=programs_statistic
            )
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text=">",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL,
                programs_statistic=programs_statistic,
                offset=next
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup
