from app.memory.memory_extractor import extract_memories
from app.memory.postgres_memory import PostgresMemory
def test_extract_preference():
    assert extract_memories("Remember that I prefer Python examples.")[0][0] == "preference"
def test_sensitive_data_is_not_memory(): assert extract_memories("My API key is abc") == []
def test_deduplicate_memory(repo):
    user = repo.get_or_create_user("alice"); store = PostgresMemory(repo)
    store.save(user.id, "preference", "User prefers Python."); store.save(user.id, "preference", "User prefers Python.")
    assert len(repo.memories(user.id)) == 1

