import pygame
from mazegenerator import MazeGenerator

def display_maze(maze,surface):
    lines = []
    #maze = MazeGenerator(seed=our_seed,size=(30,14))
    grid = maze.maze
    #pygame.init()
    #main_surface = pygame.display.set_mode((1920,1080))
    main_surface=surface
    color = (0, 0, 255)
    x = 60
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
                tuple1 = tuple((x,y))
                tuple2 = tuple ((x, y+60))
                lines.append(tuple((tuple1, tuple2)))
            if cell & 1: #n
                pygame.draw.line(main_surface, color, (x,y), (x+60, y))
                tuple1 = tuple((x,y))
                tuple2 = tuple ((x+60, y))
                lines.append(tuple((tuple1, tuple2)))
            if width == maze._width -1 :
                pygame.draw.line(main_surface, color, (x+60,y), (x+60, y+60))
                tuple1 = tuple((x+60,y))
                tuple2 = tuple ((x+60, y+60))
                lines.append(tuple((tuple1, tuple2)))            
            if height ==maze._height - 1:
                pygame.draw.line(main_surface, color, (x,y+60), (x+60, y+60)) 
                tuple1 = tuple((x,y+60))
                tuple2 = tuple ((x+60, y+60))
                lines.append(tuple((tuple1, tuple2)))     
            x += 60
            width += 1
        height += 1
        y += 60 #cell height
    return lines
