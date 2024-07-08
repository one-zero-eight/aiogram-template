__all__ = ["User", "UserRole"]

from enum import StrEnum

from sqlalchemy import Enum

from src.storages.sqlalchemy.models.__mixin__ import IdMixin
from src.storages.sqlalchemy.models.base import Base
from src.storages.sqlalchemy.utils import *


class UserRole(StrEnum):
    DEFAULT = "default"
    ADMIN = "admin"


class User(Base, IdMixin):
    __tablename__ = "users"

    name: Mapped[str | None]
    login: Mapped[str] = mapped_column(unique=True)

    password_hash: Mapped[str]
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.DEFAULT)
