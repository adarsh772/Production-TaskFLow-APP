from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.utils.settings import settings
Base=declarative_base()

engine=create_engine(url=settings.DB_CONNECTION)

Localsession=sessionmaker(bind=engine)

def get_db():
    session=Localsession()
    try:
        yield session
    finally:
        session.close()    

