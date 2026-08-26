import pygame
from typing import Any


lives: int = 3
points_per_pacgum: int = 1
points_per_super_pacgum: int = 5
points_per_ghost: int = 10
seed: int = 42
level_max_time: int = 90000

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

maze: Any = None
gums: list[list[int]] = []
num_of_gums: int = 0
ghosts: list[Any] = []
