from aiogram import Bot, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommandScopeChat
from aiogram_dialog import DialogManager, StartMode

from src.bot.filters import USER_REGISTERED_FILTER, StatusFilter
from src.bot.routers.admin import AdminStates
from src.bot.routers.registration import RegisterStates
from src.bot.routers.user import UserStates
from src.config import settings

router = Router(name="commands")


@router.message(CommandStart(), USER_REGISTERED_FILTER)
async def start(message: types.Message):
    await message.answer("Welcome! You registered in the system. Use /help to see the list of available commands.")


@router.message(CommandStart(), ~USER_REGISTERED_FILTER)
async def start_not_registered(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(RegisterStates.enter_name, mode=StartMode.RESET_STACK)


@router.message(Command("help"))
async def go_help(message: types.Message):
    await message.answer("Available commands:\n/help - show this message\n/menu - show the main menu")


@router.message(Command("menu"), USER_REGISTERED_FILTER)
async def go_menu(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserStates.menu, mode=StartMode.RESET_STACK)


@router.message(Command("admin"), StatusFilter("admin"))
async def enable_admin_mode(message: types.Message, bot: Bot, dialog_manager: DialogManager):
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
    await dialog_manager.start(AdminStates.menu, mode=StartMode.RESET_STACK)


@router.message(Command("admin"), ~StatusFilter("admin"))
async def failed_enable_admin_mode(message: types.Message, bot: Bot):
    text = "You are not the Admin!"
    await message.answer(text)
    await bot.set_my_commands(
        settings.bot_commands or [],
        scope=BotCommandScopeChat(chat_id=message.from_user.id),
    )
