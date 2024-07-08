__all__ = ["lifespan"]

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.api.shared import Shared
from src.config import settings
from src.config_schema import Environment
from src.logging_ import logger
from src.modules.auth.repository import AuthRepository
from src.modules.user.repository import UserRepository
from src.storages.sqlalchemy.storage import SQLAlchemyStorage


async def setup_repositories():
    # ------------------- Repositories Dependencies -------------------
    async_engine = create_async_engine(settings.database.uri.get_secret_value())
    storage = SQLAlchemyStorage(async_engine)
    user_repository = UserRepository()
    auth_repository = AuthRepository()

    Shared.register_provider(AuthRepository, auth_repository)
    Shared.register_provider(SQLAlchemyStorage, storage)
    Shared.register_provider(UserRepository, user_repository)
    Shared.register_provider(AsyncSession, lambda: storage.create_session())

    if settings.environment == Environment.DEVELOPMENT:
        import logging

        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
        logger.info("SQLAlchemy logging is enabled!")


async def setup_predefined():
    user_repository = Shared.f(UserRepository)
    async with Shared.f(AsyncSession) as session:
        if not await user_repository.read_by_login(settings.predefined.first_superuser_login, session):
            await user_repository.create_superuser(
                login=settings.predefined.first_superuser_login,
                password=settings.predefined.first_superuser_password,
                session=session,
            )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup

    await setup_repositories()
    await setup_predefined()

    yield

    # Application shutdown
    from src.api.shared import Shared

    storage = Shared.f(SQLAlchemyStorage)
    await storage.close_connection()
