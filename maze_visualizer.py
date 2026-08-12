import pygame
from mazegenerator import MazeGenerator

def display_maze(surface,our_seed):
    maze = MazeGenerator(seed=our_seed,size=(30,14))
    grid = maze.maze
    #pygame.init()
    #main_surface = pygame.display.set_mode((1920,1080))
    main_surface=surface
    color = (0, 0, 255)
    x = 40
    y = 120
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
    height = 0
    for row in grid:
        x = 60 #cell width
        width = 0
        for cell in row:
            if cell == 15 :
                color = (255,0,0)
            else:
                color = (0, 0, 255)
            if cell & 8: #w
                pygame.draw.line(main_surface, color, (x,y), (x, y+60))
            if cell & 1: #n
                pygame.draw.line(main_surface, color, (x,y), (x+60, y))
            if width == maze._width -1 :
                pygame.draw.line(main_surface, color, (x+60,y), (x+60, y+60))
            if height ==maze._height - 1:
                pygame.draw.line(main_surface, color, (x,y+60), (x+60, y+60))
            x+=60
            width += 1
        height += 1
        y+=60#cell height
