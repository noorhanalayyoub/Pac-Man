# Pacman: Ghosts! More Ghosts!

**Version:** 1.5  
**Language:** Python  
**Theme:** Gaming

## Summary

Recreate the famous arcade game Pac-Man with a playable, modular Python game.

## Intellectual Property Notice

The training-module content, including text, images, graphics, and other materials,
is protected by intellectual-property rights held by Association 42.

The content is for personal use only. Commercial use, reproduction, distribution,
modification, or public display requires prior written permission. Content must not
be altered in a way that harms its integrity.

Questions or authorization requests: `legal@42.fr`.

## AI Guidance

- Use AI to reduce repetitive work, not to replace understanding.
- Review, question, test, and peer-review AI-generated code and documentation.
- Use AI output only when the team understands it and can take responsibility for it.
- AI is context-limited; use peers as a quality checkpoint.

## General Rules

- Use Python 3.10 or later.
- Follow `flake8` standards.
- Handle errors gracefully with clear messages and no traceback during review.
- Use context managers for files and other resources where applicable.
- Add type hints where applicable and make functions pass `mypy`.
- Add PEP 257-compatible docstrings to functions and classes.
- Provide a `Makefile` with `install`, `run`, `debug`, `clean`, and `lint` rules.
- `lint` must run `flake8 .` and `mypy . --warn-return-any --warn-unused-ignores
  --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`.
- Include tests for functionality and edge cases; keep test programs out of submission
  if the subject requires that.
- Include a `.gitignore` for Python artifacts and prefer an isolated virtual environment.

## Mandatory Part

Build a complete Pac-Man game using object-oriented Python, a graphical library,
and a modular, reusable architecture. The game must support:

- A custom JSON configuration file, including game parameters.
- Robust error handling.
- Level generation through the assigned external A-Maze-ing package.
- A persistent highscore system stored on disk.
- A polished main menu, game view, game-over handling, and cheat mode.
- Packaging for demonstration on a public gaming platform such as Itch.io.

Required game loop:

```text
Main Menu -> Start Game -> Win or Lose -> Enter Name for Highscore -> Main Menu
```

## Usage

The final subject expects command-line execution with exactly one configuration
file argument:

```bash
python3 pac-man.py config.json
```

The filename may vary but must be JSON. Missing files, invalid values, and missing
keys must be handled cleanly with clear messages and no Python traceback.

## Configuration

- Configuration uses JSON and should support lines beginning with `#` as comments.
- Document configuration keys and provide safe defaults.
- Invalid or missing values must be clamped or replaced with safe defaults, logged
  clearly, and must not crash the game.
- Unknown keys must be ignored.
- Suggested keys include `highscore_filename`, level definitions, `width`, `height`,
  `lives`, `pacgum`, `points_per_pacgum`, `points_per_super_pacgum`,
  `points_per_ghost`, `seed`, and `level_max_time`.

## Maze Generator Integration

- Do not write a maze generator.
- Use the assigned A-Maze-ing package as-is; it may be reinstalled during review.
- Adapt the loader to the package interface instead of modifying the package.
- Set `PERFECT` to `False` for Pac-Man-compatible corridors.
- Handle maze-generation failures cleanly.

## Highscores

Implement a persistent highscore system. The implementation choice is up to the
team, but it must satisfy all of these requirements:

- Survive program restarts and load at game start.
- Save at game end and display from the main menu.
- Handle missing files, invalid formats, and file errors robustly.
- Accept names of at most 10 alphanumeric characters or spaces.
- Accept only non-negative integer scores.
- Keep and display the top 10 entries with names and scores.
- Prompt for a name on both victory and game over.

## Level Structure

- Generate mazes using the assigned A-Maze-ing package.
- Use a fixed seed for the first level, such as `42`; later levels may be random.
- Place pacgums through most corridors.
- Place four super-pacgums in the four maze corners.
- Place four ghosts, one in each corner.
- Start the player in the maze center.

