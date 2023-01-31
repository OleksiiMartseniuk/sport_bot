import logging

from collections import defaultdict

from aiogram import Dispatcher, types

from config import MEDIA_ROOT, MENU_IMAGE_FILE_ID
from programs import db as db_program
from programs.constants import DAY_WEEK
from bot.keyboard.inline import menu_keyboard
from bot.utils import rate_limit


logger = logging.getLogger(__name__)


@rate_limit(3)
async def program_start(message: types.Message):
    await list_category(message)


async def list_category(
    massage: types.Message | types.CallbackQuery,
    **kwargs
):
    markup = await menu_keyboard.category_keyboard()
    text = "Выберите категорию:"
    if isinstance(massage, types.Message):
        await massage.answer_photo(
            photo=MENU_IMAGE_FILE_ID,
            caption=text,
            parse_mode=types.ParseMode.HTML,
            reply_markup=markup
        )
    elif isinstance(massage, types.CallbackQuery):
        callback: types.CallbackQuery = massage
        await callback.answer(cache_time=kwargs.get("cache_time"))
        await callback.message.edit_caption(
            caption=text,
            reply_markup=markup,
            parse_mode=types.ParseMode.HTML
        )


async def list_programs(
    callback: types.CallbackQuery,
    category: int,
    cache_time: int,
    **kwargs
):
    await callback.answer(cache_time=cache_time)
    markup = await menu_keyboard.program_keyboard(category)
    await callback.message.edit_caption(
        caption="<b>Выберите программу:</b>",
        reply_markup=markup,
        parse_mode=types.ParseMode.HTML
    )


async def list_day(
    callback: types.CallbackQuery,
    category: int,
    program: int,
    cache_time: int,
    **kwargs
):
    await callback.answer(cache_time=cache_time)
    markup = await menu_keyboard.day_keyboard(category, program)
    exercises = await db_program.get_exercises_list(program_id=program)
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
    await callback.message.edit_caption(
        caption=text,
        reply_markup=markup,
        parse_mode=types.ParseMode.HTML
    )


async def list_exercises(
    callback: types.CallbackQuery,
    category: int,
    program: int,
    day: int,
    cache_time: int,
    **kwargs
):
    await callback.answer(cache_time=cache_time)
    markup = await menu_keyboard.exercises_all_keyboard(category, program, day)
    day_text = DAY_WEEK.get(day, "").capitalize()
    media = types.InputMediaPhoto(
        media=MENU_IMAGE_FILE_ID,
        caption=f"<b>{day_text}</b>",
        parse_mode=types.ParseMode.HTML
    )
    await callback.message.edit_media(media=media, reply_markup=markup)


async def get_exercises(
    callback: types.CallbackQuery,
    category: int,
    program: int,
    day: int,
    exercises: int,
    cache_time: int
):
    await callback.answer(cache_time=cache_time)
    markup = await menu_keyboard.exercises_keyboard(
        category, program, day, exercises
    )
    exercises_data = await db_program.get_exercises(exercises)
    if exercises_data:
        text = f"<b>{exercises_data.title.capitalize()}</b>\n\n"\
              f"Количество подходов [{exercises_data.number_approaches}]\n"\
              f"Количество повторений [{exercises_data.number_repetitions}]\n"

        if exercises_data.telegram_image_id:
            media = types.InputMediaPhoto(
                media=exercises_data.telegram_image_id,
                caption=text,
                parse_mode=types.ParseMode.HTML
            )
            await callback.message.edit_media(media=media, reply_markup=markup)
        else:
            image = open(f"{MEDIA_ROOT}/{exercises_data.image}", "rb")
            media = types.InputMediaPhoto(
                media=image,
                caption=text,
                parse_mode=types.ParseMode.HTML
            )
            data = await callback.message.edit_media(
                media=media,
                reply_markup=markup
            )
            await db_program.set_telegram_image_id(
                exercises_id=exercises_data.id,
                file_id=data.photo[-1].file_id
            )
            logger.info("Image %s for exercise (id:%s) uploaded to telegram.",
                        exercises_data.image,
                        exercises_data.id)
    else:
        logger.error(
            "Not exist exercises [category=%s, program=%s,"
            " day=%s, exercises=%s]",
            category,
            program,
            day,
            exercises
        )
        await callback.message.edit_text(
            "Не найдено упражнения",
            reply_markup=markup
        )


async def navigate(call: types.CallbackQuery, callback_data: dict):
    CACHE_TIME = 1

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
        exercises=int(exercises),
        cache_time=CACHE_TIME
    )


def register_handlers_program(dp: Dispatcher):
    dp.register_message_handler(program_start, commands="program")
    dp.register_callback_query_handler(
        navigate,
        menu_keyboard.menu_cd.filter()
    )
