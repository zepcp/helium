"""Docs: https://docs.helium.com/api"""
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from requests import get

from database.database import Database
from apis.authentication import oauth2_token
from settings import settings

router = APIRouter()
router.dependencies = [oauth2_token]


def get_reward(hotspot: str, min_time: str, max_time: str) -> float:
    response = get("https://api.helium.io/v1/hotspots/{}/rewards/sum".format(hotspot),
                   params={"min_time": min_time, "max_time": max_time})
    return response.json()["data"]["sum"] / 10**8


def get_balance(wallet: str) -> float:
    response = get("https://api.helium.io/v1/accounts/{}/".format(wallet))
    return response.json().get("data").get("balance") / 10**8


def get_price() -> float:
    response = get("https://api.helium.io/v1/oracle/prices/current")
    return response.json().get("data").get("price") / 10 ** 8


@router.get("/reward/{owner}", response_model=Dict[str, Any])
async def reward(owner: str, min_time: str, max_time: str, db: Database = Depends(settings.database)):
    hotspot = db.get_hotspot(owner=owner)
    amount = get_reward(hotspot.address, min_time=min_time, max_time=max_time)
    return {
        "hotspot": hotspot,
        "reward": {
            "total": round(amount, 2),
            "referral": round(amount * 0.05, 2),
            "owner": round(amount * 0.1, 2),
        },
    }


@router.get("/rewards", response_model=List[Dict[str, Any]])
async def rewards(min_time: str, max_time: str, db: Database = Depends(settings.database)):
    response = []
    for hotspot in db.get_hotspots():
        amount = get_reward(hotspot.address, min_time=min_time, max_time=max_time)
        response.append({
            "hotspot": hotspot,
            "reward": {
                "total": round(amount, 2),
                "referral": round(amount * 0.05, 2),
                "owner": round(amount * 0.1, 2),
            },
        })
    return response


@router.get("/balance/{owner}", response_model=Dict[str, Any])
async def balance(owner: str, db: Database = Depends(settings.database)):
    wallet = db.get_wallet(owner=owner)
    return {
        "wallet": wallet,
        "balance": round(get_balance(wallet.address), 2)
    }


@router.get("/balances", response_model=List[Dict[str, Any]])
async def balances(db: Database = Depends(settings.database)):
    response = []
    for wallet in db.get_wallets():
        response.append({
            "wallet": wallet,
            "balance": rount(get_balance(wallet.address), 2)
        })
    return response


@router.get("/price", response_model=Dict[str, Any])
async def price():
    return {
        "price": round(get_price(), 2),
    }
