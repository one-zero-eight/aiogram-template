from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const


class UserStates(StatesGroup):
    menu = State("menu")


menu_ww = Window(
    Const("Menu"),
    Button(Const("Just a Button"), id="button"),
    state=UserStates.menu,
)

router = Dialog(menu_ww, name="user")
