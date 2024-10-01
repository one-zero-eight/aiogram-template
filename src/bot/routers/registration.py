from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, KeyboardButton, Message, ReplyKeyboardMarkup

from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput, TextInput
from aiogram_dialog.manager.manager import DialogManager

from src.bot.filters import USER_REGISTERED_FILTER
from src.bot.routers.user import UserStates


class RegisterStates(StatesGroup):
    enter_name = State("enter_name")
    enter_phone = State("enter_phone")


async def name_on_success(
    message: Message,
    widget: ManagedTextInput[str],
    dialog_manager: DialogManager,
    data: str,
    /,
):
    dialog_manager.dialog_data["name"] = message.text
    await message.answer(
        "👀",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Send phone number", request_contact=True)]],
            one_time_keyboard=True,
            resize_keyboard=True,
            is_persistent=True,
        ),
    )
    await dialog_manager.switch_to(RegisterStates.enter_phone)


name_window = Window(
    Const("You are not registered. Please, follow the instructions.\n\nEnter your name:"),
    TextInput(id="name", on_success=name_on_success),
    state=RegisterStates.enter_name,
)


async def phone_on_message(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    from src.bot.app import dp, bot

    if message.contact is None or (message.contact.user_id != message.from_user.id):
        await message.answer("Please, send your phone number.")
        return
    dialog_manager.dialog_data["phone"] = message.contact.phone_number
    await dp.fsm.resolve_context(bot, chat_id=None, user_id=message.from_user.id).update_data(
        {
            "registered": True,
            "phone": dialog_manager.dialog_data["phone"],
            "name": dialog_manager.dialog_data["name"],
        }
    )
    await message.answer("You are registered successfully. Welcome!")
    await dialog_manager.start(UserStates.menu)


phone_window = Window(
    Const("Please, send your phone number"),
    MessageInput(phone_on_message),
    state=RegisterStates.enter_phone,
)


async def not_registered(event: CallbackQuery | Message, dialog_manager: DialogManager):
    await dialog_manager.start(RegisterStates.enter_name, mode=StartMode.RESET_STACK)


router = Dialog(name_window, phone_window, name="registration")
router.message.register(not_registered, ~USER_REGISTERED_FILTER)
router.callback_query.register(not_registered, ~USER_REGISTERED_FILTER)
