import pygame
import sys


def display_instructions(screen):
    font_title = pygame.font.SysFont("Corbel", 50)
    font_text = pygame.font.SysFont("Corbel", 30)
    font_hint = pygame.font.SysFont("Corbel", 25)

    instructions = [
        "Arrow Keys to move Pac-Man",
        "Eat all pacgums to complete each level",
        "Complete all levels to win the game",
        "Super pacgums make ghosts edible",
        "Eat edible ghosts for bonus points",
        "Avoid non-edible ghosts or lose a life",
        "Press Escape to pause the game",
    ]

    cheat_instructions = [
        "Press C to toggle Cheat Mode",
        "Cheat Mode: endless lives and no timer",
        "Press N to skip to the next level",
    ]

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False

        screen.fill((0, 0, 0))
        title = font_title.render("How To Play", True, (255, 215, 0))
        screen.blit(title, (960 - title.get_width() // 2, 60))

        y = 140
        for line in instructions:
            surf = font_text.render(line, True, (255, 255, 255))
            screen.blit(surf, (960 - surf.get_width() // 2, y))
            y += 45

        y += 20
        cheat_title = font_text.render("Cheat Mode", True, (255, 255, 0))
        screen.blit(cheat_title, (960 - cheat_title.get_width() // 2, y))
        y += 50
        for line in cheat_instructions:
            surf = font_text.render(line, True, (255, 255, 0))
            screen.blit(surf, (960 - surf.get_width() // 2, y))
            y += 45

        hint = font_hint.render("Press any key to return", True, (150, 150, 150))
        screen.blit(hint, (960 - hint.get_width() // 2, 700))

        pygame.display.update()
        pygame.time.Clock().tick(40)
