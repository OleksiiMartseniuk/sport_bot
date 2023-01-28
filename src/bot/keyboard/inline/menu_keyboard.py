from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from programs import service

menu_cd = CallbackData(
    "show_menu",
    "level",
    "category",
    "program",
    "day",
    "exercises"
)


def make_callback_data(
    level: int,
    category: int = 0,
    program: int = 0,
    day: str = "",
    exercises: int = 0,
) -> str:
    return menu_cd.new(
        level=level,
        category=category,
        program=program,
        day=day,
        exercises=exercises
    )


async def category_keyboard() -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0

    markup = InlineKeyboardMarkup()

    categories = await service.get_category_list()

    for category in categories:
        text = f"{category.title.capitalize()}"
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category.id
        )
        markup.row(
            InlineKeyboardButton(text=text, callback_data=callback_data)
        )

    return markup


async def program_keyboard(category_id: int) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1

    markup = InlineKeyboardMarkup()

    programs = await service.get_programs_list(category_id)

    for program in programs:
        text = f"{program.title.capitalize()}"
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category_id,
            program=program.id
        )
        markup.row(
            InlineKeyboardButton(text=text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup


async def day_keyboard(
    category_id: int,
    program_id: int
) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup()

    day_list = await service.get_day_list(program_id)

    for day in day_list:
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category_id,
            program=program_id,
            day=day
        )
        markup.insert(
            InlineKeyboardButton(
                text=day.capitalize(),
                callback_data=callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1,
                category=category_id
            )
        )
    )
    return markup


async def exercises_all_keyboard(
    category_id: int,
    program_id: int,
    day: str
) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 3

    markup = InlineKeyboardMarkup()

    exercises_day = await service.get_exercises_list(program_id, day)

    for exercises in exercises_day:
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category_id,
            program=program_id,
            day=day,
            exercises=exercises.id
        )
        markup.row(
            InlineKeyboardButton(
                text=exercises.title.capitalize(),
                callback_data=callback_data
            )
        )

    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1,
                category=category_id,
                program=program_id
            )
        )
    )
    return markup


async def exercises_keyboard(
    category_id: int,
    program_id: int,
    day: str,
    exercises_id: int
) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 4

    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1,
                category=category_id,
                program=program_id,
                day=day
            )
        )
    )
    return markup
