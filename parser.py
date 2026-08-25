import json
import sys
from typing import Any, Sequence


class ConfigError(Exception):
    """Raised when the game configuration cannot be loaded."""


DEFAULTS: dict[str, int] = {
    "lives": 3,
    "points_per_pacgum": 1,
    "points_per_super_pacgum": 5,
    "points_per_ghost": 10,
    "seed": 42,
    "level_max_time": 90000,
}

lives: int = DEFAULTS["lives"]
points_per_pacgum: int = DEFAULTS["points_per_pacgum"]
points_per_super_pacgum: int = DEFAULTS["points_per_super_pacgum"]
points_per_ghost: int = DEFAULTS["points_per_ghost"]
seed: int = DEFAULTS["seed"]
level_max_time: int = DEFAULTS["level_max_time"]


def _warning(message: str) -> None:
    """Print a non-fatal configuration warning."""
    print(f"Configuration warning: {message}", file=sys.stderr)


def _read_json(path: str) -> dict[str, Any]:
    """Read a JSON object while allowing full-line comments."""
    try:
        with open(path, "r", encoding="utf-8") as config_file:
            content = "\n".join(
                line for line in config_file
                if not line.lstrip().startswith("#")
            )
        data: Any = json.loads(content)
    except FileNotFoundError as error:
        raise ConfigError(f"configuration file not found: {path}") from error
    except IsADirectoryError as error:
        raise ConfigError(
            f"configuration path is a directory: {path}"
        ) from error
    except (OSError, UnicodeError) as error:
        raise ConfigError(
            f"cannot read configuration file '{path}': {error}"
        ) from error
    except json.JSONDecodeError as error:
        raise ConfigError(
            f"invalid JSON in configuration file '{path}': {error.msg}"
        ) from error

    if not isinstance(data, dict):
        raise ConfigError("configuration root must be a JSON object")
    return data


def _integer_value(data: dict[str, Any], key: str) -> int:
    """Return a validated integer configuration value."""
    default = DEFAULTS[key]
    value = data.get(key, default)
    if key not in data:
        _warning(f"missing '{key}', using {default}")
    if isinstance(value, bool) or not isinstance(value, int):
        _warning(f"invalid '{key}', using {default}")
        return default
    minimum = 1000 if key == "level_max_time" else 0
    if key == "lives":
        minimum = 1
    if value < minimum:
        _warning(f"'{key}' is too small, using {default}")
        return default
    return int(value)


def load_config(path: str) -> None:
    """Load and validate configuration values into this module."""
    global lives, points_per_pacgum, points_per_super_pacgum
    global points_per_ghost, seed, level_max_time

    data = _read_json(path)
    lives = _integer_value(data, "lives")
    points_per_pacgum = _integer_value(data, "points_per_pacgum")
    points_per_super_pacgum = _integer_value(data, "points_per_super_pacgum")
    points_per_ghost = _integer_value(data, "points_per_ghost")
    seed = _integer_value(data, "seed")
    level_max_time = _integer_value(data, "level_max_time")


def load_from_args(arguments: Sequence[str]) -> None:
    """Load configuration from the required single command-line argument."""
    if len(arguments) != 2:
        raise ConfigError("usage: python3 pac-man.py config.json")
    load_config(arguments[1])
