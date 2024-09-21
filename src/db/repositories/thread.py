"""Thread repository file."""
import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role

from ..models import Base, User
from .abstract import Repository
from ..models.thread import Thread


class ThreadRepo(Repository[Thread]):
    """Thread repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize thread repository as for all users or only for one user."""
        super().__init__(type_model=Thread, session=session)

    async def new(
            self,
            conversation_id: str,
            user: User,
    ) -> None:
        await self.session.merge(
            Thread(
                conversation_id=conversation_id,
                user=user
            )
        )
