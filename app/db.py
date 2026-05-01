from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

metadata = MetaData()

albums_table = Table(
    "albums",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("artist", String(255), nullable=False),
    Column("year", Integer, nullable=False),
    Column("rating", Integer, nullable=False),
)


def create_db_engine(app):
    database_url = app.config["DATABASE_URL"]

    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    return create_engine(
        database_url,
        future=True,
        pool_pre_ping=True,
        connect_args=connect_args,
    )


def get_engine():
    from flask import current_app

    return current_app.extensions["db_engine"]


def init_db(app):
    engine = create_db_engine(app)
    app.extensions["db_engine"] = engine

    with engine.begin() as connection:
        metadata.create_all(connection)
