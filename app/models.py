from datetime import datetime, timezone

from . import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(1024), nullable=False, unique=True)
    title = db.Column(db.String(500), nullable=False, default="Untitled")
    subtitle = db.Column(db.String(500), default="")
    author = db.Column(db.String(500), default="")
    publisher = db.Column(db.String(500), default="")
    language = db.Column(db.String(100), default="")
    isbn = db.Column(db.String(100), default="")
    series = db.Column(db.String(500), default="")
    series_index = db.Column(db.String(50), default="")
    description = db.Column(db.Text, default="")
    cover_path = db.Column(db.String(1024), default="")
    file_size = db.Column(db.Integer, default=0)
    file_hash = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @property
    def format(self):
        return self.filename.rsplit(".", 1)[-1].upper() if "." in self.filename else "FILE"

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "filepath": self.filepath,
            "title": self.title,
            "subtitle": self.subtitle,
            "author": self.author,
            "publisher": self.publisher,
            "language": self.language,
            "isbn": self.isbn,
            "series": self.series,
            "series_index": self.series_index,
            "description": self.description,
            "cover_url": f"/covers/{self.cover_path}" if self.cover_path else None,
            "file_size": self.file_size,
            "format": self.format,
            "download_url": f"/books/{self.id}/download",
        }
