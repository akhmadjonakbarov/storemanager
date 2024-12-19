from typing import Any, Callable, Set

from pydantic import (
    AliasChoices,
    AmqpDsn,
    BaseModel,
    Field,
    ImportString,
    PostgresDsn,
    RedisDsn,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR = "/api/v1"
    TIME_ZONE = 'Asia/Tashkent'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 120
    SECRET_KEY: str = "dd9a735175a83222d92c987aec57f4bde11f0e770b5d9ebd5803f734b290edba"
    ALGORITHM = "HS256"


settings = Settings()
