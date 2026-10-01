import re
from pathlib import Path

from ebooklib import epub


class MetadataService:
    @staticmethod
    def _clean(value):
        if value is None:
            return ""
        return str(value).strip()

    @staticmethod
    def _humanize_title(value):
        cleaned = value.replace("_", " ")
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        if not cleaned:
            return "Untitled"
        return cleaned[:1].upper() + cleaned[1:]

    @staticmethod
    def extract_metadata(file_path):
        path = Path(file_path)
        metadata = {
            "title": "",
            "subtitle": "",
            "author": "",
            "publisher": "",
            "language": "",
            "isbn": "",
            "series": "",
            "series_index": "",
            "description": "",
            "cover_path": "",
        }

        suffix = path.suffix.lower()
        title_seed = path.stem

        if suffix == ".epub":
            try:
                book = epub.read_epub(str(path))
                metadata["title"] = MetadataService._clean(
                    book.get_metadata("DC", "title")[0][0] if book.get_metadata("DC", "title") else ""
                )
                metadata["author"] = MetadataService._clean(
                    ", ".join(
                        author[0]
                        for author in book.get_metadata("DC", "creator")
                    )
                    if book.get_metadata("DC", "creator")
                    else ""
                )
                metadata["publisher"] = MetadataService._clean(
                    book.get_metadata("DC", "publisher")[0][0] if book.get_metadata("DC", "publisher") else ""
                )
                metadata["language"] = MetadataService._clean(
                    book.get_metadata("DC", "language")[0][0] if book.get_metadata("DC", "language") else ""
                )
                metadata["isbn"] = MetadataService._clean(
                    book.get_metadata("DC", "identifier")[0][0] if book.get_metadata("DC", "identifier") else ""
                )
                metadata["description"] = MetadataService._clean(
                    book.get_metadata("DC", "description")[0][0] if book.get_metadata("DC", "description") else ""
                )
                for item in book.get_items():
                    if item.get_name().lower().endswith("cover"):
                        metadata["cover_path"] = item.get_name()
                        break
            except Exception:
                pass

        if not metadata["title"]:
            metadata["title"] = MetadataService._humanize_title(title_seed)

        if not metadata["author"] and len(path.stem.split("-")) > 1 and path.stem.lower().startswith("by "):
            metadata["author"] = path.stem.split("-", 1)[1]

        return metadata
