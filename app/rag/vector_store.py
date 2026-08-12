import json
import re
from pathlib import Path
from langchain_core.documents import Document
from langchain_chroma import Chroma
from app.config import get_settings
from app.rag.embeddings import make_embeddings


class KeywordStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self.file = self.path / "keyword_store.json"
        self.documents = self._load()

    def _load(self):
        if not self.file.exists():
            return []
        return json.loads(self.file.read_text(encoding="utf-8"))

    def _save(self):
        self.file.write_text(json.dumps(self.documents, indent=2), encoding="utf-8")

    def add_documents(self, chunks):
        for chunk in chunks:
            self.documents.append({"page_content": chunk.page_content, "metadata": dict(chunk.metadata)})
        self._save()

    def search(self, query, k=4):
        query_terms = set(re.findall(r"[a-z0-9]+", query.lower()))
        if not query_terms:
            return []
        scored = []
        for item in self.documents:
            text_terms = set(re.findall(r"[a-z0-9]+", item["page_content"].lower()))
            score = len(query_terms & text_terms) / max(len(query_terms), 1)
            if score:
                scored.append((Document(page_content=item["page_content"], metadata=item["metadata"]), score))
        return sorted(scored, key=lambda row: row[1], reverse=True)[:k]

    def health_check(self):
        return True


class VectorStore:
    def __init__(self, path: str | Path, embeddings=None):
        self.path = str(path)
        self.keyword_store = KeywordStore(path)
        settings = get_settings()
        self.store = self.keyword_store
        if embeddings or settings.google_api_key:
            try:
                self.store = Chroma(persist_directory=self.path, embedding_function=embeddings or make_embeddings())
            except Exception:
                self.store = self.keyword_store
    def add(self, chunks):
        self.keyword_store.add_documents(chunks)
        if self.store is not self.keyword_store:
            try:
                self.store.add_documents(chunks)
            except Exception:
                self.store = self.keyword_store
    def search(self, query, k=4):
        if self.store is self.keyword_store:
            return self.keyword_store.search(query, k)
        try:
            return self.store.similarity_search_with_relevance_scores(query, k=k)
        except Exception:
            self.store = self.keyword_store
            return self.keyword_store.search(query, k)
    def health_check(self):
        try:
            if self.store is self.keyword_store:
                return self.keyword_store.health_check()
            self.store.get(limit=1); return True
        except Exception: return False
