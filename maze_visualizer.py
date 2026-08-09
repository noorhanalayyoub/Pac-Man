import pygame
from mazegenerator import MazeGenerator

def display_maze():
    maze = MazeGenerator()
    grid = maze.maze
    pygame.init()
    main_surface = pygame.display.set_mode((1920,1080))

    Blue = (0, 0, 255)
    while True:
        x = 0
        y = 0
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
        height = 0
        for row in grid:
            x = 0
            width = 0
            for cell in row:
                if cell & 8: #w
                    pygame.draw.line(main_surface, Blue, (x,y), (x, y+10))
                if cell & 1: #n
                    pygame.draw.line(main_surface, Blue, (x,y), (x+10, y))
                if width == 14 :
                    pygame.draw.line(main_surface, Blue, (x+10,y), (x+10, y+10))
                if height == 14:
                    pygame.draw.line(main_surface, Blue, (x,y+10), (x+10, y+10))
                x+=10
                width += 1
            height += 1
            y+=10
   
        pygame.display.update()

display_maze()
