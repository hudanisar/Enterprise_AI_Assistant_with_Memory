class Retriever:
    def __init__(self, vector_store, top_k=4, threshold=.2): self.vector_store, self.top_k, self.threshold = vector_store, top_k, threshold
    def retrieve(self, query): return [(doc, score) for doc, score in self.vector_store.search(query, self.top_k) if score >= self.threshold]

