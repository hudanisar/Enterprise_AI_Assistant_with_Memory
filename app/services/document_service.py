from pathlib import Path
from app.rag.document_loader import ALLOWED_EXTENSIONS
from app.rag.ingestion import ingest
def save_and_ingest(upload, documents_dir: Path, vector_store, repository, settings):
    name = Path(upload.name).name
    if Path(name).suffix.lower() not in ALLOWED_EXTENSIONS: raise ValueError("Unsupported file type.")
    if len(upload.getvalue()) > settings.max_upload_mb * 1024 * 1024: raise ValueError("File exceeds upload size limit.")
    target = documents_dir / name; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(upload.getvalue())
    return ingest(target, vector_store, repository, settings.chunk_size, settings.chunk_overlap)

