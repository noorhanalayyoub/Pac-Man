# Agent Guide

- Before editing, read every file relevant to the change; for repository-wide changes, inspect all tracked source, configuration, and instruction files first.
- Keep build/edit granularity to no more than 50 changed lines in one response; use small, focused patches and verify each increment before continuing.
- Follow Google's Python Style Guide and applicable Google engineering practices: prefer clear names, small focused functions, explicit error handling, minimal duplication, and targeted verification.
- Run the game from the repository root with `python menu.py`; `config.json`, images, and `scores.json` are loaded through relative paths.
- Install the vendored maze dependency with `python -m pip install ./mazegenerator-2.1.0-py3-none-any.whl`; there is no requirements or test manifest.
- `menu.py` owns the Pygame loop, menus, levels, pause/cheat modes, and screen transitions; `player.py` owns movement and scoring; `ghost.py` owns AI and ghost lifecycle; `var.py` holds shared runtime state.
- `parser.py` reads `config.json` at import time, so run commands from the repository root and update `config.json` for configurable lives, points, seed, and level timeout.
- `setup_level()` resets maze, gum, ghost, and per-level state; score and lives must persist between levels and reset only when starting a new game from the main menu.
- Maze cells use wall bits `N=1`, `E=2`, `S=4`, `W=8`; a set bit means movement is blocked. Rendering and gameplay use 60px cells with origin `(60, 120)`.
- Player grid state uses `maze[var.col][var.row]` despite the names: `row` is the x index and `col` is the y index.
- When teleporting or resetting a ghost, clear `behavior.target_pixel` so it recalculates its path from the new position.
- Pause logic must preserve elapsed time by adjusting `var.timer_start`; cheat mode disables life loss and timeout, and `N` must not advance beyond `var.MAX_LEVELS` (currently 10).
- `scores.json` is persistent runtime data; scoreboard code keeps only the top 10 entries. Do not overwrite it during verification.
- `testing/` contains older manual prototypes, not an automated test suite.
- `SUBJECT.md` summarizes the Pacman Version 1.5 assignment requirements; consult it before making feature or packaging changes.
- Focused verification is `python -m py_compile <changed-file>.py`; interactive verification is `python menu.py` from the repository root.
