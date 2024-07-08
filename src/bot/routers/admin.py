from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.types import BotCommandScopeChat

from src.bot.filters import StatusFilter
from src.config import settings

router = Router(name="admin")


@router.message(Command("admin"), StatusFilter("admin"))
async def enable_admin_mode(message: types.Message, bot: Bot):
    text = "You are the Admin!"
    await message.answer(text)
    await bot.set_my_commands(
        settings.bot_commands
        or []
        + [
            types.BotCommand(command="admin", description="Enable admin mode"),
        ],
        scope=BotCommandScopeChat(chat_id=message.from_user.id),
    )


@router.message(Command("admin"), ~StatusFilter("admin"))
async def failed_enable_admin_mode(message: types.Message, bot: Bot):
    text = "You are not the Admin!"
    await message.answer(text)
    await bot.set_my_commands(
        settings.bot_commands or [],
        scope=BotCommandScopeChat(chat_id=message.from_user.id),
    )
