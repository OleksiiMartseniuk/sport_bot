from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str | None
    telegram_id: int
    is_admin: bool
    is_active: bool
    created: datetime
