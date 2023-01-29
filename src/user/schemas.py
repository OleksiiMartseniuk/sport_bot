from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str | None
    is_admin: bool
    is_active: bool
    created: datetime
