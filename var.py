import pygame


row: int = 14
col: int = 6
removed: list[pygame.Rect] = []
super1: int = 0
super2: int = 0
super3: int = 0
super4: int = 0
num_of_eaten_gums: int = 0
# cell = maze.maze[col][row]
edible: bool = False
level: int = 1
timer_start: int = 0
level_complete: bool = False
MAX_LEVELS: int = 10
paused: bool = False
pause_time: int = 0
cheat_mode: bool = False
