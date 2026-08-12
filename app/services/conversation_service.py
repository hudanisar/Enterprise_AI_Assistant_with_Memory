class ConversationService:
    def __init__(self, repository): self.repository = repository
    def new(self, user_id, title="New conversation"): return self.repository.create_conversation(user_id, title)
    def list(self, user_id): return self.repository.list_conversations(user_id)

