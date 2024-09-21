"""This file represents configurations from files and environment."""
import os
import logging
from dataclasses import dataclass, field

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()


@dataclass
class BotConfig:
    """Bot configuration."""

    token: str = os.getenv('BOT_TOKEN')
    LOCALES: list[str] = field(default_factory=lambda: [
        'en', 'ru'
    ])
    DEFAULT_LOCALE: str = 'en'


@dataclass
class DifyConfig:
    api_key: str = os.getenv('DIFY_API_KEY')


@dataclass
class DatabaseConfig:
    """Database connection variables."""

    name: str | None = os.getenv('POSTGRES_DATABASE')
    user: str | None = os.getenv('POSTGRES_USER')
    passwd: str | None = os.getenv('POSTGRES_PASSWORD', None)
    port: int = int(os.getenv('POSTGRES_PORT', 5432))
    host: str = os.getenv('POSTGRES_HOST', 'db')

    driver: str = 'asyncpg'
    database_system: str = 'postgresql'

    def build_connection_str(self) -> str:
        """This function build a connection string."""
        return URL.create(
            drivername=f'{self.database_system}+{self.driver}',
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class Configuration:
    """All in one configuration's class."""
    logging_level = logging.INFO
    debug = bool(os.getenv('DEBUG'))

    bot = BotConfig()
    dify = DifyConfig()
    db = DatabaseConfig()


conf = Configuration()
