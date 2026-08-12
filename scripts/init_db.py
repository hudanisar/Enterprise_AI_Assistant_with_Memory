import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.database.connection import Base, make_engine
import app.database.models
Base.metadata.create_all(make_engine())
print("Database tables initialized.")
