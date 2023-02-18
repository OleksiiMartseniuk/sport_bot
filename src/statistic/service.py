import logging

from collections import defaultdict
from datetime import datetime

from user import db as user_db
from programs import db as program_db
from programs.schemas import DAYS_WEEK

from .schemas import StatisticsExercises
from . import db as statistic_db


logger = logging.getLogger(__name__)


async def set_statistics_program(
    telegram_user_id: int,
    program_id: int,
    start_time: datetime = datetime.now(),
) -> None:
    user = await user_db.get_user(telegram_id=telegram_user_id)
    if not user:
        return

    statistics_program = await statistic_db.get_active_statistics_program(
        user_id=user.id
    )
    if statistics_program:
        if statistics_program.program_id == program_id:
            await statistic_db.end_statistics_program(
                statistics_program_id=statistics_program.id
            )
            logger.info(
                "User %s ending program %s",
                user.id,
                program_id
            )
            return
        else:
            await statistic_db.end_statistics_program(
                statistics_program_id=statistics_program.id
            )
            await statistic_db.start_statistics_program(
                user_id=user.id,
                program_id=program_id,
                start_time=start_time
            )
    else:
        await statistic_db.start_statistics_program(
            user_id=user.id,
            program_id=program_id,
            start_time=start_time
        )
    logger.info(
        "User %s installed program %s",
        user.id,
        program_id
    )


async def check_active_statistics_program(
    telegram_user_id: int,
    program_id: int
):
    user = await user_db.get_user(telegram_id=telegram_user_id)
    if not user:
        return
    return await statistic_db.check_active_statistics_program(
        user_id=user.id,
        program_id=program_id
    )


async def set_statistics_exercises(
    telegram_user_id: int,
    program_id: int,
    exercises_id: int,
    done: bool,
    created: datetime = datetime.now()
):
    user = await user_db.get_user(telegram_id=telegram_user_id)
    if not user:
        return

    statistics_program = await statistic_db.check_active_statistics_program(
        user_id=user.id,
        program_id=program_id
    )

    if not statistics_program:
        logger.error(
            "Not fund statistics_program user_id %s program_id %s",
            user.id,
            program_id
        )
        return

    await statistic_db.insert_statistics_exercises(
        statistics_program_id=statistics_program.id,
        exercises_id=exercises_id,
        done=done,
        created=created
    )


async def get_program_statistic_text(
    programs_statistic: int,
    offset: int = 0
) -> str | None:
    statistics_program = await statistic_db.get_statistics_program(
        id=programs_statistic,
    )
    if not statistics_program:
        logger.info(f"Not exist active program {programs_statistic}")
        return None

    program = await program_db.get_program(id=programs_statistic)
    if not program:
        logger.error(
            f"Program not exist program_id {programs_statistic}"
        )
        return None

    statistics_exercises_list = await statistic_db.get_list_exercises(
        program_id=program.id,
        offset=offset
    )
    if not statistics_exercises_list:
        return None

    return await get_text_program(
        program_title=program.title,
        date_start=statistics_program.start_time,
        date_finish=statistics_program.finish_time,
        statistics_exercises_list=statistics_exercises_list
    )


async def get_text_program(
    program_title: str,
    date_start: datetime,
    date_finish: datetime | None,
    statistics_exercises_list: StatisticsExercises
) -> str:
    title = f"<b>{program_title}</b> "\
            f"[{date_start.strftime('%Y-%m-%d')} - "\
            f"{date_finish.strftime('%Y-%m-%d') if date_finish else ''}]\n"
    current_date = ''
    lines = defaultdict(list)
    for exercises_stc in statistics_exercises_list:
        exercises = await program_db.get_exercises(
            exercises_id=exercises_stc.exercises_id
        )

        date = f"\n<b>{DAYS_WEEK.get(exercises.day)}</b> "\
               f"[{exercises_stc.created.astimezone().strftime('%m-%d')}]\n"

        if current_date != date:
            lines[date]
            current_date = date

        done = "✅" if exercises_stc.done else "❌"
        line = f"{exercises.title} [{done}]"\
               f" [🕔{exercises_stc.created.astimezone().strftime('%H:%M')}]\n"
        lines[date].append(line)

    text = [title]
    for day, exercises_list in lines.items():
        text.append(day)
        text.extend(
            [f"{id}. {exe}" for id, exe in enumerate(exercises_list[::-1], 1)]
        )
    return ''.join(text)
