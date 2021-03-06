from typing import Dict, Optional, Union
from time import time

from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

from database.database import Database, User
from settings import settings

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
oauth2_token = Depends(oauth2_schema)


class UpdatePassword(BaseModel):
    old: str
    new: str
    confirm: str


def login(db: Database, email: str, password: str) -> Optional[User]:
    user = db.get_user(email)
    if user and pwd_context.verify(password, user.password):
        return User(email=email, password=password)
    raise unauthorized("Incorrect username or password")


def get_token(user: User) -> Dict[str, str]:
    data = {"sub": user.email, "exp": time() + settings.access_token_expiration}
    encoded_jwt = jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)
    return {"access_token": encoded_jwt, "token_type": "bearer"}


def get_user(db: Database, token: str) -> User:
    payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
    email = payload.get("sub")
    return db.get_user(email=email)


def unauthorized(detail: str) -> HTTPException:
    return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/login", response_model=Dict[str, str])
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Database = Depends(settings.database),
):
    user = login(db, form_data.username, form_data.password)
    if not user:
        raise unauthorized("Incorrect username or password")
    return get_token(user)


@router.put("/change_password", response_model=User)
async def change_password(
        password: UpdatePassword,
        token: str = oauth2_token,
        db: Database = Depends(settings.database),
):
    user = get_user(db, token)
    if not pwd_context.verify(password.old, user.password):
        raise unauthorized("Incorrect username or password")
    if password.new != password.confirm:
        raise unauthorized("Passwords don't match")
    user.password = pwd_context.hash(password.new)
    return db.update_user(user)


@router.get("/me", response_model=User)
async def get_current_user(
        token: str = oauth2_token,
        db: Database = Depends(settings.database),
):
    return get_user(db, token)
