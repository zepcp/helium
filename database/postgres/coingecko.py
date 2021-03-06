from sqlalchemy import Column, String

from database.postgres.base import Base


class CoingeckoValues(Base):
    __tablename__ = "coingecko"

    key = Column(String, primary_key=True, index=True, nullable=False)
    value = Column(String)
