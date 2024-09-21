"""This package is used for middlewares."""
from src.bot.middlewares.db_middleware import DatabaseMiddleware
from src.bot.middlewares.user_middleware import RegisterCheck

middlewares = (
    DatabaseMiddleware(),
    RegisterCheck()
)
