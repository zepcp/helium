from sqlalchemy import Column, String

from database.postgres.base import Base


class Users(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True, nullable=False)
    password = Column(String)
