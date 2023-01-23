from sqlalchemy import select

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


async def get_exercises(program_id: int, day: str = None) -> list:
    async with async_session() as session:
        query = select(exercises).join(program_exercises).where(
            program_exercises.c.program_id == program_id)
        if day:
            query = query.where(exercises.c.day == day)
        result = await session.execute(query)
        return [schemas.Exercises(*item) for item in result.fetchall()]
