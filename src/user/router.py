from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserSchema,UserResponseModel,LoginSchema
from src.user import controllers



user_routes=APIRouter(prefix="/user")

@user_routes.post("/register",response_model=UserResponseModel,status_code=status.HTTP_201_CREATED)
def register(body:UserSchema,db:Session=Depends(get_db)):
    return controllers.registration(body,db)


@user_routes.post("/login",status_code=status.HTTP_200_OK)
def login(body:LoginSchema,db:Session=Depends(get_db)):
    return controllers.user_login(body,db)