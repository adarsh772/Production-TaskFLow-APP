from sqlalchemy import Column,Integer , Boolean,String
from src.utils.db import Base

class TaskModel(Base):
    __tablename__="UserTask"

    id=Column(Integer ,primary_key=True)
    title=Column(String )
    discription=Column("Discription", String)
    is_completed=Column("is_Completed", Boolean, default=False)

