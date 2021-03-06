from sqlalchemy import Column, String

from database.postgres.base import Base


class Hotspots(Base):
    __tablename__ = "hotspots"

    owner = Column(String, primary_key=True, index=True, nullable=False)
    address = Column(String, unique=True, nullable=False)
