from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.utils.settings import settings

Base = declarative_base()

_connect_args = {"check_same_thread": False} if settings.DB_CONNECTION.startswith("sqlite") else {}
engine = create_engine(url=settings.DB_CONNECTION, connect_args=_connect_args)

LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()
