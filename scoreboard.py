import pygame
import json
import os
import sys
import tempfile
from typing import Any, TypedDict


class ScoreEntry(TypedDict):
    name: str
    score: int


SCORES_FILE: str = "scores.json"
MAX_ENTRIES: int = 10


def _warning(message: str) -> None:
    """Print a non-fatal score file warning."""
    print(f"Scoreboard warning: {message}", file=sys.stderr)


def _valid_entry(name: Any, score: Any) -> bool:
    """Return whether raw score data satisfies scoreboard rules."""
    return (
        isinstance(name, str)
        and 1 <= len(name) <= 10
        and all(character.isalnum() or character == " " for character in name)
        and isinstance(score, int)
        and not isinstance(score, bool)
        and score >= 0
    )


def load_scores() -> list[ScoreEntry]:
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as file:
            data: Any = json.load(file)
    except FileNotFoundError:
        return []
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        _warning(f"cannot read '{SCORES_FILE}': {error}")
        return []
    if not isinstance(data, list):
        _warning(f"'{SCORES_FILE}' must contain a JSON list")
        return []
    scores: list[ScoreEntry] = []
    for entry in data:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        score = entry.get("score")
        if _valid_entry(name, score):
            assert isinstance(name, str)
            assert isinstance(score, int)
            scores.append({"name": name, "score": score})
    scores.sort(key=lambda entry: entry["score"], reverse=True)
    return scores[:MAX_ENTRIES]


def save_scores(scores: list[ScoreEntry]) -> bool:
    """Atomically save scores and report filesystem failures."""
    temporary_path: str | None = None
    directory = os.path.dirname(os.path.abspath(SCORES_FILE))
    try:
        descriptor, temporary_path = tempfile.mkstemp(
            prefix=".scores-", dir=directory, text=True
        )
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            json.dump(scores[:MAX_ENTRIES], file, indent=2)
        os.replace(temporary_path, SCORES_FILE)
    except (OSError, TypeError, ValueError) as error:
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except OSError:
                pass
        _warning(f"cannot save '{SCORES_FILE}': {error}")
        return False
    return True


def add_score(name: str, score: int) -> list[ScoreEntry]:
    scores = load_scores()
    if not _valid_entry(name, score):
        _warning("rejected invalid score entry")
        return scores
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda e: e["score"], reverse=True)
    scores = scores[:MAX_ENTRIES]
    save_scores(scores)
    return scores


def get_player_name(screen: pygame.Surface) -> str:
    font = pygame.font.SysFont("Corbel", 40)
    small_font = pygame.font.SysFont("Corbel", 30)
    name = ""
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if (
                        len(name) < 10
                        and (event.unicode.isalnum() or event.unicode == " ")
                    ):
                        name += event.unicode

        screen.fill((0, 0, 0))
        prompt = font.render("Enter your name:", True, (255, 255, 255))
        screen.blit(prompt, (960 - prompt.get_width() // 2, 350))

        cursor = "|" if pygame.time.get_ticks() % 1000 < 500 else ""
        name_surface = font.render(name + cursor, True, (255, 255, 0))
        name_rect = name_surface.get_rect(center=(960, 420))
        pygame.draw.rect(screen, (50, 50, 50), name_rect.inflate(20, 10))
        screen.blit(name_surface, name_rect)

        hint = small_font.render(
            "Press Enter to confirm", True, (150, 150, 150)
        )
        screen.blit(hint, (960 - hint.get_width() // 2, 470))

        pygame.display.update()
        pygame.time.Clock().tick(40)

    return name.strip()


def display_scoreboard(screen: pygame.Surface) -> None:
    font_title = pygame.font.SysFont("Corbel", 50)
    font_entry = pygame.font.SysFont("Corbel", 30)
    font_hint = pygame.font.SysFont("Corbel", 25)

    scores = load_scores()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False

        screen.fill((0, 0, 0))
        title = font_title.render("SCOREBOARD", True, (255, 215, 0))
        screen.blit(title, (960 - title.get_width() // 2, 80))

        y = 160
        for i, entry in enumerate(scores):
            rank_text = f"{i + 1}."
            name_text = entry["name"]
            score_text = str(entry["score"])

            rank_surf = font_entry.render(rank_text, True, (255, 255, 255))
            name_surf = font_entry.render(name_text, True, (255, 255, 255))
            score_surf = font_entry.render(score_text, True, (255, 255, 0))

            screen.blit(rank_surf, (700, y))
            screen.blit(name_surf, (750, y))
            screen.blit(score_surf, (1100, y))
            y += 40

        if not scores:
            no_scores = font_entry.render(
                "No scores yet!", True, (150, 150, 150)
            )
            screen.blit(no_scores, (960 - no_scores.get_width() // 2, 250))

        hint = font_hint.render(
            "Press any key to continue", True, (150, 150, 150)
        )
        screen.blit(hint, (960 - hint.get_width() // 2, 700))

        pygame.display.update()
        pygame.time.Clock().tick(40)
