from aiogram.types import BotCommand
from pydantic import TypeAdapter

commands_type_adapter = TypeAdapter(list[BotCommand])


def check_commands_equality(x: list[BotCommand], y: list[BotCommand]) -> bool:
    return commands_type_adapter.dump_json(x) == commands_type_adapter.dump_json(y)
