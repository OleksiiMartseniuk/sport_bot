import logging

from datetime import datetime

from user import db as user_db

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
