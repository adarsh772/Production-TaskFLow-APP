from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.utils.db import Base


class UserModel(Base):
    __tablename__ = "UserTable"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hash_password = Column(String, nullable=False)

    tasks = relationship("TaskModel", back_populates="owner", cascade="all, delete-orphan")
