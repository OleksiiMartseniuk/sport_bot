from dataclasses import dataclass
from datetime import datetime


@dataclass
class Category:
    id: int
    title: str


@dataclass
class Program:
    id: int
    title: str
    created: datetime
    category_id: int


@dataclass
class Exercises:
    id: int
    title: str
    number_approaches: int
    number_repetitions: str
    day: int
    image: str
    telegram_image_id: str


DAYS_WEEK = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье"
}
