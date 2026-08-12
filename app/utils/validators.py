from pathlib import Path
from app.rag.document_loader import ALLOWED_EXTENSIONS
def is_allowed_upload(name: str, size: int, max_bytes: int) -> bool:
    return Path(name).suffix.lower() in ALLOWED_EXTENSIONS and 0 < size <= max_bytes

