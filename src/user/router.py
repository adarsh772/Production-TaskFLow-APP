from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserSchema
from src.user import controllers


user_routes=APIRouter("/user",status_code=status.HTTP_201_CREATED)

@user_routes.post("/register")
def register(body:UserSchema,db:Session=Depends(get_db)):
    return controllers.register(body,db)
