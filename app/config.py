from pydantic_settings import BaseSettings
from pydantic import SecretStr
from typing import Optional


class Settings(BaseSettings):
    bot_token: SecretStr
    database_url: str
    redis_url: str
    admin_user_id: int
    slot_duration: int = 60  # in minutes
    default_reminder_time: int = 24  # in hours
    office_location: Optional[str] = None  # format: "lat,lon|address"
    timezone: str = "Europe/Moscow"
    log_file: str = "logs/bot.log"
    loyalty_visits: int = 5  # number of visits for loyalty discount
    loyalty_discount: int = 10  # discount percentage
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


# Create settings instance
settings = Settings()