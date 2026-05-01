from sqlalchemy import delete, func, insert, select

from .db import albums_table, get_engine


def get_all_albums():
    engine = get_engine()

    with engine.connect() as connection:
        rows = connection.execute(
            select(albums_table).order_by(albums_table.c.id.desc())
        ).mappings().all()

    return [dict(row) for row in rows]


def count_albums():
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(select(func.count()).select_from(albums_table))
        return result.scalar_one()


def add_album(title, artist, year, rating):
    errors = validate_album(title, artist, year, rating)

    if errors:
        return errors

    engine = get_engine()

    with engine.begin() as connection:
        connection.execute(
            insert(albums_table).values(
                title=title.strip(),
                artist=artist.strip(),
                year=int(year),
                rating=int(rating),
            )
        )

    return []


def delete_album(album_id):
    engine = get_engine()

    with engine.begin() as connection:
        connection.execute(delete(albums_table).where(albums_table.c.id == album_id))


def validate_album(title, artist, year, rating):
    errors = []

    if not title or not title.strip():
        errors.append("Название альбома обязательно.")

    if not artist or not artist.strip():
        errors.append("Исполнитель обязателен.")

    try:
        year = int(year)
        if year < 1900 or year > 2100:
            errors.append("Год должен быть от 1900 до 2100.")
    except ValueError:
        errors.append("Год должен быть числом.")

    try:
        rating = int(rating)
        if rating < 1 or rating > 10:
            errors.append("Оценка должна быть от 1 до 10.")
    except ValueError:
        errors.append("Оценка должна быть числом.")

    return errors
