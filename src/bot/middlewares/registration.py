import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from user import db as user_db


logger = logging.getLogger(__name__)


class RegistrationMiddleware(BaseMiddleware):

    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user
        elif update.callback_query:
            user = update.callback_query.from_user
        else:
            return

        user = await user_db.get_user(telegram_id=user.id)
        if not user:
            await user_db.create_user(
                name=user.full_name,
                telegram_id=user.id,
            )
            logger.info(
                "User telegram_id %s is registration.",
                user.id
            )
