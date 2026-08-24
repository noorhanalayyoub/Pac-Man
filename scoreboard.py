import pygame
import json
import os

SCORES_FILE = "scores.json"
MAX_ENTRIES = 10


def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r") as f:
        return json.load(f)


def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)


def add_score(name, score):
    scores = load_scores()
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda e: e["score"], reverse=True)
    scores = scores[:MAX_ENTRIES]
    save_scores(scores)
    return scores


def get_player_name(screen):
    font = pygame.font.SysFont("Corbel", 40)
    small_font = pygame.font.SysFont("Corbel", 30)
    name = ""
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 20 and event.unicode.isprintable():
                        name += event.unicode

        screen.fill((0, 0, 0))
        prompt = font.render("Enter your name:", True, (255, 255, 255))
        screen.blit(prompt, (960 - prompt.get_width() // 2, 350))

        cursor = "|" if pygame.time.get_ticks() % 1000 < 500 else ""
        name_surface = font.render(name + cursor, True, (255, 255, 0))
        name_rect = name_surface.get_rect(center=(960, 420))
        pygame.draw.rect(screen, (50, 50, 50), name_rect.inflate(20, 10))
        screen.blit(name_surface, name_rect)

        hint = small_font.render("Press Enter to confirm", True, (150, 150, 150))
        screen.blit(hint, (960 - hint.get_width() // 2, 470))

        pygame.display.update()
        pygame.time.Clock().tick(40)

    return name.strip()


def display_scoreboard(screen):
    font_title = pygame.font.SysFont("Corbel", 50)
    font_entry = pygame.font.SysFont("Corbel", 30)
    font_hint = pygame.font.SysFont("Corbel", 25)

    scores = load_scores()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False

        screen.fill((0, 0, 0))
        title = font_title.render("SCOREBOARD", True, (255, 215, 0))
        screen.blit(title, (960 - title.get_width() // 2, 80))

        y = 160
        for i, entry in enumerate(scores):
            rank_text = f"{i+1}."
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
            no_scores = font_entry.render("No scores yet!", True, (150, 150, 150))
            screen.blit(no_scores, (960 - no_scores.get_width() // 2, 250))

        hint = font_hint.render("Press any key to continue", True, (150, 150, 150))
        screen.blit(hint, (960 - hint.get_width() // 2, 700))

        pygame.display.update()
        pygame.time.Clock().tick(40)
