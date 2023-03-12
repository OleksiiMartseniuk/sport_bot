import uuid
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from programs.import_file import process_import
from programs import db as db_program
from user import db as db_user

from config import DOCUMENTS_ROOT


logger = logging.getLogger(__name__)


class DownloadFile(StatesGroup):
    waiting_file = State()


async def import_start(message: types.Message,  state: FSMContext):
    text = "Загрузите файл '<b>.csv</b>' \n\n"\
           "Обязательные поля [<b>category_title, program_title,"\
           " exercise_tile exercise_number_approaches,"\
           " exercise_number_repetitions, exercise_day,"\
           " exercise_image</b>]\n\n"\
           "<b>category_title</b> - Названия категории\n"\
           "<b>program_title</b> - Названия программы тренировок\n"\
           "<b>exercise_tile</b> - Названия упражнения\n"\
           "<b>exercise_number_approaches</b> - Количество подходов\n"\
           "<b>exercise_number_repetitions</b> - Количество повторений\n"\
           "<b>exercise_day</b> - День недели в формате цифр [Пн-0, Вт-1,"\
           " Ср-2, Чт-3, Пт-4, Сб-5, Вс-6]\n"\
           "<b>exercise_image</b> - Ссылка на изображения\n"
    await message.answer(text=text, parse_mode=types.ParseMode.HTML)
    await state.set_state(DownloadFile.waiting_file.state)


async def download_doc(message: types.Message, state: FSMContext):
    if not message.document:
        await message.answer("Загрузите файл иле отмените действие /cancel")
        return

    error_message = "Что-то пошло не так!!!"
    file_name = f"{DOCUMENTS_ROOT}/{uuid.uuid4()}.csv"
    try:
        await message.document.download(destination_file=file_name)
    except Exception as e:
        await message.answer(error_message)
        logger.error(
            "Error not download file user[%s] massage: %s",
            message.from_user.id,
            str(e)
        )
    else:
        await message.answer("Идет обработка подождите...")
        user = await db_user.get_user(telegram_id=message.from_user.id)
        try:
            await process_import(file_path=file_name)
        except Exception as e:
            await message.answer(error_message)
            await db_program.insert_file(
                user_id=user.id,
                file_name=file_name.split("/")[-1],
                done=False
            )
            logger.error(
                "Error write in database file_path[%s] user[%s] massage:%s",
                file_name,
                message.from_user.id,
                str(e)
            )
        else:
            await db_program.insert_file(
                user_id=user.id,
                file_name=file_name.split("/")[-1],
                done=True
            )
            await message.answer("Обработка завершена данные записаны!!!")
    finally:
        await state.finish()


def register_handlers_import_file(dp: Dispatcher):
    dp.register_message_handler(
        import_start,
        commands="import_file",
        state="*"
    )
    dp.register_message_handler(
        download_doc,
        state=DownloadFile.waiting_file,
        content_types=[types.ContentType.DOCUMENT, types.ContentType.TEXT]
    )
