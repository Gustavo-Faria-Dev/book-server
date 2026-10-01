from pathlib import Path

from flask import current_app
from ebooklib import epub


class CoverService:
    @staticmethod
    def extract_cover(file_path, output_name=None):
        path = Path(file_path)
        if path.suffix.lower() != ".epub":
            return ""

        try:
            book = epub.read_epub(str(path))
            for item in book.get_items():
                if item.get_type() == epub.ITEM_IMAGE:
                    cover_bytes = item.get_content()
                    target_name = output_name or f"{path.stem}.jpg"
                    target_dir = Path(current_app.config["COVERS_DIR"]).resolve()
                    target_dir.mkdir(parents=True, exist_ok=True)
                    target_path = target_dir / target_name
                    target_path.write_bytes(cover_bytes)
                    return target_name
        except Exception:
            return ""

        return ""
