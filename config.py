import tomllib
from functools import cache
from pathlib import Path
from typing import Any

CONFIG_FILE = Path("config.toml")


@cache
def read_config() -> dict[str, Any]:
    if not CONFIG_FILE.exists():
        return {}

    content = CONFIG_FILE.read_text("utf-8")
    return tomllib.loads(content)


@cache
def get_config_section(section_name: str, default_value: Any = None) -> Any:
    config = read_config()

    if section_name in config:
        return config[section_name]

    if default_value is not None:
        return default_value

    return {}
