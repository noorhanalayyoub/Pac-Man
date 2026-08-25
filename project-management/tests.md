# Tests and Bugs

## Acceptance Tests

- Missing, malformed, or incomplete configuration gives a clear message.
- Invalid configuration values use their matching defaults.
- Missing or corrupt scores do not crash the game.
- Movement, ghosts, scoring, pause, cheat mode, victory, and game over work.
- Maze and asset failures are handled without a traceback.
- `flake8 .` and `mypy .` pass.

## Evidence Log

- Replaced forbidden `collidepoint` calls with manual bounds checks.
- Added type annotations and excluded only the untouched maze dependency.
- Fixed Flake8 formatting and unused names.
- Added configuration, score, maze, and asset error handling.

