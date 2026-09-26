import os

from pydantic import BaseModel

PREFIX = "APP_"


class AppConfig(BaseModel):
    database_url: str
    debug: bool = False
    workers: int = 4


def load_config() -> AppConfig:
    data = {}
    for name in AppConfig.model_fields:
        key = PREFIX + name.upper()
        if key in os.environ:
            data[name] = os.environ[key]
    return AppConfig.model_validate(data)
