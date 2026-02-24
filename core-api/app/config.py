from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    core_api_port: int = 8000
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/giftforge"
    redis_url: str = "redis://localhost:6379/0"
    hmac_secret: str = "change-me-in-production"
    master_api_key: str = "master-key"
    admin_bot_token: str = ""
    client_bot_token: str = ""
    core_bot_token: str = ""
    qr_ttl_seconds: int = 300
    default_business_id: str = "COFFEE_001"
    default_business_budget: int = 50000
    allowed_baristas: str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
