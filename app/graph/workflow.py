from langgraph.graph import END, START, StateGraph
from app.graph.state import AssistantState
from app.graph.nodes import document_node, memory_node, response_node, route_node

def build_workflow(memory_manager, retriever, llm):
    graph=StateGraph(AssistantState)
    graph.add_node("classify_query", route_node)
    graph.add_node("retrieve_memory", lambda s: memory_node(s, memory_manager))
    graph.add_node("retrieve_documents", lambda s: document_node(s, retriever))
    graph.add_node("generate_response", lambda s: response_node(s, llm))
    graph.add_edge(START,"classify_query"); graph.add_edge("classify_query","retrieve_memory"); graph.add_edge("retrieve_memory","retrieve_documents"); graph.add_edge("retrieve_documents","generate_response"); graph.add_edge("generate_response",END)
    return graph.compile()

