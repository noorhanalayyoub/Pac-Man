import pygame
from mazegenerator import MazeGenerator

def display_maze(surface,our_seed):
    maze = MazeGenerator(seed=our_seed)
    grid = maze.maze
    #pygame.init()
    #main_surface = pygame.display.set_mode((1920,1080))
    main_surface=surface
    color = (0, 0, 255)
    x = 500
    y = 100
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
    height = 0
    for row in grid:
        x = 500
        width = 0
        for cell in row:
            if cell == 15 :
                color = (255,0,0)
            else:
                color = (0, 0, 255)
            if cell & 8: #w
                pygame.draw.line(main_surface, color, (x,y), (x, y+50))
            if cell & 1: #n
                pygame.draw.line(main_surface, color, (x,y), (x+50, y))
            if width == 14 :
                pygame.draw.line(main_surface, color, (x+50,y), (x+50, y+50))
            if height == 14:
                pygame.draw.line(main_surface, color, (x,y+50), (x+50, y+50))
            x+=50
            width += 1
        height += 1
        y+=50
