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


def warning(message: str) -> None:
    """Print a non-fatal configuration warning.

    Args:
        message: Warning description to print.
    """
    print(f"Configuration warning: {message}", file=sys.stderr)


def strip_comments(content: str) -> str:
    """Remove hash comments while preserving hashes inside JSON strings.

    Args:
        content: Raw JSON string that may contain # comments.

    Returns:
        Cleaned JSON string with comments removed.
    """
    result: list[str] = []
    in_string = False
    escaped = False
    skipping_comment = False
    for character in content:
        if skipping_comment:
            if character == "\n":
                skipping_comment = False
                result.append(character)
            continue
        if in_string:
            result.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
            result.append(character)
        elif character == "#":
            skipping_comment = True
        else:
            result.append(character)
    return "".join(result)


def object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build an object and warn when a key is repeated.

    Args:
        pairs: List of (key, value) tuples from JSON parsing.

    Returns:
        Dict of the last value for each key.
    """
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            warning(
                f"duplicate key '{key}'; the last value will be used"
            )
        result[key] = value
    return result


def read_json(path: str) -> dict[str, Any]:
    """Read a JSON object while allowing full-line comments.

    Args:
        path: Path to the JSON configuration file.

    Returns:
        Parsed configuration dict.

    Raises:
        ConfigError: On file not found, invalid JSON, or non-object root.
    """
    try:
        with open(path, "r", encoding="utf-8") as config_file:
            content = strip_comments(config_file.read())
        data: Any = json.loads(content, object_pairs_hook=object_pairs)
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


def integer_value(data: dict[str, Any], key: str) -> int:
    """Return a validated integer configuration value.

    Args:
        data: Parsed configuration dict.
        key: Configuration key to validate.

    Returns:
        Validated integer value, or the default if invalid/missing.
    """
    default = DEFAULTS[key]
    value = data.get(key, default)
    if key not in data:
        warning(f"missing '{key}', using {default}")
    if isinstance(value, bool) or not isinstance(value, int):
        warning(f"invalid '{key}', using {default}")
        return default
    minimum = 1000 if key == "level_max_time" else 0
    if key == "lives":
        minimum = 1
    if value < minimum:
        warning(f"'{key}' is too small, using {default}")
        return default
    return int(value)


def load_config(path: str) -> None:
    """Load and validate configuration values into this module.

    Args:
        path: Path to the JSON configuration file.

    Raises:
        ConfigError: On file or parsing errors.
    """
    global lives, points_per_pacgum, points_per_super_pacgum
    global points_per_ghost, seed, level_max_time

    data = read_json(path)
    lives = integer_value(data, "lives")
    points_per_pacgum = integer_value(data, "points_per_pacgum")
    points_per_super_pacgum = integer_value(data, "points_per_super_pacgum")
    points_per_ghost = integer_value(data, "points_per_ghost")
    seed = integer_value(data, "seed")
    level_max_time = integer_value(data, "level_max_time")


def load_from_args(arguments: Sequence[str]) -> None:
    """Load configuration from the required single command-line argument.

    Args:
        arguments: Command-line arguments (sys.argv).

    Raises:
        ConfigError: If not exactly one config file argument is provided.
    """
    if len(arguments) != 2:
        raise ConfigError("usage: python3 pac-man.py config.json")
    load_config(arguments[1])