The game must contain at least 10 levels. Each level has a time limit. Completing
a level advances to the next level while preserving score and remaining lives.
The game ends after all levels or when all lives are lost.

## Player

- Move through corridors only, without crossing walls.
- Support four directions: up, down, left, and right; arrow keys or WASD are valid.
- Start with three lives, or the configured value.
- Lose one life on contact with a non-edible ghost.
- Respawn in the maze center after losing a life.
- Win a level by eating all pacgums.
- Win the game by completing every level.
- Increase score for pacgums, super-pacgums, and edible ghosts.

## Ghosts

- Move autonomously through corridors.
- Chase the player while normal; the chase behavior may be distance-based or custom.
- Run away from the player while edible.
- Respawn in their corner after being eaten, such as after 5 or 10 seconds.

## Pacgums and Super-pacgums

- Pacgums are small dots placed in most corridors.
- Super-pacgums are larger dots in the four maze corners.
- Eating a pacgum adds `X` points.
- Eating a super-pacgum adds `Y` points and makes ghosts edible temporarily.
- Eating an edible ghost adds `Z` points.

## Cheat Mode

Cheat mode exists to make peer review easier. It should genuinely help reviewers
exercise game features. Suggested capabilities include:

- Invincibility: no life loss when touching ghosts.
- Level skip: immediately win or advance past the current level.
- Ghost freeze.
- Extra or endless lives.
- Increased player speed.
- Other useful review shortcuts.

## Scoring and Progression

The score increases, and never decreases, for:

- Eating a pacgum: `+X`.
- Eating a super-pacgum: `+Y`.
- Eating an edible ghost: `+Z`.

The player can pause and resume during gameplay. When the game ends, display the
final score, prompt for the player's name, save the highscore, and return to the
main menu. The time-limit behavior is a project choice, but it must be clear and
must not crash the game.

## User Interface

The main menu must provide:

- Start Game.
- View Highscores with the top 10 names and scores.
- Instructions showing controls and rules.
- Exit.

The in-game HUD must always show:

- Current score.
- Remaining lives.
- Current level.
- Remaining level time.

The pause menu must provide Resume and Return to Main Menu. The game-over screen
must show the final score and prompt for a highscore name. The victory screen must
show a congratulatory message, final score, and name prompt.

## Packaging

- Deliver a complete, functional build suitable for a free private/unlisted public
  platform release such as Itch.io.
- Include minimal in-package instructions for controls, options, and configuration.
- Keep all source and the packaging script/specification at repository root.
- Be prepared to regenerate the package during peer review.

## Project Management

Include a dedicated project-management directory with relevant evidence, such as:

- Timeline, Gantt, Kanban, or progress tracking.
- Project analysis and technical choices.
- Risk analysis and mitigations.
- Team responsibilities and decision process.
- Acceptance test plan and discovered/fixed bugs.
- Blocking points or conflict summaries.

## README Requirements

Provide an English `README.md` at repository root. Its first line must be italicized
and read:

```text
This activity has been created as part of the 42 curriculum by <login1>[, <login2>[, <login3>[...]]].
```

The README must include:

- Description of the activity and its goal.
- Installation, compilation, and execution instructions.
- Resources and references, including how AI was used and for which tasks.
- Configuration keys and default values.
- Highscore storage design and rationale.
- Maze-generation package integration.
- Technical implementation summary.
- General software architecture, modules, classes, and relationships.
- Project-management summary and a link to the project-management directory.

## Submission and Peer Review

- Submit only the repository contents for review.
- Verify filenames and required documents before submission.
- Be prepared to make a small requested modification during the defense.
- The requested modification should be understandable and feasible within minutes.

## Reference

This file is a repository-local Markdown reference for the Association 42 Pacman
Version 1.5 subject. The official subject and its intellectual-property terms take
precedence if this summary ever conflicts with them.
