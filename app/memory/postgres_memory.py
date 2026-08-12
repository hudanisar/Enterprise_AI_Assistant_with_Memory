from app.database.repositories import Repository
class PostgresMemory:
    def __init__(self, repository: Repository): self.repository = repository
    def save(self, user_id, memory_type, content): return self.repository.upsert_memory(user_id, memory_type, content)
    def search(self, user_id, query, limit=6):
        words = {w.lower() for w in query.split() if len(w) > 2}
        return sorted(self.repository.memories(user_id), key=lambda m: sum(w in m.content.lower() for w in words), reverse=True)[:limit]

