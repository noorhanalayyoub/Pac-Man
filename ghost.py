import pygame
from collections import deque
import random
import var

def pixel_to_cell(pos, cell_size, origin_x, origin_y):
    return [(pos[0] - origin_x) // cell_size,
            (pos[1] - origin_y) // cell_size]


def cell_to_pixel(cell, cell_size, origin_x, origin_y, image_size=(0, 0)):
    offset_x = (cell_size - image_size[0]) // 2
    offset_y = (cell_size - image_size[1]) // 2
    return [origin_x + cell[0] * cell_size + offset_x,
            origin_y + cell[1] * cell_size + offset_y]

def find_short_path(maze, ghost_coords, pacman_coords):
    moves = [(0, -1, 1, 'N'), (1, 0, 2, 'E'),
             (0, 1, 4, 'S'), (-1, 0, 8, 'W')]
    start = (ghost_coords[0], ghost_coords[1])
    goal = (pacman_coords[0], pacman_coords[1])
    prev = {start: None}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break
        for dx, dy, code, letter in moves:
            nx, ny = x + dx, y + dy
            if (0 <= nx < maze._width and 0 <= ny < maze._height
                    and (maze._maze[y][x] & code) == 0
                    and (nx, ny) not in prev):
                prev[(nx, ny)] = ((x, y), letter)
                queue.append((nx, ny))
    if goal not in prev:
        return False
    letters = []
    cur = goal
    while prev[cur] is not None:
        parent, letter = prev[cur]
        letters.append(letter)
        cur = parent
    return ''.join(reversed(letters))


class chase:
    DIRECTION_DELTA = {
        'N': (0, -1),
        'S': (0, 1),
        'E': (1, 0),
        'W': (-1, 0),
    }

    def __init__(self, maze, ghost, pacman, cell_size, origin_x, origin_y):
        self.maze = maze
        self.ghost = ghost
        self.pacman = pacman
        self.cell_size = cell_size
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.target_cell = None
        self.target_pixel = None

    def move(self):
        if self.target_pixel is None or self.ghost.position == self.target_pixel:
            ghost_coords = pixel_to_cell(self.ghost.position, self.cell_size,
                                          self.origin_x, self.origin_y)
            pacman_coords = pixel_to_cell(self.pacman.pos, self.cell_size,
                                           self.origin_x, self.origin_y)
            path = find_short_path(self.maze, ghost_coords, pacman_coords)

            if not path:
                return

            direction = path[0]
            dx, dy = self.DIRECTION_DELTA[direction]
            self.target_cell = (ghost_coords[0] + dx, ghost_coords[1] + dy)
            self.target_pixel = cell_to_pixel(self.target_cell, self.cell_size,
                                               self.origin_x, self.origin_y, self.ghost.image.get_size())

        pos = self.ghost.position
        tx, ty = self.target_pixel
        dx = tx - pos[0]
        dy = ty - pos[1]
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist <= self.ghost.speed:
            pos[0], pos[1] = tx, ty
        else:
            pos[0] += self.ghost.speed * dx / dist
            pos[1] += self.ghost.speed * dy / dist


def possible_moves(maze, current_cell):
    x, y = int(current_cell[0]), int(current_cell[1])
    moves = []

    # CHANGED: the maze uses a set bit to mean there is a WALL.
    # Therefore a direction is possible when its bit is 0.
    cell = maze._maze[y][x]
    if (cell & 8) == 0:
        moves.append('W')
    if (cell & 4) == 0:
        moves.append('S')
    if (cell & 2) == 0:
        moves.append('E')
    if (cell & 1) == 0:
        moves.append('N')

    return moves

class frightened:
    # CHANGED: frightened mode now uses the same cell-to-cell movement
    # system as chase, but chooses a random legal direction.
    def __init__(self, maze, ghost, pacman, cell_size, origin_x, origin_y):
        self.maze = maze
        self.ghost = ghost
        self.pacman = pacman
        self.cell_size = cell_size
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.target_pixel = None


    def move(self):
        # CHANGED: choose a new random target cell when we reach the old one.
        if self.target_pixel is None or self.ghost.position == self.target_pixel:
            ghost_coords = pixel_to_cell(
                self.ghost.position, self.cell_size, self.origin_x, self.origin_y
            )
            moves = possible_moves(self.maze, ghost_coords)

            if not moves:
                return

            direction = random.choice(moves)
            dx, dy = chase.DIRECTION_DELTA[direction]
            target_cell = (ghost_coords[0] + dx, ghost_coords[1] + dy)
            self.target_pixel = cell_to_pixel(
                target_cell, self.cell_size, self.origin_x, self.origin_y,
                self.ghost.image.get_size()
            )

        # CHANGED: move toward the selected cell instead of jumping 60 pixels.
        pos = self.ghost.position
        tx, ty = self.target_pixel
        dx = tx - pos[0]
        dy = ty - pos[1]
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist <= self.ghost.speed:
            pos[0], pos[1] = tx, ty
        else:
            pos[0] += self.ghost.speed * dx / dist
            pos[1] += self.ghost.speed * dy / dist


class ghost:
    def __init__(self, maze, name, behavior, position, speed=2, image_path=None): 
        self.speed = speed
        self.name = name
        self.behavior = behavior
        self.position = list(position)
        self.image = pygame.image.load(image_path) 
        self.edible = False
        self.edible_start = 0
        self.edible_duration = 2000

    def make_edible(self):
        self.edible = True
        self.edible_start = pygame.time.get_ticks()

    def update(self):
        if self.edible:
            current_time = pygame.time.get_ticks()

            if current_time - self.edible_start >= self.edible_duration:
                #self.edible = False
                var.edible = False
    
    def moving_algorithm(self):
        self.behavior.move()

    def draw(self, surface):
        surface.blit(self.image, self.position)
