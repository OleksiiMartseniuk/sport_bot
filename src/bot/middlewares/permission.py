import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

from user import db as db_user


logger = logging.getLogger(__name__)


class PermissionMiddleware(BaseMiddleware):

    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
            await self.admin_handlers(user=user, command=update.message.text)
        elif update.callback_query:
            user = update.callback_query.from_user.id
        else:
            return

        users = await db_user.get_not_active_users()
        if user in users:
            raise CancelHandler()

    async def admin_handlers(self, user: int, command: str):
        commands_admin = ["/import_file"]
        if command in commands_admin:
            users_admin = await db_user.get_active_admins()
            if user not in users_admin:
                raise CancelHandler()
            return
