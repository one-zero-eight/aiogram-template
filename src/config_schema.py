from enum import StrEnum
from pathlib import Path

import yaml
from aiogram.types import BotCommand
from pydantic import BaseModel, ConfigDict, Field, SecretStr


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class SettingBaseModel(BaseModel):
    model_config = ConfigDict(use_attribute_docstrings=True, extra="forbid")


class Settings(SettingBaseModel):
    """
    Settings for the application.
    """

    schema_: str = Field(None, alias="$schema")
    environment: Environment = Environment.DEVELOPMENT
    "App environment flag"
    redis_url: SecretStr | None = Field(None, examples=["redis://localhost:6379/0", "redis://redis:6379/0"])
    "Redis URL"
    bot_token: SecretStr
    "Telegram bot token from @BotFather"
    bot_name: str = None
    "Desired bot name"
    bot_description: str = None
    "Bot description"
    bot_short_description: str = None
    "Bot short description"
    bot_commands: list[BotCommand] = None
    "Bot commands (displayed in telegram menu)"
    admins: list[int] = []
    "Admin' telegram IDs"

    @classmethod
    def from_yaml(cls, path: Path) -> "Settings":
        with open(path, encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f)

        return cls.model_validate(yaml_config)

    @classmethod
    def save_schema(cls, path: Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            schema = {"$schema": "http://json-schema.org/draft-07/schema#", **cls.model_json_schema()}
            yaml.dump(schema, f, sort_keys=False)
