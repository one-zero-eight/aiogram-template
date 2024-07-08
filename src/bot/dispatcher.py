from typing import Any

from aiogram import Dispatcher, Bot
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.types import Update, User, Message, CallbackQuery

from src.bot.logging_ import logger


# noinspection PyMethodMayBeStatic
class CustomDispatcher(Dispatcher):
    async def _send_dunno_message(self, bot: Bot, chat_id: int):
        await bot.send_message(
            chat_id,
            "⚡️ I don't understand you. Please, use /start command.",
        )

    async def _listen_update(self, update: Update, **kwargs) -> Any:
        res = await super()._listen_update(update, **kwargs)
        if res is UNHANDLED:
            bot: Bot = kwargs.get("bot")
            event_from_user: User = kwargs.get("event_from_user")
            username = event_from_user.username
            user_string = f"User @{username}<{event_from_user.id}>" if username else f"User <{event_from_user.id}>"
            event = update.event
            event_type = type(event).__name__

            if isinstance(event, Message):
                message_text = f"{event.text[:50]}..." if len(event.text) > 50 else event.text
                msg = f"{user_string}: [{event_type}] `{message_text}`"
            elif isinstance(event, CallbackQuery):
                msg = f"{user_string}: [{event_type}] `{event.data}`"
            else:
                msg = f"{user_string}: [{event_type}]"

            logger.warning(f"Unknown event from user. {msg}")
            await self._send_dunno_message(bot, event_from_user.id)
        return res
