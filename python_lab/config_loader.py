import configparser
import os
from pathlib import Path


def _load_config() -> configparser.ConfigParser:
    config_file = os.getenv("APP_CONFIG_FILE", "config.ini")
    path = Path(config_file)
    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file '{config_file}' was not found. "
            "Create it from config.example.ini or set APP_CONFIG_FILE."
        )

    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(section: str, key: str, env_name: str | None = None) -> str:
    if env_name:
        env_value = os.getenv(env_name)
        if env_value is not None:
            return env_value

    config = _load_config()
    return config.get(section, key)
