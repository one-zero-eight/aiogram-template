from typing import Any, Literal

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import User, TelegramObject

from src.config import settings


class UserRegisteredFilter(Filter):
    async def __call__(self, event: TelegramObject, event_from_user: User, state: FSMContext) -> bool | dict[str, Any]:
        data = await state.get_data()
        is_registered = data.get("registered", False)
        return is_registered


class StatusFilter(Filter):
    _status: Literal["admin", "user"] | None

    def __init__(self, status: Literal["admin", "user"] | None = None):
        self._status = status

    async def __call__(self, event: TelegramObject, event_from_user: User) -> bool | dict[str, Any]:
        telegram_id = event_from_user.id
        status = "admin" if telegram_id in settings.admins else "user"

        if self._status is None:
            return {"status": status}

        if status == self._status:
            return True
        return False


USER_REGISTERED_FILTER = UserRegisteredFilter()
