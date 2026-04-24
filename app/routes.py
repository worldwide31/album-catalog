from flask import Blueprint, render_template, request, redirect, url_for
from .services import get_all_albums, add_album, delete_album

albums_bp = Blueprint("albums", __name__)


@albums_bp.route("/")
def index():
    albums = get_all_albums()
    return render_template("index.html", albums=albums)


@albums_bp.route("/add", methods=["GET", "POST"])
def add():
    errors = []

    if request.method == "POST":
        title = request.form.get("title", "")
        artist = request.form.get("artist", "")
        year = request.form.get("year", "")
        rating = request.form.get("rating", "")

        errors = add_album(title, artist, year, rating)

        if not errors:
            return redirect(url_for("albums.index"))

    return render_template("form.html", errors=errors)


@albums_bp.route("/delete/<int:album_id>", methods=["POST"])
def delete(album_id):
    delete_album(album_id)
    return redirect(url_for("albums.index"))
