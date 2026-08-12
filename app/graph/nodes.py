from app.graph.routing import classify_query
from app.llm.prompts import answer_prompt
def route_node(state): return {"route": classify_query(state["query"]).value}
def memory_node(state, manager): return {"memories": [m.content for m in manager.retrieve(state["user_id"], state["query"])]}
def document_node(state, retriever):
    results = retriever.retrieve(state["query"]) if retriever and state.get("route") in ("RAG", "HYBRID") else []
    return {"retrieved_documents": [d.page_content for d, _ in results], "sources": [d.metadata for d, _ in results]}
def response_node(state, llm):
    prompt=answer_prompt(state["query"], state.get("chat_history", []), state.get("memories", []), state.get("retrieved_documents", []))
    return {"response": llm.invoke(prompt).content}

