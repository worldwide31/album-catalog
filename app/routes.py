import socket

from flask import Blueprint, current_app, jsonify, redirect, render_template, request, session, url_for

from .services import add_album, count_albums, delete_album, get_all_albums

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


@albums_bp.route("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "app_name": current_app.config["APP_NAME"],
            "version": current_app.config["APP_VERSION"],
            "environment": current_app.config["RELEASE_ENVIRONMENT"],
            "database": current_app.config["DB_ENGINE"],
            "sessions": current_app.config["SESSION_TYPE"],
            "instance": socket.gethostname(),
            "albums_count": count_albums(),
        }
    )


@albums_bp.route("/session-demo")
def session_demo():
    session["views"] = session.get("views", 0) + 1

    return jsonify(
        {
            "message": "Счётчик хранится в централизованной сессии.",
            "session_views": session["views"],
            "session_storage": current_app.config["SESSION_TYPE"],
            "instance": socket.gethostname(),
        }
    )
