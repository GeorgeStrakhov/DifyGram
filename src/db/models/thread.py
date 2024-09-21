"""Thread model file."""
import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from .user import User

from .base import Base


class Thread(Base):
    """Thread model."""

    conversation_id: Mapped[str] = mapped_column(sa.Text, nullable=False, unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'))
    user: Mapped[User] = orm.relationship('User', lazy='selectin')
