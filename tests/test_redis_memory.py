from app.memory.redis_memory import RedisMemory
class FakeRedis:
    def __init__(self): self.data = {}
    def ping(self): return True
    def rpush(self, key, value): self.data.setdefault(key, []).append(value)
    def ltrim(self, key, start, end): self.data[key] = self.data.get(key, [])[start:end + 1 if end != -1 else None]
    def lrange(self, key, start, end): return self.data.get(key, [])[start:end + 1 if end != -1 else None]
    def delete(self, key): self.data.pop(key, None)
def test_redis_save_get_clear():
    memory = RedisMemory(); memory.client = FakeRedis()
    memory.save_message(1, "user", "Hello")
    assert memory.get_recent_messages(1)[0]["content"] == "Hello"
    memory.clear_conversation_memory(1)
    assert memory.get_recent_messages(1) == []
