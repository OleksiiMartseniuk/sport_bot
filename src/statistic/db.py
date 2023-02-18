from datetime import datetime

from sqlalchemy import insert, update, select, and_, desc
from sqlalchemy import func

from database import async_session

from .models import statistics_program, statistics_exercises
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


async def get_statistics_program(id: int) -> schemas.StatisticsProgram | None:
    query = select(statistics_program).where(
        statistics_program.c.id == id
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


async def insert_statistics_exercises(
    statistics_program_id: int,
    exercises_id: int,
    done: bool,
    created: datetime = datetime.now()
) -> None:
    query = insert(statistics_exercises).values(
        statistics_program_id=statistics_program_id,
        exercises_id=exercises_id,
        done=done,
        created=created
    )
    async with async_session() as session:
        await session.execute(query)
        await session.commit()


async def get_statistics_exercises(
    program_id: int,
    exercises_id: int,
    created_filter: datetime = datetime.now()
) -> schemas.StatisticsExercises | None:
    query = select(statistics_exercises).where(
        and_(
            statistics_exercises.c.statistics_program_id == program_id,
            statistics_exercises.c.exercises_id == exercises_id,
            func.DATE(statistics_exercises.c.created) == created_filter.date()
        )
    )
    async with async_session() as session:
        result = await session.execute(query)
        item = result.fetchone()
        return schemas.StatisticsExercises(*item) if item else None


async def get_list_exercises(
        program_id: int,
        offset: int = 0,
        limit: int = 8
) -> list[schemas.StatisticsExercises | None]:
    query = select(statistics_exercises).where(
        statistics_exercises.c.statistics_program_id == program_id
    ).order_by(
        desc(statistics_exercises.c.created)
    ).offset(offset).limit(limit)
    async with async_session() as session:
        result = await session.execute(query)
        items = result.fetchall()
        return [schemas.StatisticsExercises(*item) for item in items]


async def get_count_exercises(
    statistics_program_id: int
) -> int:
    query = select(func.count(statistics_exercises.c.id)).where(
        statistics_exercises.c.statistics_program_id == statistics_program_id
    )
    async with async_session() as session:
        result = await session.execute(query)
        return result.scalar()


async def get_list_program(
    user_id: int
) -> list[schemas.StatisticsProgram | None]:
    query = select(statistics_program).where(
        statistics_program.c.user_id == user_id
    ).order_by(desc(statistics_program.c.finish_time))
    async with async_session() as session:
        result = await session.execute(query)
        items = result.fetchall()
        return [schemas.StatisticsProgram(*item) for item in items]
