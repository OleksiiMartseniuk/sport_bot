import csv
import logging

from . import db


logger = logging.getLogger(__name__)


async def process_import(file_path: str):
    """
    | Column's name              | Required |
    |----------------------------+----------|
    | category_title             | Y        |
    | program_title              | Y        |
    | exercise_tile              | Y        |
    | exercise_number_approaches | Y        |
    | exercise_number_repetitions| Y        |
    | exercise_day               | Y        |
    | exercise_image             | Y        |
    """

    file = open(file_path, "r")
    reader = csv.DictReader(file.read().split("\n"))
    for index, row in enumerate(reader):
        row_data = {key.lower(): data.strip() for key, data in row.items()}

        required_fields = [
            row_data.get("category_title"),
            row_data.get("program_title"),
            row_data.get("exercise_tile"),
            row_data.get("exercise_number_approaches"),
            row_data.get("exercise_number_repetitions"),
            row_data.get("exercise_day"),
            row_data.get("exercise_image"),
        ]

        if not all(required_fields):
            logger.error(f"Item index {index} missing required fields")

        category = await db.get_category(title=row_data["category_title"])
        if category:
            category_id = category.id
        else:
            category_id = await db.insert_category(
                title=row_data["category_title"]
            )

        program = await db.get_program(title=row_data["program_title"])
        if program:
            program_id = program.id
        else:
            program_id = await db.insert_program(
                title=row_data["program_title"],
                category_id=category_id
            )

        exercise_id = await db.insert_exercise(
            title=row_data["exercise_tile"],
            number_approaches=int(row_data["exercise_number_approaches"]),
            number_repetitions=row_data["exercise_number_repetitions"],
            day=int(row_data["exercise_day"]),
            image=row_data["exercise_image"]
        )

        await db.insert_program_exercise(
            program_id=program_id,
            exercises_id=exercise_id
        )

    logger.info("Data fro file write to database")
    file.close()
