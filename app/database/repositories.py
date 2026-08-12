from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.models import Conversation, Document, Memory, Message, User


class Repository:
    def __init__(self, session: Session): self.session = session
    def get_or_create_user(self, external_id: str) -> User:
        user = self.session.scalar(select(User).where(User.external_id == external_id))
        if not user:
            user = User(external_id=external_id); self.session.add(user); self.session.commit(); self.session.refresh(user)
        return user
    def create_conversation(self, user_id: int, title: str = "New conversation") -> Conversation:
        item = Conversation(user_id=user_id, title=title); self.session.add(item); self.session.commit(); self.session.refresh(item); return item
    def get_conversation(self, user_id: int, conversation_id: int) -> Conversation | None:
        return self.session.scalar(select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id))
    def list_conversations(self, user_id: int): return self.session.scalars(select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())).all()
    def add_message(self, conversation_id: int, role: str, content: str) -> Message:
        item = Message(conversation_id=conversation_id, role=role, content=content); self.session.add(item); self.session.commit(); return item
    def messages(self, conversation_id: int): return self.session.scalars(select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)).all()
    def upsert_memory(self, user_id: int, memory_type: str, content: str, importance: float = .7) -> Memory:
        existing = self.session.scalar(select(Memory).where(Memory.user_id == user_id, Memory.content == content))
        if existing: existing.importance = max(existing.importance, importance); self.session.commit(); return existing
        item = Memory(user_id=user_id, memory_type=memory_type, content=content, importance=importance); self.session.add(item); self.session.commit(); return item
    def memories(self, user_id: int): return self.session.scalars(select(Memory).where(Memory.user_id == user_id).order_by(Memory.importance.desc())).all()
    def add_document(self, **kwargs):
        item = Document(**kwargs); self.session.add(item); self.session.commit(); self.session.refresh(item); return item
    def document_by_hash(self, file_hash: str): return self.session.scalar(select(Document).where(Document.file_hash == file_hash))

