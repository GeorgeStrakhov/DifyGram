"""Init file for models namespace."""
from src.db.models.base import Base
from src.db.models.user import User

__all__ = (
    'Base',
    'User',
)
