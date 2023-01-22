from sqlalchemy import (
    Table, Column, Integer, String, DateTime, ForeignKey, MetaData
)
from sqlalchemy.sql import func


metadata = MetaData()


category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False)
)


program = Table(
    "programs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("created", DateTime(timezone=True), server_default=func.now()),
    Column("category_id", Integer, ForeignKey("category.id"), nullable=False),
)

exercises = Table(
    "exercises",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("number_approaches", Integer),
    Column("number_repetitions", String),
    Column("day", String),
    Column("image", String),
)


program_exercises = Table(
    'program_exercises',
    metadata,
    Column("program_id", ForeignKey("programs.id")),
    Column("exercises_id", ForeignKey("exercises.id")),
)
