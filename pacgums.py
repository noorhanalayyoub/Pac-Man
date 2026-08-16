import random 
import pygame

l = [1,1,1,1,1,0]
def place_gums(surface,maze):
    total_gums = []
    grid = maze.maze
    x = 60
    y = 120
    for row in grid :
        gum_row=[]
        x = 60
        for cell in row:
            if random.choice(l) and not cell ==15:
                gum_row.append(1)
                #pygame.draw.circle(surface,(255,255,255),(x+30,y+30),1)
            else:
                gum_row.append(0)
            x +=60
        total_gums.append(gum_row)
        y+=60
    return total_gums

def draw_gums(surface,maze,gums):

    grid = maze.maze
    x = 60
    y = 120
    for r,row in enumerate (grid) :
        x = 60
        for c,cell in enumerate (row):
            if gums[r][c]:
                pygame.draw.circle(surface,(255,255,255),(x+30,y+30),1)
            x +=60
        y+=60   

    
