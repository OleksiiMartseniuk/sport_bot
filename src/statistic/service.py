import logging

from prettytable import PrettyTable
from datetime import datetime

from user import db as user_db
from programs import db as program_db

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


async def get_current_statistic(
        telegram_user_id: int,
        program_id: int
) -> str | None:
    user = await user_db.get_user(telegram_id=telegram_user_id)
    if not user:
        return

    statistics_program = await statistic_db.check_active_statistics_program(
        user_id=user.id,
        program_id=program_id
    )

    if not statistics_program:
        logger.info(f"Not exist active program in user {user.id}")
        return "<b>У вас не существует активной программы!!!</b>"

    program = await program_db.get_program(id=program_id)
    if not program:
        logger.error(f"Program not exist program_id {program_id}")
        return None

    statistics_exercises_list = await statistic_db.get_list_exercises(
        program_id=program.id
    )

    table = PrettyTable()
    table.field_names = ["Упражнения", "Выполнения", "Дата"]
    for exercises_stc in statistics_exercises_list:
        exercises = await program_db.get_exercises(
            exercises_id=exercises_stc.exercises_id
        )
        if not exercises:
            logger.error(f"Not exist program {exercises_stc.exercises_id}")
            continue

        table.add_row([
            exercises.title,
            "✅" if exercises_stc.done else "❌",
            exercises_stc.created.strftime("%Y-%m-%d %H:%M")
        ])

    return f"<b>{program.title}</b> "\
           f"{statistics_program.start_time.strftime('%Y-%m-%d %H:%M')}\n"\
           f" <pre>{table}</pre>"
