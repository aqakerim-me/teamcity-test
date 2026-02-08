import os
from pathlib import Path
from typing import Any


def _env_key(key: str) -> str:
    """Имя переменной окружения для ключа: admin.bearerToken -> TC_ADMIN_BEARERTOKEN"""
    return "TC_" + key.upper().replace(".", "_")


class Config:
    """Загрузка config.properties относительно корня проекта.
    Секреты можно передавать через переменные окружения (приоритет над файлом):
    - admin.bearerToken -> TC_ADMIN_BEARERTOKEN
    """

    # Определяем корень проекта по текущему файлу
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
    CONFIG_PATH = BASE_DIR / "resources" / "config.properties"

    _properties: dict[str, str] = {}

    @classmethod
    def _load_properties(cls) -> None:
        if cls._properties:
            return

        if not cls.CONFIG_PATH.is_file():
            raise FileNotFoundError(f"Config file not found at {cls.CONFIG_PATH}")

        with open(cls.CONFIG_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    cls._properties[key.strip()] = value.strip()

    @classmethod
    def get(cls, key: str, default_value: Any = None) -> Any:
        cls._load_properties()
        env_val = os.environ.get(_env_key(key))
        if env_val is not None and env_val != "":
            return env_val
        return cls._properties.get(key, default_value)