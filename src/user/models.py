from sqlalchemy import (
    MetaData, Table, Column, Integer, String, DateTime, Boolean
)
from sqlalchemy.sql import func


metadata = MetaData()


user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("telegram_id", Integer, nullable=False),
    Column("is_admin", Boolean, nullable=False),
    Column("is_active", Boolean, nullable=False),
    Column("created", DateTime(timezone=True), server_default=func.now()),
)
