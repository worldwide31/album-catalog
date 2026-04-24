from .db import get_db


def get_all_albums():
    db = get_db()
    return db.execute(
        "SELECT id, title, artist, year, rating FROM albums ORDER BY id DESC"
    ).fetchall()


def add_album(title, artist, year, rating):
    errors = validate_album(title, artist, year, rating)

    if errors:
        return errors

    db = get_db()
    db.execute(
        "INSERT INTO albums (title, artist, year, rating) VALUES (?, ?, ?, ?)",
        (title.strip(), artist.strip(), int(year), int(rating)),
    )
    db.commit()

    return []


def delete_album(album_id):
    db = get_db()
    db.execute("DELETE FROM albums WHERE id = ?", (album_id,))
    db.commit()


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
