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


async def get_exercises_list(
    program_id: int,
    day: str = ""
) -> list[schemas.Exercises]:
    async with async_session() as session:
        query = select(exercises).join(program_exercises).where(
            program_exercises.c.program_id == program_id)
        if day:
            query = query.where(exercises.c.day == day)
        result = await session.execute(query)
        return [schemas.Exercises(*item) for item in result.fetchall()]


async def get_exercises(exercises_id: int) -> schemas.Exercises | None:
    async with async_session() as session:
        query = select(exercises).where(exercises.c.id == exercises_id)
        result = await session.execute(query)
        item = result.fetchone()
        return schemas.Exercises(*item) if item else None


async def get_day_list(program_id: int) -> list[str]:
    day_week_key = [
        "понедельник", "вторник", "среда",
        "четверг", "пятница", "суббота", "воскресения"]
    async with async_session() as session:
        query = select(exercises.c.day).join(program_exercises).where(
            program_exercises.c.program_id == program_id).distinct()
        result = await session.execute(query)
        day_list = [day[0] for day in result.fetchall()]
        return sorted(day_list, key=day_week_key.index)
