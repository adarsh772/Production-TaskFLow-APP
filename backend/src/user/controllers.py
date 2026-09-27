from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, Request, status
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from src.user.dtos import LoginSchema, UserSchema
from src.user.models import UserModel
from src.utils.db import get_db
from src.utils.settings import settings

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def registration(body: UserSchema, db: Session) -> UserModel:
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


def user_login(body: LoginSchema, db: Session) -> dict:
    user = db.query(UserModel).filter(UserModel.username == body.username).first()

    if not user or not verify_password(body.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode(
        {"_id": user.id, "exp": expires_at},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return {"token": token, "token_type": "bearer"}


def get_current_user(request: Request, db: Session = Depends(get_db)) -> UserModel:
    """FastAPI dependency: resolves the authenticated user from the
    'Authorization: Bearer <token>' header, or raises 401."""
    auth_header = request.headers.get("authorization")
    if not auth_header or " " not in auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header",
        )

    token = auth_header.split(" ")[-1]

    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    user_id = data.get("_id")
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
        )

    return user
