from app.graph.workflow import build_workflow
class Memory:
    def retrieve(self, user_id, query): return []
class Retriever:
    def retrieve(self, query): return []
class Reply:
    content = "Test response"
class LLM:
    def invoke(self, prompt): return Reply()
def test_workflow_runs():
    graph = build_workflow(Memory(), Retriever(), LLM())
    assert graph.invoke({"user_id":1,"conversation_id":1,"query":"Hello"})["response"] == "Test response"

