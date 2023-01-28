import logging

from collections import defaultdict

from aiogram import Dispatcher, types

from config import MEDIA_ROOT
from programs import service
from programs.constants import DAY_WEEK
from bot.keyboard.inline import menu_keyboard


logger = logging.getLogger(__name__)


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


async def list_programs(
    callback: types.CallbackQuery,
    category: int,
    **kwargs
):
    markup = await menu_keyboard.program_keyboard(category)
    await callback.message.edit_text(
        "Выберите программу:",
        reply_markup=markup
    )


async def list_day(
    callback: types.CallbackQuery,
    category: int,
    program: int,
    **kwargs
):
    markup = await menu_keyboard.day_keyboard(category, program)
    exercises = await service.get_exercises_list(program_id=program)
    day_week = defaultdict(list)
    for e in exercises:
        day_week[e.day].append(
            f"⸰ {e.title} - {e.number_approaches} - [{e.number_repetitions}]"
        )
    text_list = []
    for day in day_week:
        day_text = DAY_WEEK.get(day, "").capitalize()
        text_list.append(f"\n<b>{day_text}</b>")
        text_list.extend(day_week[day])
    text = "\n".join(text_list)
    await callback.message.edit_text(
        text,
        reply_markup=markup,
        parse_mode=types.ParseMode.HTML
    )


async def list_exercises(
    callback: types.CallbackQuery,
    category: int,
    program: int,
    day: int,
    **kwargs
):
    markup = await menu_keyboard.exercises_all_keyboard(category, program, day)
    day_text = DAY_WEEK.get(day, "").capitalize()
    await callback.message.edit_text(
        f"<b>{day_text}</b>",
        reply_markup=markup,
        parse_mode=types.ParseMode.HTML
    )


async def get_exercises(
    callback: types.CallbackQuery,
    category: int,
    program: int,
    day: int,
    exercises: int
):
    markup = await menu_keyboard.exercises_keyboard(
        category, program, day, exercises
    )
    # TODO fix image
    exercises_data = await service.get_exercises(exercises)
    if exercises_data:
        text = f"<b>{exercises_data.title.capitalize()}</b>\n"\
              f"Количество подходов [{exercises_data.number_approaches}]\n"\
              f"Количество повторений [{exercises_data.number_repetitions}]\n"\
              f"Image {exercises_data.image}"
        image = open(f"{MEDIA_ROOT}/{exercises_data.image}", "rb")
        image_file = types.InputFile(image)
        logger.info(image_file)
        print(image_file)
        media = types.InputMediaPhoto(media=image_file, caption="asdsad")
        print(media)
    else:
        logger.error(
            "Not exist exercises [category=%s, program=%s,"
            " day=%s, exercises=%s]",
            category,
            program,
            day,
            exercises
        )
        text = "Не найдено упражнения"
    # await callback.message.answer_photo(media)
    await callback.message.edit_text(
        text,
        reply_markup=markup,
        parse_mode=types.ParseMode.HTML
    )


async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level", "0")
    category = callback_data.get("category", 0)
    program = callback_data.get("program", 0)
    day = callback_data.get("day", 0)
    exercises = callback_data.get("exercises", 0)

    levels = {
        "0": list_category,
        "1": list_programs,
        "2": list_day,
        "3": list_exercises,
        "4": get_exercises
    }

    current_level_function = levels[current_level]

    await current_level_function(
        call,
        category=int(category),
        program=int(program),
        day=int(day),
        exercises=int(exercises)
    )


def register_handlers_program(dp: Dispatcher):
    dp.register_message_handler(program_start, commands="program")
    dp.register_callback_query_handler(
        navigate,
        menu_keyboard.menu_cd.filter()
    )
