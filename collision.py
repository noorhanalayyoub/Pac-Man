import pygame


def collide_line(rect,lines):
    for line in lines:
        clip_line = rect.clipline(line)
        if clip_line:
            print("collide")
