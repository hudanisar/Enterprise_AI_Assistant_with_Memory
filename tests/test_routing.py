from app.graph.routing import Route, classify_query
def test_routes():
    assert classify_query("Hello") == Route.GENERAL
    assert classify_query("What did I tell you about my project?") == Route.MEMORY
    assert classify_query("What is our leave policy?") == Route.RAG
    assert classify_query("What is our policy and what do I prefer?") == Route.HYBRID

