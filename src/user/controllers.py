from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from src.user.dtos import LoginSchema, UserSchema
from src.user.models import UserModel
from src.utils.settings import Settings

# ...existing code...
EXP_TIME: int = 30
# ...existing code...
password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def registration(body: UserSchema, db: Session):
    if db.query(UserModel).filter(UserModel.username == body.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken",
        )

    if db.query(UserModel).filter(UserModel.email == body.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already in use",
        )

    new_user = UserModel(
        name=body.name,
        username=body.username,
        email=body.email,
        hash_password=get_password_hash(body.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def user_login(body: LoginSchema, db: Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()

    if not user or not verify_password(body.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=Settings.EXP_TIME)
    token = jwt.encode(
        {"_id": user.id, "exp": expires_at},
        Settings.SECRET_KEY,
        algorithm=Settings.ALGORITHM,
    )
    return {"token": token}