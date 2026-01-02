from dataclasses import dataclass
from environs import Env

@dataclass
class DatabaseConfig:
    name: str
    host: str
    user: str
    password: str

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]

@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_ID')))
        ),
        db=DatabaseConfig(
            name=env("DATABASE"),
            host=env("DB_HOST"),
            user=env("DB_USER"),
            password=env("DB_PASSWORD")
        )
    )