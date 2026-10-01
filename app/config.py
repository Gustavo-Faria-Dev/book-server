import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def resolve_path(value):
    path = Path(value)
    return path if path.is_absolute() else BASE_DIR / path


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8080"))
    BOOKS_DIR = resolve_path(os.getenv("BOOKS_DIR", "books"))
    COVERS_DIR = resolve_path(os.getenv("COVERS_DIR", "covers"))
    DATA_DIR = resolve_path("data")
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'library.db'}")
    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "500"))
    SUPPORTED_EXTENSIONS = {"epub", "pdf", "mobi", "azw3", "cbz", "txt"}
