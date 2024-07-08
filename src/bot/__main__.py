import asyncio

from aiogram import Bot, F
from aiogram import types
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.types import ErrorEvent
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent

from src.bot.logging_ import logger
from src.bot.dispatcher import CustomDispatcher
from src.bot.middlewares import LogAllEventsMiddleware
from src.config import settings

bot = Bot(token=settings.bot_token.get_secret_value())
if settings.redis_url:
    storage = RedisStorage.from_url(
        settings.redis_url.get_secret_value(), key_builder=DefaultKeyBuilder(with_destiny=True)
    )
    logger.info("Using Redis storage")
else:
    storage = MemoryStorage()
    logger.info("Using Memory storage")
dp = CustomDispatcher(storage=storage)
log_all_events_middleware = LogAllEventsMiddleware()
dp.message.middleware(log_all_events_middleware)
dp.callback_query.middleware(log_all_events_middleware)


@dp.error(ExceptionTypeFilter(UnknownIntent), F.update.callback_query.as_("callback_query"))
async def unknown_intent_handler(event: ErrorEvent, callback_query: types.CallbackQuery):
    await callback_query.answer("Unknown intent: Please, try to restart the action.")


from src.bot.routers.registration import router as router_registration  # noqa: E402
from src.bot.routers.start_help_menu import router as start_help_menu_router  # noqa: E402
from src.bot.routers.admin import router as router_admin  # noqa: E402

dp.include_router(router_registration)  # sink for not registered users
dp.include_router(start_help_menu_router)  # start, help, menu commands
dp.include_router(router_admin)  # admin commands

setup_dialogs(dp)


@dp.startup()
async def on_startup():
    logger.info("Bot starting...")
    # Set bot name, description and commands
    existing_bot = {
        "name": (await bot.get_my_name()).name,
        "description": (await bot.get_my_description()).description,
        "shortDescription": (await bot.get_my_short_description()).short_description,
        "commands": await bot.get_my_commands(),
    }

    if settings.bot_name and existing_bot["name"] != settings.bot_name:
        await bot.set_my_name(settings.bot_name)
    if settings.bot_description and existing_bot["description"] != settings.bot_description:
        await bot.set_my_description(settings.bot_description)
    if settings.bot_short_description and existing_bot["shortDescription"] != settings.bot_short_description:
        await bot.set_my_short_description(settings.bot_short_description)
    if settings.bot_commands and existing_bot["commands"] != settings.bot_commands:
        await bot.set_my_commands(settings.bot_commands)


@dp.shutdown()
async def on_shutdown():
    logger.info("Bot shutting down...")


async def main():
    # Drop pending updates
    await bot.delete_webhook(drop_pending_updates=True)
    # Start long-polling
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


# NOTE: No need for if __name__ == "__main__":, because this is the __main__.py module already
asyncio.run(main())
