from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from programs.constants import DAY_WEEK
from programs import db as db_program
from statistic.service import (
    check_active_statistics_program,
    get_active_statistics_program,
    get_statistics_exercises
)


menu_cd = CallbackData(
    "show_menu",
    "level",
    "category",
    "program",
    "day",
    "exercises"
)
subscribe_program = CallbackData(
    "subscribe_program",
    "user",
    "program",
    "category"
)
exercise_execution = CallbackData(
    "exercise_execution",
    "done",
    "category",
    "program",
    "statistics_program",
    "day",
    "exercises"

)


def make_callback_data(
    level: int,
    category: int = 0,
    program: int = 0,
    day: int = 0,
    exercises: int = 0,
) -> str:
    return menu_cd.new(
        level=level,
        category=category,
        program=program,
        day=day,
        exercises=exercises
    )


async def category_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0

    markup = InlineKeyboardMarkup()

    categories = await db_program.get_category_list()
    active = await get_active_statistics_program(telegram_id=telegram_id)
    if active:
        program = await db_program.get_program(id=active.program_id)

    for category in categories:
        text = ""
        if active:
            text = f"{'🔵 ' if program.category_id == category.id else ''}"
        text += f"{category.title.capitalize()}"

        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category.id
        )
        markup.row(
            InlineKeyboardButton(text=text, callback_data=callback_data)
        )

    return markup


async def program_keyboard(
    category_id: int,
    telegram_id: int
) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1

    markup = InlineKeyboardMarkup()

    programs = await db_program.get_programs_list(category_id)
    active = await get_active_statistics_program(telegram_id=telegram_id)

    for program in programs:
        text = ""
        if active:
            text = f"{'🔵 ' if active.program_id == program.id else ''}"
        text += f"{program.title.capitalize()}"
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
    program_id: int,
    user_id: int
) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup()
    statistic_program = await check_active_statistics_program(
        telegram_user_id=user_id,
        program_id=program_id
    )
    text_subscribe = "Отписаться" if statistic_program else "Подписаться"
    day_list = await db_program.get_day_list(program_id)

    for day in day_list:
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category_id,
            program=program_id,
            day=day
        )
        markup.insert(
            InlineKeyboardButton(
                text=DAY_WEEK.get(day, "").capitalize(),
                callback_data=callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text=text_subscribe,
            callback_data=subscribe_program.new(
                user=user_id,
                program=program_id,
                category=category_id
            )
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
    day: int
) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 3

    markup = InlineKeyboardMarkup()

    exercises_day = await db_program.get_exercises_list(program_id, day)

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
    day: int,
    exercises_id: int,
    user_id: int
) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 4

    markup = InlineKeyboardMarkup()

    date_now = datetime.now()

    active_program = await check_active_statistics_program(
        telegram_user_id=user_id,
        program_id=program_id
    )

    if active_program:
        active_exercises = await get_statistics_exercises(
            telegram_id=user_id,
            program_id=active_program.id,
            exercises_id=exercises_id
        )
        if not active_exercises and date_now.weekday() == day:
            markup.insert(
                InlineKeyboardButton(
                    "❌ Провалено",
                    callback_data=exercise_execution.new(
                        done=0,
                        category=category_id,
                        program=program_id,
                        statistics_program=active_program.id,
                        day=day,
                        exercises=exercises_id
                    )
                )
            )
            markup.insert(
                InlineKeyboardButton(
                    "✅ Выполнено",
                    callback_data=exercise_execution.new(
                        done=1,
                        category=category_id,
                        program=program_id,
                        statistics_program=active_program.id,
                        day=day,
                        exercises=exercises_id
                    )
                )
            )
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
