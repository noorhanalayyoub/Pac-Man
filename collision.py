import pygame

def get_possible_moves(cell):
    possible_moves={"w":0,"s":0,"e":0,"n":0}
    if not(cell & 8):
        possible_moves["w"]=1
    if not(cell & 4):
        possible_moves["s"]=1
    if not(cell & 2):
        possible_moves["e"]=1
    if not(cell & 1):
        possible_moves["n"]=1
    return possible_moves

def collide_line(rect,lines):
    for line in lines:
        clip_line = rect.clipline(line)
        if clip_line:
            print(clip_line)
            return True
def collide_rect(rect1,rect2):
    if rect1.x == rect2.x and rect1.y == rect2.y:
        return True
        print("collided w a gum")
    return False
