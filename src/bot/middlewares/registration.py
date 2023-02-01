import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from user import db as user_db


logger = logging.getLogger(__name__)


class RegistrationMiddleware(BaseMiddleware):

    async def on_process_message(self, message: types.Message, data: dict):
        user = await user_db.get_user(telegram_id=message.from_user.id)
        if not user:
            await user_db.create_user(
                name=message.from_user.full_name,
                telegram_id=message.from_user.id,
            )
            logger.info(
                "User telegram_id %s is registration.",
                message.from_user.id
            )
