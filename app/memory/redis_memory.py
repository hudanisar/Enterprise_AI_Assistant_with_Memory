import json, logging
logger = logging.getLogger(__name__)

class RedisMemory:
    def __init__(self, host="localhost", port=6379, max_messages=20):
        self.max_messages, self.client = max_messages, None
        try:
            import redis
            self.client = redis.Redis(host=host, port=port, decode_responses=True, socket_connect_timeout=1)
            self.client.ping()
        except Exception as exc: logger.warning("Redis unavailable; continuing without cache: %s", type(exc).__name__); self.client = None
    def _key(self, cid): return f"conversation:{cid}:messages"
    def save_message(self, cid, role, content):
        if self.client:
            self.client.rpush(self._key(cid), json.dumps({"role": role, "content": content})); self.trim_history(cid)
    def get_recent_messages(self, cid):
        if not self.client: return []
        try: return [json.loads(v) for v in self.client.lrange(self._key(cid), 0, -1)]
        except Exception: return []
    def trim_history(self, cid):
        if self.client: self.client.ltrim(self._key(cid), -self.max_messages, -1)
    def clear_conversation_memory(self, cid):
        if self.client: self.client.delete(self._key(cid))
    def health_check(self):
        try: return bool(self.client and self.client.ping())
        except Exception: return False

