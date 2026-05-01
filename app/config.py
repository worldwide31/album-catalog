import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from dynaconf import Dynaconf

BASE_DIR = Path(__file__).resolve().parent.parent

# .env и config.yaml нужны только для локальной разработки.
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


def build_sqlite_url():
    sqlite_db_path = get_setting("SQLITE_DB_PATH", "albums.db")
    path = Path(sqlite_db_path)

    if not path.is_absolute():
        path = BASE_DIR / path

    return f"sqlite:///{path.as_posix()}"


def build_postgres_url():
    user = quote_plus(get_setting("DB_USER", "albums_user"))
    password = quote_plus(get_setting("DB_PASSWORD", "albums_password"))
    host = get_setting("DB_HOST", "db")
    port = get_setting("DB_PORT", 5432, int)
    name = get_setting("DB_NAME", "albums_db")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


def build_database_url():
    database_url = get_setting("DATABASE_URL", None)

    if database_url:
        if database_url.startswith("sqlite:///") and not database_url.startswith("sqlite:////"):
            raw_path = database_url.replace("sqlite:///", "", 1)
            path = Path(raw_path)
            if not path.is_absolute():
                path = BASE_DIR / path
            return f"sqlite:///{path.as_posix()}"
        return database_url

    db_engine = get_setting("DB_ENGINE", "sqlite").lower()

    if db_engine == "postgresql":
        return build_postgres_url()

    return build_sqlite_url()


class Config:
    APP_NAME = get_setting("APP_NAME", "Каталог альбомов")
    HOST = get_setting("HOST", "0.0.0.0")
    PORT = get_setting("PORT", 5000, int)
    FLASK_ENV = get_setting("FLASK_ENV", "production")
    DEBUG = FLASK_ENV == "development"

    SECRET_KEY = get_setting("SECRET_KEY", "change-me-only-for-local-dev")

    DB_ENGINE = get_setting("DB_ENGINE", "sqlite")
    DATABASE_URL = build_database_url()
