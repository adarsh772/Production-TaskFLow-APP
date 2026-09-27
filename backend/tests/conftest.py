import os

# Point the app at a throwaway SQLite DB for the test session, and provide
# required settings so src.utils.settings.Settings() doesn't need a real .env.
os.environ.setdefault("DB_CONNECTION", "sqlite:///./test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-only")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("EXP_TIME", "30")

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.utils.db import Base, engine


@pytest.fixture(scope="session", autouse=True)
def _setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
    db_file = "./test.db"
    if os.path.exists(db_file):
        os.remove(db_file)


@pytest.fixture()
def client():
    return TestClient(app)
