import hashlib
from pathlib import Path
from app.rag.document_loader import load_document
from app.rag.document_processor import chunk_documents

def file_hash(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def ingest(path: Path, vector_store, repository=None, chunk_size=1000, chunk_overlap=150):
    digest = file_hash(path)
    if repository and repository.document_by_hash(digest): return False, "Duplicate document skipped."
    documents = load_document(path)
    if not documents or not any(doc.page_content.strip() for doc in documents): raise ValueError("Document contains no extractable text.")
    for doc in documents:
        doc.metadata.update({"filename": path.name, "file_hash": digest})
    chunks = chunk_documents(documents, chunk_size, chunk_overlap)
    vector_store.add(chunks)
    if repository: repository.add_document(filename=path.name, document_type=path.suffix.lower(), file_hash=digest, status="indexed")
    return True, f"Indexed {len(chunks)} chunks."

