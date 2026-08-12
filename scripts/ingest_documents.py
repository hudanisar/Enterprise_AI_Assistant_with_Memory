import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.config import get_settings
from app.database.connection import make_session_factory
from app.database.repositories import Repository
from app.rag.document_loader import ALLOWED_EXTENSIONS
from app.rag.ingestion import ingest
from app.rag.vector_store import VectorStore
s = get_settings(); repo = Repository(make_session_factory()()); vector = VectorStore(s.vector_store_path)
for path in s.documents_path.glob("*"):
    if path.suffix.lower() in ALLOWED_EXTENSIONS:
        try: print(path.name, ingest(path, vector, repo, s.chunk_size, s.chunk_overlap)[1])
        except Exception as exc: print(path.name, "FAILED", type(exc).__name__)
