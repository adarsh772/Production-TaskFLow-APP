from sqlalchemy import Column,Integer,String,DateTime,Boolean
from pydantic import EmailStr
from src.utils.db import Base

class UserModel(Base):
    __tablename__="UserTable"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    username=Column(String,unique=True,nullable=False)
    email=Column(EmailStr,unique=True,nullable=False)
    hash_password=Column(String,nullable=False)