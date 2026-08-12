from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import Settings, get_settings


class Base(DeclarativeBase):
    pass


def make_engine(settings: Settings | None = None):
    settings = settings or get_settings()
    url = settings.database_url
    engine_kwargs = {"pool_pre_ping": True}
    if url.startswith("sqlite"):
        if url != "sqlite:///:memory:":
            db_path = url.replace("sqlite:///", "", 1)
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    return create_engine(url, **engine_kwargs)


def make_session_factory(settings: Settings | None = None):
    return sessionmaker(bind=make_engine(settings), expire_on_commit=False)


def health_check(settings: Settings | None = None) -> bool:
    try:
        with make_engine(settings).connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
