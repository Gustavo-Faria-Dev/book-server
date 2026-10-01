from pathlib import Path, PurePosixPath

from flask import Blueprint, abort, current_app, jsonify, render_template, request, send_file
from werkzeug.utils import secure_filename

from app.models import Book, db
from app.services.library import LibraryScanner

books_bp = Blueprint("books", __name__)

ALLOWED_EXTENSIONS = {"epub", "pdf", "mobi", "azw3", "cbz", "txt"}


def _resolve_book_file(book):
    if not book or not book.filepath:
        abort(404)
    path = Path(book.filepath).resolve()
    root = Path(current_app.config["BOOKS_DIR"]).resolve()
    if root not in path.parents and path != root:
        abort(404)
    return path


@books_bp.route("/api/books", methods=["GET"]) 
def api_books_list():
    books = Book.query.order_by(Book.created_at.desc()).all()
    return jsonify([book.to_dict() for book in books])


@books_bp.route("/api/books", methods=["POST"]) 
def api_books_create():
    uploaded_file = request.files.get("file")
    if uploaded_file is None or not uploaded_file.filename:
        return jsonify({"error": "A file is required."}), 400

    filename = secure_filename(uploaded_file.filename)
    if not filename:
        return jsonify({"error": "Invalid file name."}), 400

    extension = Path(filename).suffix.lower().lstrip(".")
    if extension not in current_app.config["SUPPORTED_EXTENSIONS"]:
        return jsonify({"error": "Unsupported file format."}), 400

    storage_dir = Path(current_app.config["BOOKS_DIR"]).resolve()
    storage_dir.mkdir(parents=True, exist_ok=True)
    destination = storage_dir / filename
    uploaded_file.save(destination)

    LibraryScanner(current_app).scan()
    saved_book = Book.query.filter_by(filepath=str(destination.resolve())).first()
    if saved_book is None:
        return jsonify({"error": "The file could not be imported."}), 500
    return jsonify(saved_book.to_dict()), 201


@books_bp.route("/api/books/<int:book_id>", methods=["GET", "PUT", "DELETE"]) 
def api_book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == "GET":
        return jsonify(book.to_dict())

    if request.method == "PUT":
        payload = request.get_json(silent=True) or request.form or {}
        for field in [
            "title",
            "subtitle",
            "author",
            "series",
            "series_index",
            "publisher",
            "language",
            "isbn",
            "description",
        ]:
            value = payload.get(field)
            if value is not None:
                setattr(book, field, value)
        db.session.commit()
        return jsonify(book.to_dict())

    delete_file = request.args.get("delete_file", "false").lower() == "true"
    if delete_file:
        target = Path(book.filepath)
        if target.exists():
            target.unlink()
    db.session.delete(book)
    db.session.commit()
    return jsonify({"status": "deleted", "id": book_id})


@books_bp.route("/books/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("book.html", book=book)


@books_bp.route("/books/<int:book_id>/download")
def book_download(book_id):
    book = Book.query.get_or_404(book_id)
    file_path = _resolve_book_file(book)
    return send_file(file_path, as_attachment=True, download_name=book.filename)


@books_bp.route("/books/<path:book_path>/download")
def book_download_path(book_path):
    if book_path.isdigit():
        return book_download(int(book_path))

    if ".." in PurePosixPath(book_path).parts:
        abort(404)

    storage_dir = Path(current_app.config["BOOKS_DIR"]).resolve()
    file_path = (storage_dir / book_path).resolve()
    if not file_path.exists() or not file_path.is_file():
        abort(404)
    if storage_dir not in file_path.parents and file_path != storage_dir:
        abort(404)
    return send_file(file_path, as_attachment=True, download_name=file_path.name)
