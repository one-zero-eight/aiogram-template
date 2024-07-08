from aiogram import Router, Bot, F
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state

from src.bot.filters import UserRegisteredFilter

router = Router(name="registration")


@router.callback_query(any_state, F.data == "register", UserRegisteredFilter())
async def registered_user(callback_query: types.CallbackQuery, bot: Bot, event_from_user: types.User):
    await bot.send_message(event_from_user.id, "You are already registered.")
    await callback_query.answer()


@router.callback_query(any_state, F.data == "register", ~UserRegisteredFilter())
async def register_user(callback_query: types.CallbackQuery, bot: Bot, event_from_user: types.User, state: FSMContext):
    await state.update_data(registered=True)
    await bot.send_message(event_from_user.id, "You are registered successfully.")
    await state.set_state(None)
    await callback_query.answer()
    await callback_query.message.delete()


@router.message(any_state, ~UserRegisteredFilter())
@router.callback_query(any_state, ~UserRegisteredFilter())
async def not_registered(_, bot: Bot, state: FSMContext, event_from_user: types.User):
    cb = types.InlineKeyboardButton(text="Register", callback_data="register")
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[cb]])
    await bot.send_message(event_from_user.id, "You are not registered. Please, register.", reply_markup=kb)
    await state.set_state(None)
