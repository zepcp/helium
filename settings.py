from pydantic import BaseSettings

from database.database import Database
from database.filebase.filebase import Filebase


class Settings(BaseSettings):
    app_name: str = "Helium App"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expiration: int = 10 * 60  # Seconds
    database: Database = Filebase

    class Config:
        env_file = ".env"


settings = Settings()
