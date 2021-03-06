from pydantic import BaseSettings


class Settings(BaseSettings):
    db_name: str = "helium"
    db_host: str = "localhost"
    db_user: str = "postgres"
    db_password: str = "postgres"

    class Config:
        env_file = ".env"


settings = Settings()
