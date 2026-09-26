from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")

    database_url: str
    debug: bool = False
    workers: int = 4


def load_config() -> AppConfig:
    return AppConfig()
