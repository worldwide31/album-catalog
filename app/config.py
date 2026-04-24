import os
from pathlib import Path

from dotenv import load_dotenv
from dynaconf import Dynaconf

BASE_DIR = Path(__file__).resolve().parent.parent

# .env нужен только для локальной разработки.
# В Docker/staging/prod значения должны приходить из переменных окружения.
load_dotenv(BASE_DIR / ".env")

CONFIG_FILE = os.getenv("CONFIG_FILE", "config.yaml")

settings = Dynaconf(
    settings_files=[str(BASE_DIR / CONFIG_FILE)],
    environments=False,
)


def get_setting(name, default=None, cast=str):
    """
    Порядок приоритета:
    1. Переменная окружения
    2. Значение из config.yaml
    3. Значение по умолчанию
    """
    value = os.getenv(name)

    if value is None:
        value = settings.get(name, default)

    if cast is bool:
        if isinstance(value, bool):
            return value
        return str(value).lower() in ("1", "true", "yes", "on")

    if cast is int:
        return int(value)

    return value


def resolve_database_path(database_url):
    """
    Поддержка SQLite-строк:
    sqlite:///albums.db      -> файл внутри проекта
    sqlite:////data/app.db   -> абсолютный путь внутри контейнера/сервера
    """
    if not database_url.startswith("sqlite:///"):
        return database_url

    raw_path = database_url.replace("sqlite:///", "", 1)
    path = Path(raw_path)

    if path.is_absolute():
        return path

    return BASE_DIR / path


class Config:
    APP_NAME = get_setting("APP_NAME", "Каталог альбомов")
    HOST = get_setting("HOST", "0.0.0.0")
    PORT = get_setting("PORT", 5000, int)
    FLASK_ENV = get_setting("FLASK_ENV", "production")
    DEBUG = FLASK_ENV == "development"

    SECRET_KEY = get_setting("SECRET_KEY", "change-me-only-for-local-dev")
    DATABASE_URL = get_setting("DATABASE_URL", "sqlite:///albums.db")
    DB_PATH = resolve_database_path(DATABASE_URL)
