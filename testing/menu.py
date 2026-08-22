import pygame
from sys import exit
from mazegenerator import MazeGenerator
from maze_visualizer import display_maze
from player import Player
from ghost import ghost, chase
import random

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
start_button_color = (255, 255, 255)
menu = True
seed = random.randint(1, 1000)
player = Player(screen)
clock = pygame.time.Clock()
maze = MazeGenerator(seed=seed, size=(30, 14))

# ⚠️ ADJUST these three to match how maze_visualizer.py actually draws cells
CELL_SIZE = 60
ORIGIN_X = 40
ORIGIN_Y = 120

# Spawn the ghost at the maze's entry cell, converted to pixels
entry_cell = maze.maze_entry
ghost_start = [ORIGIN_X + entry_cell[0] * CELL_SIZE,
               ORIGIN_Y + entry_cell[1] * CELL_SIZE]

blinky = ghost(maze, "blinky", None, ghost_start, speed=2)
# ⚠️ assumes `player` has a `.position` attribute ([x, y] pixel list) —
# rename if your Player class stores it differently (e.g. player.pos)
blinky.behavior = chase(maze, blinky, player, CELL_SIZE, ORIGIN_X, ORIGIN_Y)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    print("start")
                    start_button_color = (255, 0, 0)
                    menu = False
                if exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

    if menu:
        # title
        title = pygame.image.load('images/pacman_title.jpg').convert_alpha()
        title_rect = title.get_rect(center=(960, 200))
        # font
        smallfont = pygame.font.SysFont('Corbel', 35)
        # start button
        start_button = smallfont.render('Start Game', True, start_button_color)
        start_button_rect = start_button.get_rect(center=(960, 360))
        # high score
        high_score_button = smallfont.render('View Highscores', True, start_button_color)
        high_score_rect = high_score_button.get_rect(center=(960, 400))
        # instructions
        instructions_button = smallfont.render('Instructions', True, start_button_color)
        instructions_rect = instructions_button.get_rect(center=(960, 450))
        # exit
        exit_button = smallfont.render('Exit', True, (255, 255, 255))
        exit_button_rect = exit_button.get_rect(center=(960, 500))
        screen.blit(exit_button, exit_button_rect)
        screen.blit(start_button, start_button_rect)
        screen.blit(title, title_rect)
        screen.blit(high_score_button, high_score_rect)
        screen.blit(instructions_button, instructions_rect)

    else:
        screen.fill((0, 0, 0))
        lines = display_maze(maze, screen)
        player.draw(screen)
        player.move(maze, lines)
        player.animate()

        blinky.moving_algorithm()
        blinky.draw(screen)

    pygame.display.update()
    # clock.tick(80)
