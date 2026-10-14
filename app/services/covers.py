from pathlib import Path

import ebooklib
from flask import current_app
from ebooklib import epub


class CoverService:
    @staticmethod
    def _cover_score(item, cover_ids):
        name = item.get_name().lower()
        stem = Path(name).stem
        item_id = (item.get_id() or "").lower()

        if item_id in cover_ids:
            return 0
        if item_id in {"cover", "cover-image", "frontcover"}:
            return 1
        if stem in {"cover", "cover-image", "frontcover"}:
            return 2
        if "cover" in stem:
            return 3
        if stem in {"frontpage", "titlepage"}:
            return 4
        return 10

    @staticmethod
    def extract_cover(file_path, output_name=None):
        path = Path(file_path)
        if path.suffix.lower() != ".epub":
            return ""

        try:
            book = epub.read_epub(str(path))
            cover_ids = {
                value
                for value, _ in book.get_metadata("OPF", "cover")
                if value
            }
            images = [
                item
                for item in book.get_items()
                if item.get_type() in {ebooklib.ITEM_IMAGE, ebooklib.ITEM_COVER}
            ]
            images.sort(key=lambda item: CoverService._cover_score(item, cover_ids))
            if images:
                cover_bytes = images[0].get_content()
                target_name = output_name or f"{path.stem}.jpg"
                target_dir = Path(current_app.config["COVERS_DIR"]).resolve()
                target_dir.mkdir(parents=True, exist_ok=True)
                target_path = target_dir / target_name
                target_path.write_bytes(cover_bytes)
                return target_name
        except Exception:
            return ""

        return ""
