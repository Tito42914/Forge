from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="FORGE_",
        extra="ignore",
    )

    app_name: str = "Forge"
    app_version: str = "0.1.0"
    environment: Literal["development", "testing", "production"] = "development"
