from dataclasses import dataclass
from datetime import datetime


@dataclass
class StatisticsProgram:
    id: int
    user_id: int
    program_id: int
    start_time: datetime
    finish_time: datetime | None


@dataclass
class StatisticsExercises:
    id: int
    user_id: int
    statistics_program_id: int
    exercises_id: int
    done: bool
    created: datetime
