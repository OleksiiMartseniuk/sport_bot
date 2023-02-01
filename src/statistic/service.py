import logging

from datetime import datetime

from . import db


logger = logging.getLogger(__name__)


async def set_statistics_program(
    user_id: int,
    program_id: int,
    start_time: datetime = datetime.now()
) -> None:
    statistics_program = await db.get_active_statistics_program(
        user_id=user_id
    )
    if statistics_program:
        if statistics_program.program_id == program_id:
            logger.warning(
                "User %s trying to change the program to the current one",
                user_id
            )
            return
        else:
            await db.end_statistics_program(
                statistics_program_id=statistics_program.id
            )
            await db.start_statistics_program(
                user_id=user_id,
                program_id=program_id,
                start_time=start_time
            )
    else:
        await db.start_statistics_program(
            user_id=user_id,
            program_id=program_id,
            start_time=start_time
        )
    logger.info(
        "User %s installed program %s",
        user_id,
        program_id
    )
