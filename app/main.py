import streamlit as st
from app.config import get_settings
from app.database.connection import Base, make_engine, make_session_factory
import app.database.models
from app.database.repositories import Repository
from app.memory.postgres_memory import PostgresMemory
from app.memory.memory_manager import MemoryManager
from app.memory.redis_memory import RedisMemory
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.llm.model import make_llm
from app.graph.workflow import build_workflow
from app.services.chat_service import ChatService
from app.services.document_service import save_and_ingest
from app.ui.components import apply_theme
from app.ui.sidebar import render_sidebar
from app.ui.memory_panel import render_memories
from app.ui.document_panel import render_documents
from app.ui.chat import render_chat, render_sources

st.set_page_config(page_title="Enterprise AI Assistant", page_icon="🤖", layout="wide")
apply_theme(); settings = get_settings()

@st.cache_resource
def dependencies():
    Base.metadata.create_all(make_engine(settings))
    session = make_session_factory()()
    repo = Repository(session); redis = RedisMemory(settings.redis_host, settings.redis_port)
    vector = VectorStore(settings.vector_store_path); manager = MemoryManager(PostgresMemory(repo))
    workflow = build_workflow(manager, Retriever(vector, settings.retriever_top_k), make_llm())
    return repo, vector, manager, ChatService(workflow, repo, redis, manager)

try:
    repo, vector, manager, chat_service = dependencies()
except Exception as exc:
    st.error(f"Service setup failed: {type(exc).__name__}: {exc}")
    st.stop()
user = repo.get_or_create_user(st.session_state.get("external_id", "demo-user"))
external_id, new_chat, selected = render_sidebar(repo.list_conversations(user.id))
st.session_state.external_id = external_id; user = repo.get_or_create_user(external_id)
if new_chat or "conversation_id" not in st.session_state: st.session_state.conversation_id = repo.create_conversation(user.id).id
if selected: st.session_state.conversation_id = selected
conversation = repo.get_conversation(user.id, st.session_state.conversation_id)
st.markdown("<div class='hero'><h1>Enterprise AI Assistant</h1><p>Intelligent conversations with persistent memory and knowledge retrieval</p></div>", unsafe_allow_html=True)
render_memories(repo.memories(user.id)); render_documents(lambda u: save_and_ingest(u, settings.documents_path, vector, repo, settings)); render_chat(repo.messages(conversation.id))
if query := st.chat_input("Ask about your work or company knowledge..."):
    st.chat_message("user").write(query)
    with st.chat_message("assistant"):
        with st.spinner("Assistant is typing..."):
            try:
                result = chat_service.chat(user.id, conversation.id, query)
                st.write(result["response"]); render_sources(result.get("sources", []))
            except Exception:
                st.error("I couldn't complete that request. Check configuration and try again.")
