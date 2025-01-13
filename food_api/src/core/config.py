import os

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__)).removesuffix(
    os.path.join("src", "core")
)


class Settings(BaseSettings):
    BASE_DIR: str = BASE_DIR
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/data/food_delivery.db"

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/../.env")


settings = Settings()
