from typing import List

from fastapi import APIRouter, Depends

from database.database import Database, User
from apis.authentication import oauth2_token, pwd_context
from settings import settings

router = APIRouter()
router.dependencies = [oauth2_token]


@router.get("/", response_model=List[User])
async def get_users(
        db: Database = Depends(settings.database),
):
    return db.get_users()


@router.post("/", response_model=User)
async def add_user(
        user: User,
        db: Database = Depends(settings.database),
):
    user.password = pwd_context.hash(user.password)
    return db.add_user(user)
