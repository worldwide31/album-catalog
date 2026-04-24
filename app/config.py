import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    BASE_DIR = Path(__file__).resolve().parent.parent
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///albums.db")

    if DATABASE_URL.startswith("sqlite:///"):
        DB_PATH = BASE_DIR / DATABASE_URL.replace("sqlite:///", "")
    else:
        DB_PATH = DATABASE_URL
