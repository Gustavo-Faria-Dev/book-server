import hashlib
from datetime import datetime, timezone
from pathlib import Path

from flask import current_app

from app.models import Book, db

from .covers import CoverService
from .metadata import MetadataService


class LibraryScanner:
    def __init__(self, app=None):
        self.app = app

    def _book_root(self):
        return Path(current_app.config["BOOKS_DIR"]).resolve()

    @staticmethod
    def _hash_file(file_path):
        digest = hashlib.sha256()
        with open(file_path, "rb") as handle:
            for chunk in iter(lambda: handle.read(8192), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _safe_import(self, file_path):
        file_path = Path(file_path).resolve()
        file_hash = self._hash_file(file_path)
        existing = Book.query.filter_by(file_hash=file_hash).first()
        if existing:
            existing.filepath = str(file_path)
            existing.filename = file_path.name
            existing.updated_at = datetime.now(timezone.utc)
            db.session.add(existing)
            db.session.commit()
            return existing

        metadata = MetadataService.extract_metadata(str(file_path))
        cover_path = CoverService.extract_cover(str(file_path), output_name=f"{file_hash[:12]}.jpg")

        book = Book(
            filename=file_path.name,
            filepath=str(file_path),
            title=metadata["title"],
            subtitle=metadata["subtitle"],
            author=metadata["author"],
            publisher=metadata["publisher"],
            language=metadata["language"],
            isbn=metadata["isbn"],
            series=metadata["series"],
            series_index=metadata["series_index"],
            description=metadata["description"],
            cover_path=cover_path,
            file_size=file_path.stat().st_size,
            file_hash=file_hash,
        )
        db.session.add(book)
        db.session.commit()
        return book

    def scan(self):
        root = self._book_root()
        root.mkdir(parents=True, exist_ok=True)

        supported = current_app.config["SUPPORTED_EXTENSIONS"]
        imported = 0
        seen_files = set()

        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower().lstrip(".") not in supported:
                continue
            seen_files.add(str(file_path.resolve()))
            existing = Book.query.filter_by(filepath=str(file_path.resolve())).first()
            if existing:
                continue
            self._safe_import(file_path)
            imported += 1

        for book in Book.query.all():
            if book.filepath and not Path(book.filepath).exists():
                db.session.delete(book)

        db.session.commit()
        return imported
