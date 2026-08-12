from app.rag.document_processor import chunk_documents
from langchain_core.documents import Document
def test_chunks_have_metadata():
    chunks = chunk_documents([Document(page_content="word " * 500, metadata={"filename":"x.md"})], 100, 20)
    assert len(chunks) > 1 and "chunk_index" in chunks[0].metadata

