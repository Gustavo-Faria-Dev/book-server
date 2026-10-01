from html import escape
from pathlib import Path

from flask import Blueprint, Response, current_app, request

from app.models import Book

opds_bp = Blueprint("opds", __name__)


def _query_books():
    query = (request.args.get("q") or "").strip().lower()
    books = Book.query.order_by(Book.created_at.desc()).all()
    if not query:
        return books
    return [
        book
        for book in books
        if query in (book.title or "").lower()
        or query in (book.author or "").lower()
        or query in (book.series or "").lower()
        or query in (book.isbn or "").lower()
        or query in (book.publisher or "").lower()
        or query in (book.filename or "").lower()
    ]


def _mime_for_book(book):
    suffix = Path(book.filename).suffix.lower().lstrip(".")
    mapping = {
        "epub": "application/epub+zip",
        "pdf": "application/pdf",
        "mobi": "application/x-mobipocket-ebook",
        "azw3": "application/x-mobipocket-ebook",
        "cbz": "application/vnd.comicbook+zip",
        "txt": "text/plain",
    }
    return mapping.get(suffix, "application/octet-stream")


def _entry_xml(book):
    return f"""
    <entry>
      <title>{escape(book.title or book.filename)}</title>
      <author><name>{escape(book.author or 'Unknown')}</name></author>
      <updated>{book.updated_at.isoformat() if book.updated_at else '1970-01-01T00:00:00Z'}</updated>
      <id>urn:book:{book.id}</id>
      <link href="/opds/books/{book.id}" rel="alternate" type="application/atom+xml;type=entry;profile=opds-catalog"/>
      <link href="/books/{book.id}/download" rel="http://opds-spec.org/acquisition/open-access" type="{_mime_for_book(book)}"/>
      <content type="text">{escape(book.description or '')}</content>
    </entry>
    """.strip()


@opds_bp.route("/opds")
@opds_bp.route("/opds/search")
def opds_catalog():
    books = _query_books()
    entries = "\n".join(_entry_xml(book) for book in books)
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:opds="http://opds-spec.org/2010/catalog">
  <title>Reader Server</title>
  <id>urn:reader-server:library</id>
  <updated>{(books[0].updated_at if books else Book.query.order_by(Book.created_at.desc()).first()).isoformat() if books or Book.query.order_by(Book.created_at.desc()).first() else '1970-01-01T00:00:00Z'}</updated>
  <link href="{current_app.config.get('SERVER_NAME', '/opds')}" rel="self"/>
  {entries}
</feed>'''
    return Response(xml, mimetype="application/atom+xml")


@opds_bp.route("/opds/books/<int:book_id>")
def opds_book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<entry xmlns="http://www.w3.org/2005/Atom">
  <title>{escape(book.title or book.filename)}</title>
  <author><name>{escape(book.author or 'Unknown')}</name></author>
  <id>urn:book:{book.id}</id>
  <updated>{book.updated_at.isoformat() if book.updated_at else '1970-01-01T00:00:00Z'}</updated>
  <content type="text">{escape(book.description or '')}</content>
  <link href="/books/{book.id}/download" rel="http://opds-spec.org/acquisition/open-access" type="{_mime_for_book(book)}"/>
</entry>'''
    return Response(xml, mimetype="application/atom+xml")


@opds_bp.route("/opds/download/<int:book_id>")
def opds_download(book_id):
    book = Book.query.get_or_404(book_id)
    return Response("", status=302, headers={"Location": f"/books/{book.id}/download"})
