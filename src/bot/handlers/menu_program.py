from collections import defaultdict

from aiogram import Dispatcher, types

from programs import service
from bot.keyboard.inline import menu_keyboard


async def program_start(message: types.Message):
    await list_category(message)


async def list_category(
    massage: types.Message | types.CallbackQuery,
    **kwargs
):
    markup = await menu_keyboard.category_keyboard()
    text = "Выберите категорию:"
    if isinstance(massage, types.Message):
        await massage.answer(text, reply_markup=markup)
    elif isinstance(massage, types.CallbackQuery):
        callback: types.CallbackQuery = massage
        await callback.message.edit_text(text, reply_markup=markup)


async def list_programs(callback: types.CallbackQuery, category, **kwargs):
    markup = await menu_keyboard.program_keyboard(category)
    await callback.message.edit_text(
        "Выберите программу:",
        reply_markup=markup
    )


async def exercises(callback: types.CallbackQuery, category, program):
    markup = await menu_keyboard.exercises_keyboard(category, program)

    exercises = await service.get_exercises(program_id=program)
    day_week = defaultdict(list)
    for e in exercises:
        day_week[e.day].append(
            f"⸰ {e.title} - {e.number_approaches} - [{e.number_repetitions}]"
        )
    text_list = []
    for day in day_week:
        text_list.append(f"\n<b>{day.capitalize()}</b>")
        text_list.extend(day_week[day])
    text = "\n".join(text_list)
    await callback.message.edit_text(
        text,
        reply_markup=markup,
        parse_mode=types.ParseMode.HTML
    )


async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level", "0")
    category = callback_data.get("category", 0)
    program = callback_data.get("program", 0)

    levels = {
        "0": list_category,
        "1": list_programs,
        "2": exercises
    }

    current_level_function = levels[current_level]

    await current_level_function(
        call,
        category=int(category),
        program=int(program)
    )


def register_handlers_program(dp: Dispatcher):
    dp.register_message_handler(program_start, commands="program")
    dp.register_callback_query_handler(
        navigate,
        menu_keyboard.menu_cd.filter()
    )
