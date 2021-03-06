from typing import List, Optional

from database.postgres.base import SessionLocal
from database.database import Database, User, Hotspot, Wallet, CoinGecko
from database.postgres.users import Users
from database.postgres.hotspots import Hotspots
from database.postgres.wallets import Wallets
from database.postgres.coingecko import CoingeckoValues


class Postgres(Database):
    def __init__(self):
        self.db = SessionLocal()

    def get_user(self, email: str) -> Optional[User]:
        try:
            user = self.db.query(Users).filter(Users.email == email.lower()).first()
            return User(email=user.email, password=user.password)
        except AttributeError:
            return

    def get_users(self) -> List[User]:
        users = []
        for user in self.db.query(Users).all():
            users.append(User(email=user.email, password=user.password))
        return users

    def update_user(self, user: User) -> User:
        self.db.query(Users).filter(Users.email == user.email).update({"password": user.password})
        self.db.commit()
        return user

    def add_user(self, user: User) -> User:
        self.db.add(Users(email=user.email, password=user.password))
        self.db.commit()
        return user

    def get_hotspot(self, owner: str) -> Hotspot:
        hotspot = self.db.query(Hotspots).filter(Hotspots.owner == owner.lower()).first()
        return Hotspot(owner=hotspot.owner, address=hotspot.address)

    def get_hotspots(self) -> List[Hotspot]:
        hotspots = []
        for hotspot in self.db.query(Hotspots).all():
            hotspots.append(Hotspot(owner=hotspot.owner, address=hotspot.address))
        return hotspots

    def get_wallet(self, owner: str) -> Wallet:
        wallet = self.db.query(Wallets).filter(Wallets.owner == owner.lower()).first()
        return Wallet(owner=wallet.owner, address=wallet.address)

    def get_wallets(self) -> List[Wallet]:
        wallets = []
        for wallet in self.db.query(Wallets).all():
            wallets.append(Wallet(owner=wallet.owner, address=wallet.address))
        return wallets

    def get_coingecko(self) -> CoinGecko:
        coins = self.db.query(CoingeckoValues).filter(CoingeckoValues.key == "coins").first()
        fiat = self.db.query(CoingeckoValues).filter(CoingeckoValues.key == "fiat").first()
        return CoinGecko(coins=coins.value, fiat=fiat.value)
