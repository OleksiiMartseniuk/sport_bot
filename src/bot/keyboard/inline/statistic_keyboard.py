from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from bot.utils import get_max_offset

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


async def program_keyboard(
    telegram_id: int
) -> tuple[InlineKeyboardMarkup, bool]:
    CURRENT_LEVEL = 0
    CREATE = True

    markup = InlineKeyboardMarkup()
    user = await db_user.get_user(telegram_id=telegram_id)
    programs_statistic = await db_statistic.get_list_program(user.id)
    if not programs_statistic:
        CREATE = False

    for program_statistic in programs_statistic:
        program = await db_program.get_program(id=program_statistic.program_id)
        text = f"{'🔵 ' if not program_statistic.finish_time else ''}"\
               f"{program.title.capitalize()}"
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            programs_statistic=program_statistic.id,
        )
        markup.row(
            InlineKeyboardButton(text=text, callback_data=callback_data)
        )
    return markup, CREATE


async def get_program_menu(
    telegram_id: int
) -> tuple[InlineKeyboardMarkup, str]:
    markup, create = await program_keyboard(
        telegram_id=telegram_id
    )
    if create:
        text = "Выберите программу:"
    else:
        text = "У вас не выбрана программа тренировок. Перейдите в /program"
    return markup, text


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

    next = 0 if offset + limit >= count else offset + limit
    previous = get_max_offset(count, limit) if offset - limit < 0 \
        else offset - limit
    page_max = int(count/limit)

    # more than one page
    if page_max:
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
                text=f"{int(offset/limit) + 1} / {page_max}",
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
