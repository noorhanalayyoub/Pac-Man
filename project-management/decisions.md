# Decisions

| Area | Decision |
| --- | --- |
| Language | Python 3.10+ |
| Graphics | Pygame |
| Maze | Assigned wheel, unchanged |
| Configuration | JSON with validated defaults |
| Scores | Persistent validated top ten in `scores.json` |
| Packaging | `pyproject.toml` source and wheel archives |

## Responsibilities

- `mjbarin`: main loop, player, collision, and pacgums.
- `nalayyou`: ghosts, configuration, and highscores.
- Both: documentation, packaging, review, and acceptance testing.


