import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connection import Base
import app.database.models
from app.database.repositories import Repository
@pytest.fixture
def repo():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Repository(sessionmaker(bind=engine)())

