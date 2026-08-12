from app.config import get_settings


class LocalDemoResponse:
    def __init__(self, content: str):
        self.content = content


class LocalDemoLLM:
    """Small offline responder so the UI can run before Gemini is configured."""
    def invoke(self, prompt: str):
        return LocalDemoResponse(
            "Local demo mode is running. Gemini is not reachable right now, so I cannot generate a real AI answer. "
            "The app, database, memory storage, uploads, and local keyword document search are still working."
        )


class ResilientLLM:
    def __init__(self, primary, fallback=None):
        self.primary = primary
        self.fallback = fallback or LocalDemoLLM()

    def invoke(self, prompt: str):
        try:
            return self.primary.invoke(prompt)
        except Exception:
            return self.fallback.invoke(prompt)


def make_llm():
    settings = get_settings()
    if not settings.google_api_key:
        return LocalDemoLLM()
    from langchain_google_genai import ChatGoogleGenerativeAI
    primary = ChatGoogleGenerativeAI(model=settings.llm_model, google_api_key=settings.google_api_key, temperature=.2)
    return ResilientLLM(primary)
