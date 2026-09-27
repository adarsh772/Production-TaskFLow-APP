from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.user import controllers
from src.user.dtos import LoginSchema, TokenResponse, UserResponseModel, UserSchema
from src.user.models import UserModel
from src.utils.db import get_db

user_routes = APIRouter(prefix="/user", tags=["user"])


@user_routes.post("/register", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
def register(body: UserSchema, db: Session = Depends(get_db)):
    return controllers.registration(body, db)


@user_routes.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(body: LoginSchema, db: Session = Depends(get_db)):
    return controllers.user_login(body, db)


@user_routes.get("/me", response_model=UserResponseModel, status_code=status.HTTP_200_OK)
def me(current_user: UserModel = Depends(controllers.get_current_user)):
    return current_user
