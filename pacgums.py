import random 
import pygame
import var


l = [1,1,1,1,1,0]
#l = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
def place_gums(surface,maze):
    total_gums = []
    num_of_gums= 0
    grid = maze.maze
    x = 60
    y = 120
    r = 0
    for row in grid :
        gum_row=[]
        x = 60
        r+=1
        c=0
        for cell in row:
            c+=1 
            if (random.choice(l) and not cell == 15) and (not ( (r==1 and (c==1 or c==30)) or (r==14 and (c==1 or c==30))  )):
                gum_row.append(1)
                num_of_gums+=1
                    #pygame.draw.circle(surface,(255,255,255),(x+30,y+30),1)
            else:
                gum_row.append(0)
            x +=60
        total_gums.append(gum_row)
        y+=60
    return total_gums,num_of_gums

def draw_gums(surface,maze,gums,removed):
    gums_rects=[]
    grid = maze.maze
    x = 60
    y = 120
    for r,row in enumerate (grid) :
        x = 60
        for c,cell in enumerate (row):
            if gums[r][c]:
                gum=pygame.draw.circle(surface,(255,255,255),(x+30,y+30),1)
                if gum not in removed:
                    gums_rects.append(gum)
                else:
                    gum=pygame.draw.circle(surface,(0,0,0),(x+30,y+30),1)
                    #remove_gums(gums_rects)
            x +=60
        y+=60   
    return gums_rects

def remove_gums(gums_rects):
    if var.removed:
        gum = var.removed[0]
        gums_rects.remove(gum)
        
def place_super_pacgums(surface,maze):
    pass
