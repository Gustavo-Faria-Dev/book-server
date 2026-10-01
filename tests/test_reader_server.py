from pathlib import Path

from app import create_app
from app.models import Book


def create_test_app(tmp_path, monkeypatch):
    books_dir = tmp_path / "books"
    covers_dir = tmp_path / "covers"
    data_dir = tmp_path / "data"
    books_dir.mkdir()
    covers_dir.mkdir()
    data_dir.mkdir()

    config = {
        "TESTING": True,
        "HOST": "127.0.0.1",
        "PORT": 5001,
        "BOOKS_DIR": str(books_dir),
        "COVERS_DIR": str(covers_dir),
        "DATA_DIR": str(data_dir),
        "DATABASE_URL": f"sqlite:///{data_dir / 'test_library.db'}",
        "MAX_UPLOAD_MB": 10,
    }
    app = create_app(config)
    app.config.update(config)
    return app


def test_create_app_and_db(tmp_path, monkeypatch):
    app = create_test_app(tmp_path, monkeypatch)
    with app.app_context():
        assert Book.query.count() == 0
        assert app.config["TESTING"] is True


def test_library_scan_imports_book(tmp_path, monkeypatch):
    app = create_test_app(tmp_path, monkeypatch)
    book_path = Path(app.config["BOOKS_DIR"]) / "example.txt"
    book_path.write_text("hello world", encoding="utf-8")

    with app.app_context():
        from app.services.library import LibraryScanner

        scanner = LibraryScanner(app)
        imported = scanner.scan()
        assert imported >= 1
        assert Book.query.filter_by(filename="example.txt").count() == 1


def test_search_and_download_endpoints(tmp_path, monkeypatch):
    app = create_test_app(tmp_path, monkeypatch)
    book_path = Path(app.config["BOOKS_DIR"]) / "hamlet.txt"
    book_path.write_text("Hamlet by Shakespeare", encoding="utf-8")

    with app.app_context():
        from app.services.library import LibraryScanner

        LibraryScanner(app).scan()

    client = app.test_client()
    response = client.get("/search?q=hamlet")
    assert response.status_code == 200
    assert b"Hamlet" in response.data

    with app.app_context():
        book = Book.query.filter_by(filename="hamlet.txt").first()
    download = client.get(f"/books/{book.id}/download")
    assert download.status_code == 200
    assert download.data == b"Hamlet by Shakespeare"


def test_opds_catalog(tmp_path, monkeypatch):
    app = create_test_app(tmp_path, monkeypatch)
    book_path = Path(app.config["BOOKS_DIR"]) / "dune.txt"
    book_path.write_text("Dune", encoding="utf-8")

    with app.app_context():
        from app.services.library import LibraryScanner

        LibraryScanner(app).scan()

    client = app.test_client()
    response = client.get("/opds")
    assert response.status_code == 200
    assert response.mimetype == "application/atom+xml"
    assert b"Dune" in response.data


def test_path_traversal_protection(tmp_path, monkeypatch):
    app = create_test_app(tmp_path, monkeypatch)
    client = app.test_client()
    response = client.get("/books/../../etc/passwd/download")
    assert response.status_code == 404


def test_delete_book_removes_record(tmp_path, monkeypatch):
    app = create_test_app(tmp_path, monkeypatch)
    book_path = Path(app.config["BOOKS_DIR"]) / "remove-me.txt"
    book_path.write_text("remove me", encoding="utf-8")

    with app.app_context():
        from app.services.library import LibraryScanner

        LibraryScanner(app).scan()
        book = Book.query.filter_by(filename="remove-me.txt").first()

    client = app.test_client()
    response = client.delete(f"/api/books/{book.id}")
    assert response.status_code == 200
    with app.app_context():
        assert Book.query.filter_by(id=book.id).count() == 0


def test_metadata_service_extracts_title_from_filename(tmp_path, monkeypatch):
    app = create_test_app(tmp_path, monkeypatch)
    book_path = Path(app.config["BOOKS_DIR"]) / "metadata-book.txt"
    book_path.write_text("metadata", encoding="utf-8")

    from app.services.metadata import MetadataService

    metadata = MetadataService.extract_metadata(str(book_path))
    assert metadata["title"] == "Metadata-book"
