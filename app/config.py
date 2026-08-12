from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated, environment-backed application configuration."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    google_api_key: str | None = Field(default=None, validation_alias="GOOGLE_API_KEY")
    database_url_override: str | None = Field(default=None, validation_alias="DATABASE_URL")
    local_sqlite_path: Path = Field(default=Path("./data/local_app.db"), validation_alias="LOCAL_SQLITE_PATH")
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "enterprise_ai"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    redis_host: str = "localhost"
    redis_port: int = 6379
    vector_store_path: Path = Path("./data/vectorstore")
    documents_path: Path = Path("./data/documents")
    llm_model: str = "gemini-2.0-flash"
    embedding_model: str = "models/text-embedding-004"
    chunk_size: int = 1000
    chunk_overlap: int = 150
    retriever_top_k: int = 4
    max_upload_mb: int = 20

    @property
    def database_url(self) -> str:
        if self.database_url_override:
            return self.database_url_override
        if self.local_sqlite_path.is_absolute():
            sqlite_path = self.local_sqlite_path
        else:
            sqlite_path = Path.cwd() / self.local_sqlite_path
        return f"sqlite:///{sqlite_path.as_posix()}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
