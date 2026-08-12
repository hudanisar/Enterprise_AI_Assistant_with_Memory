from enum import Enum
class Route(str, Enum): GENERAL="GENERAL"; MEMORY="MEMORY"; RAG="RAG"; HYBRID="HYBRID"
MEMORY_WORDS=("remember", "prefer", "told you", "my project", "about me")
RAG_WORDS=("policy", "handbook", "according to", "company", "document", "knowledge base")
def classify_query(query: str) -> Route:
    q=query.lower(); memory=any(w in q for w in MEMORY_WORDS); rag=any(w in q for w in RAG_WORDS)
    return Route.HYBRID if memory and rag else Route.MEMORY if memory else Route.RAG if rag else Route.GENERAL

