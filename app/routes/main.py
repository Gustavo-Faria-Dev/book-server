from flask import Blueprint, jsonify, render_template, request

from app.models import Book

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@main_bp.route("/search")
def index():
    query = (request.args.get("q") or "").strip().lower()
    books = Book.query.order_by(Book.created_at.desc()).all()
    if query:
        books = [
            book
            for book in books
            if query in (book.title or "").lower()
            or query in (book.author or "").lower()
            or query in (book.series or "").lower()
            or query in (book.isbn or "").lower()
            or query in (book.publisher or "").lower()
            or query in (book.filename or "").lower()
        ]
    return render_template("index.html", books=books, query=query)


@main_bp.route("/health")
def health():
    return jsonify({"status": "ok"})


@main_bp.route("/settings")
def settings():
    return render_template("settings.html")
