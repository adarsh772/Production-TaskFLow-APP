from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.utils.db import Base


class TaskModel(Base):
    __tablename__ = "UserTask"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column("Description", String)
    is_completed = Column("is_Completed", Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("UserTable.id"), nullable=False)

    owner = relationship("UserModel", back_populates="tasks")
