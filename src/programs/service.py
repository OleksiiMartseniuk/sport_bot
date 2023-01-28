from sqlalchemy import select, update

from database import async_session
from programs.models import category, program, exercises, program_exercises

from . import schemas


async def get_category_list() -> list[schemas.Category]:
    async with async_session() as session:
        result = await session.execute(select(category))
        return [schemas.Category(*item) for item in result.fetchall()]


async def get_programs_list(category_id: int) -> list[schemas.Program]:
    async with async_session() as session:
        query = select(
            program.c.id,
            program.c.title,
            program.c.created
        ).where(program.c.category_id == category_id)
        result = await session.execute(query)
        return [schemas.Program(*item) for item in result.fetchall()]


async def get_exercises_list(
    program_id: int,
    day: int | None = None
) -> list[schemas.Exercises]:
    async with async_session() as session:
        query = select(exercises).join(program_exercises).where(
            program_exercises.c.program_id == program_id)
        if day is not None:
            query = query.where(exercises.c.day == day).order_by(
                exercises.c.id)
        else:
            query = query.order_by(exercises.c.day, exercises.c.id)
        result = await session.execute(query)
        return [schemas.Exercises(*item) for item in result.fetchall()]


async def get_exercises(exercises_id: int) -> schemas.Exercises | None:
    async with async_session() as session:
        query = select(exercises).where(exercises.c.id == exercises_id)
        result = await session.execute(query)
        item = result.fetchone()
        return schemas.Exercises(*item) if item else None


async def get_day_list(program_id: int) -> list[int]:
    async with async_session() as session:
        query = select(exercises.c.day).join(program_exercises).where(
            program_exercises.c.program_id == program_id
            ).distinct().order_by(exercises.c.day)
        result = await session.execute(query)
        return [day[0] for day in result.fetchall()]


async def set_telegram_image_id(exercises_id: int, file_id: str) -> None:
    async with async_session() as session:
        query = update(exercises).where(exercises.c.id == exercises_id).values(
            telegram_image_id=file_id
        )
        await session.execute(query)
        await session.commit()
