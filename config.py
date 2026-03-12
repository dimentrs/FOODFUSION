import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Defaults match `compose.yaml` + `.env.example`.
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "foodfusion"
    DB_USER: str = "foodfusion"
    DB_PASSWORD: str = "foodfusion"

    # Optional: only needed if you use Telegram integration.
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


TELEGRAM_API_URL = (
    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    if settings.TELEGRAM_BOT_TOKEN
    else ""
)


def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
