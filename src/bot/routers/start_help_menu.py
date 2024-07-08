from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart, Command

router = Router(name="start_help_menu")


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Welcome! You registered in the system. Use /help to see the list of available commands.")


@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer("Available commands:\n/help - show this message\n/menu - show the main menu")


@router.message(Command("menu"))
async def menu(message: types.Message):
    await message.answer("For now, the main menu is empty.")
