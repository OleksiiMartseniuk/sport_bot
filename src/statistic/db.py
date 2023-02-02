from datetime import datetime

from sqlalchemy import insert, update, select, and_

from database import async_session

from .models import statistics_program
from . import schemas


async def start_statistics_program(
    user_id: int,
    program_id: int,
    start_time: datetime = datetime.now()
) -> None:
    query = insert(statistics_program).values(
        user_id=user_id,
        program_id=program_id,
        start_time=start_time
    )
    async with async_session() as session:
        await session.execute(query)
        await session.commit()


async def end_statistics_program(
    statistics_program_id: int,
    finish_time: datetime = datetime.now()
) -> None:
    query = update(statistics_program).where(
        statistics_program.c.id == statistics_program_id
    ).values(finish_time=finish_time)
    async with async_session() as session:
        await session.execute(query)
        await session.commit()


async def get_active_statistics_program(
    user_id: int
) -> schemas.StatisticsProgram | None:
    query = select(statistics_program).where(
        and_(
            statistics_program.c.user_id == user_id,
            statistics_program.c.finish_time == None
        )
    )
    async with async_session() as session:
        result = await session.execute(query)
        item = result.fetchone()
        return schemas.StatisticsProgram(*item) if item else None


async def check_active_statistics_program(
    user_id: int,
    program_id: int
) -> schemas.StatisticsProgram | None:
    query = select(statistics_program).where(
        and_(
            statistics_program.c.user_id == user_id,
            statistics_program.c.program_id == program_id,
            statistics_program.c.finish_time == None
        )
    )
    async with async_session() as session:
        result = await session.execute(query)
        item = result.fetchone()
        return schemas.StatisticsProgram(*item) if item else None
