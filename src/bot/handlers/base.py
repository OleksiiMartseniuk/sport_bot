from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from user import db as db_user


async def cmd_start(message: types.Message):
    text_user = "Привет тебя приветствует sport-bot у тебя есть возможность "\
                "использовать приведение ниже команды для подержания себя "\
                "в форме:\n"\
                "/program       Выберите программу тренировок\n"\
                "/statistic     Статистика\n"

    text_user_admin = "\nДоступные команды администратора:\n"\
                      "/import_file     Импорт файла\n"

    users_admin = await db_user.get_active_admins()
    if message.from_user.id in users_admin:
        text_user += text_user_admin

    await message.answer(
        text_user,
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено")


def register_handlers_base(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
