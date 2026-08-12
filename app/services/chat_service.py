class ChatService:
    def __init__(self, workflow, repository, redis_memory, memory_manager):
        self.workflow, self.repository, self.redis, self.memory_manager = workflow, repository, redis_memory, memory_manager
    def chat(self, user_id, conversation_id, query):
        if not self.repository.get_conversation(user_id, conversation_id): raise PermissionError("Conversation not found for this user.")
        self.repository.add_message(conversation_id, "user", query); self.redis.save_message(conversation_id, "user", query)
        history = self.redis.get_recent_messages(conversation_id) or [{"role": m.role, "content": m.content} for m in self.repository.messages(conversation_id)[-20:]]
        result = self.workflow.invoke({"user_id": user_id, "conversation_id": conversation_id, "query": query, "chat_history": history})
        self.repository.add_message(conversation_id, "assistant", result["response"]); self.redis.save_message(conversation_id, "assistant", result["response"])
        self.memory_manager.process_message(user_id, query)
        return result

