import logging

from sqlalchemy import insert, select

from database import async_session

from .models import user
from . import schemas


logger = logging.getLogger(__name__)


async def create_user(
    name: str,
    telegram_id: int,
    is_admin: bool = False,
    is_active: bool = True
) -> None:
    query = insert(user).values(
        name=name,
        telegram_id=telegram_id,
        is_admin=is_admin,
        is_active=is_active
    )
    async with async_session() as session:
        await session.execute(query)
        await session.commit()


async def get_user(telegram_id: int) -> schemas.User | None:
    query = select(user).where(user.c.telegram_id == telegram_id)
    async with async_session() as session:
        result = await session.execute(query)
        user_data = result.fetchone()
        if user_data:
            return schemas.User(*user_data)
        else:
            logger.error("User telegram id %s not exist.", telegram_id)
            return None


async def get_not_active_users() -> list[int]:
    query = select(user.c.telegram_id).where(user.c.is_active == False)
    async with async_session() as session:
        result = await session.execute(query)
        return [user[0] for user in result.fetchall()]


async def get_active_admins() -> list[int]:
    query = select(user.c.telegram_id).where(
        user.c.is_active == True,
        user.c.is_admin == True,
    )
    async with async_session() as session:
        result = await session.execute(query)
        return [user[0] for user in result.fetchall()]
