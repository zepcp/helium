from sqlalchemy import Column, String

from database.postgres.base import Base


class Wallets(Base):
    __tablename__ = "wallets"

    owner = Column(String, primary_key=True, index=True, nullable=False)
    address = Column(String, unique=True, nullable=False)
