import os
from pathlib import Path

from dotenv import load_dotenv


class ConfigError(Exception):
    """Raised when required lab configuration is missing."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_properties(file_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not file_path.exists():
        return values

    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def load_db_config(
    db_name: str,
    env_prefix: str,
    required_keys: list[str],
    optional_defaults: dict[str, str] | None = None,
) -> dict[str, str]:
    optional_defaults = optional_defaults or {}
    root = _repo_root()
    load_dotenv(root / ".env")

    props_file = Path(
        os.getenv(f"{env_prefix}_PROPERTIES_FILE", str(root / "config" / f"{db_name}.properties"))
    )
    props = _read_properties(props_file)

    output: dict[str, str] = {}
    missing: list[str] = []

    for key in required_keys:
        env_key = f"{env_prefix}_{key.upper()}"
        value = os.getenv(env_key, props.get(key, "")).strip()
        if not value:
            missing.append(f"{key} (env: {env_key})")
        else:
            output[key] = value

    for key, default in optional_defaults.items():
        env_key = f"{env_prefix}_{key.upper()}"
        output[key] = os.getenv(env_key, props.get(key, default)).strip()

    if missing:
        raise ConfigError(
            f"Missing configuration for {db_name}: {', '.join(missing)}. "
            f"Set values in {props_file} or in environment variables. "
            "You can copy from .env.example and config/*.properties templates."
        )

    return output
