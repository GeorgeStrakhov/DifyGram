"""Database middleware is a common way to inject database dependency in handlers."""
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.bot.structures.data_structure import TransferData
from src.configuration import conf
from src.db.database import Database, create_async_engine


class DatabaseMiddleware(BaseMiddleware):
    """This middleware throw a Database class to handler."""

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        """This method calls every update."""
        engine: AsyncEngine = data.get('engine') or create_async_engine(
            url=conf.db.build_connection_str()
        )
        async with AsyncSession(bind=engine) as session:
            data['db'] = Database(session)
            return await handler(event, data)
