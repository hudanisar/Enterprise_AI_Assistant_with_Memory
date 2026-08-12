from app.config import get_settings
def make_embeddings():
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    settings = get_settings()
    if not settings.google_api_key: raise RuntimeError("GOOGLE_API_KEY is required for document embeddings.")
    return GoogleGenerativeAIEmbeddings(model=settings.embedding_model, google_api_key=settings.google_api_key)

