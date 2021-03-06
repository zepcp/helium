from pydantic import BaseModel
from typing import Dict, Optional, List


class Schema(BaseModel):
    hotspots: Dict[str, str]
    users: Dict[str, str]
    wallets: Dict[str, str]
    coingecko: Dict[str, str]


class Hotspot(BaseModel):
    owner: str
    address: Optional[str]


class User(BaseModel):
    email: str
    password: Optional[str]


class Wallet(BaseModel):
    owner: str
    address: Optional[str]


class CoinGecko(BaseModel):
    coins: str
    fiat: str


class Database:
    def get_user(self, email: str) -> User:
        pass

    def get_users(self) -> List[User]:
        pass

    def update_user(self, user: User) -> User:
        pass

    def add_user(self, user: User) -> User:
        pass

    def get_hotspot(self, owner: str) -> Hotspot:
        pass

    def get_hotspots(self) -> List[Hotspot]:
        pass

    def get_wallet(self, owner: str) -> Wallet:
        pass

    def get_wallets(self) -> List[Wallet]:
        pass

    def get_coingecko(self) -> CoinGecko:
        pass
