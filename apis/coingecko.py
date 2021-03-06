"""Docs: https://www.coingecko.com/en/api"""
from typing import Any, Dict

from fastapi import APIRouter, Depends
from requests import get

from database.database import Database, CoinGecko
from apis.authentication import oauth2_token
from settings import settings

router = APIRouter()
router.dependencies = [oauth2_token]


def get_coingecko(coingecko: CoinGecko) -> Dict[str, Any]:
    response = get("https://api.coingecko.com/api/v3/simple/price",
                   params={"ids": coingecko.coins, "vs_currencies": coingecko.fiat})
    return response.json()


@router.get("/prices", response_model=Dict[str, Any])
async def price(db: Database = Depends(settings.database)):
    return {
        "price": get_coingecko(db.get_coingecko()),
    }
