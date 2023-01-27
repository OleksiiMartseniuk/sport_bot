from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from programs import service

menu_cd = CallbackData("show_menu", "level", "category", "program")


def make_callback_data(
    level: int,
    category: int = 0,
    program: int = 0,
) -> str:
    return menu_cd.new(
        level=level,
        category=category,
        program=program
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


async def exercises_keyboard(
    category_id: int,
    program_id: int
) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup()

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
