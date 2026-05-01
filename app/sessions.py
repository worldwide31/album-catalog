from flask_session import Session
from redis import Redis


def init_sessions(app):
    """
    Для Docker Compose используется Redis.
    Это убирает зависимость от памяти конкретного процесса и от sticky sessions.
    """
    app.config["SESSION_TYPE"] = app.config.get("SESSION_TYPE", "filesystem")
    app.config["SESSION_PERMANENT"] = False

    if app.config["SESSION_TYPE"] == "redis":
        app.config["SESSION_REDIS"] = Redis.from_url(app.config["SESSION_REDIS_URL"])

    Session(app)
