from sqlalchemy import (
    MetaData, Table, Column, ForeignKey, Integer, DateTime, Boolean
)
from programs.models import program, exercises
from user.models import user


metadata = MetaData()


statistics_program = Table(
    "statistics_program",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(user.c.id), nullable=False),
    Column("program_id", Integer, ForeignKey(program.c.id), nullable=False),
    Column("start_time", DateTime(timezone=True)),
    Column("finish_time", DateTime(timezone=True))
)

statistics_exercises = Table(
    "statistics_exercises",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(user.c.id)),
    Column(
        "statistics_program_id",
        Integer,
        ForeignKey("statistics_program.id"),
        nullable=False
    ),
    Column(
        "exercises_id",
        Integer,
        ForeignKey(exercises.c.id),
        nullable=False
    ),
    Column("created", DateTime(timezone=True))
)


statistics_approaches = Table(
    "statistics_approaches",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "statistics_exercise_id",
        Integer,
        ForeignKey("statistics_exercises.id")
    ),
    Column("approaches", Integer),
    Column("done", Boolean),
    Column("created", DateTime(timezone=True))
)
