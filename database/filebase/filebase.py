from typing import Dict, List, Any
from json import loads, dumps

from database.database import Database, Schema, Hotspot, User, Wallet, CoinGecko


def read_table(table: str) -> Dict[str, Any]:
    try:
        return loads(open("database/filebase/{}.json".format(table), "r").read())
    except FileNotFoundError:
        open("database/filebase/{}.json".format(table), "w").write("{\n}")
        return {}


def update_table(table: str, content: Dict[str, Any]) -> None:
    filename = open("database/filebase/{}.json".format(table), "w")
    filename.write(dumps(content))
    filename.close()
    return


class Filebase(Database):
    def __init__(self):
        self.db = Schema(
            hotspots=read_table("hotspots"),
            users=read_table("users"),
            wallets=read_table("wallets"),
            coingecko=read_table("coingecko"),
        )

    def get_user(self, email: str) -> User:
        return User(
            email=email.lower(),
            password=self.db.users.get(email.lower())
        )

    def get_users(self) -> List[User]:
        users = []
        for user in self.db.users:
            users.append(self.get_user(user))
        return users

    def update_user(self, user: User) -> User:
        self.db.users[user.email] = user.password
        update_table("users", self.db.users)
        return user

    def add_user(self, user: User) -> User:
        self.db.users[user.email] = user.password
        update_table("users", self.db.users)
        return user

    def get_hotspot(self, owner: str) -> Hotspot:
        return Hotspot(
            owner=owner.lower(),
            address=self.db.hotspots.get(owner.lower())
        )

    def get_hotspots(self) -> List[Hotspot]:
        hotspots = []
        for hotspot in self.db.hotspots:
            hotspots.append(self.get_hotspot(hotspot))
        return hotspots

    def get_wallet(self, owner: str) -> Wallet:
        return Wallet(
            owner=owner.lower(),
            address=self.db.wallets.get(owner.lower())
        )

    def get_wallets(self) -> List[Wallet]:
        wallets = []
        for wallet in self.db.wallets:
            wallets.append(self.get_wallet(wallet))
        return wallets

    def get_coingecko(self) -> CoinGecko:
        return CoinGecko(
            coins=self.db.coingecko.get("coins"),
            fiat=self.db.coingecko.get("fiat"),
        )
