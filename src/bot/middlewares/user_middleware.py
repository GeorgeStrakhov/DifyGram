import logging
from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, Update
from aiogram.types import User as TelegramUser
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.bot.structures.role import Role
from src.configuration import conf
from src.db import Database
from src.db.database import create_async_engine
from src.db.models import User

logger = logging.getLogger(__name__)


class RegisterCheck(BaseMiddleware):
    """
    Middleware будет вызываться каждый раз, когда пользователь будет отправлять боту сообщения (или нажимать
    на кнопку в инлайн-клавиатуре).
    """

    async def __call__(
            self,
            handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        """Сама функция для обработки вызова"""
        db: Database = data['db']
        tg_user: TelegramUser = event.from_user
        user: Row[User] = await db.user.get_by_where(User.user_id == tg_user.id)
        if user:
            data['user'] = user[0]
            logger.debug('User from database injected')
        else:
            logger.info('User not found. Creating new...')
            new_user: User = await db.user.new(
                    user_id=tg_user.id,
                    user_name=tg_user.username,
                    first_name=tg_user.first_name,
                    language_code=tg_user.language_code,
                    second_name=tg_user.last_name,
                    is_premium=tg_user.is_premium,
                    role=Role.USER,
                )
            logger.info('New user created')
            data['user'] = new_user
            await db.session.commit()
        return await handler(event, data)
