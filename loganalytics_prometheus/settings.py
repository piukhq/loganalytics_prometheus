import logging

from pydantic import BaseSettings
from pythonjsonlogger import jsonlogger

log = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter())
log.addHandler(handler)


class Settings(BaseSettings):
    workspace_id: str = "eed2b98d-3396-4972-be3e-3e744532f7cd"
    query_interval_minutes: int = 30


settings = Settings()
