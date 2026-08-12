from app.memory.memory_extractor import extract_memories
class MemoryManager:
    def __init__(self, store): self.store = store
    def process_message(self, user_id, text):
        return [self.store.save(user_id, kind, content) for kind, content in extract_memories(text)]
    def retrieve(self, user_id, query): return self.store.search(user_id, query)

