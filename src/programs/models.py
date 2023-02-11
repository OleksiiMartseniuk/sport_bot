from sqlalchemy import (
    Table, Column, Integer, String, DateTime, ForeignKey, MetaData, Boolean
)
from sqlalchemy.sql import func

from user.models import user


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
    Column("day", Integer),
    Column("image", String),
    Column("telegram_image_id", String)
)


program_exercises = Table(
    'program_exercises',
    metadata,
    Column("program_id", ForeignKey("programs.id")),
    Column("exercises_id", ForeignKey("exercises.id")),
)


file = Table(
    "files",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(user.c.id), nullable=False),
    Column("file_name", String),
    Column("done", Boolean),
)
