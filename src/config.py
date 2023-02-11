import os

from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR.joinpath("media")
DOCUMENTS_ROOT = BASE_DIR.joinpath("documents")

# Postgres
POSTGRES_DB = os.getenv("POSTGRES_DB", "sport_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "token")
MENU_IMAGE_FILE_ID = os.getenv("MENU_IMAGE_FILE_ID", "image")
