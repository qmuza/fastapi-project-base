from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):

    # default values, if .env is present will override automatically
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASS: str = "postgres"
    POSTGRES_DB: str = "postgres"

    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = ".env"

    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASS}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_sync_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL.replace("+asyncpg", "")
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASS}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
