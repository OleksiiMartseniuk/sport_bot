from sqlalchemy import insert, select

from database import async_session

from .models import user
from . import schemas


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


async def get_user(telegram_id: str) -> schemas.User | None:
    query = select(user).where(user.c.telegram_id == telegram_id)
    result = await session.execute(query)
    user_data = result.fetchone()
    return schemas.User(*user_data) if user else None
