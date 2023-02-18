import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from user import db as db_user


logger = logging.getLogger(__name__)


class RegistrationMiddleware(BaseMiddleware):

    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user
        elif update.callback_query:
            user = update.callback_query.from_user
        else:
            return

        user_db = await db_user.get_user(telegram_id=user.id)
        if not user_db:
            await db_user.create_user(
                name=user.first_name,
                telegram_id=user.id,
            )
            logger.info(
                "User telegram_id %s is registration.",
                user.id
            )
