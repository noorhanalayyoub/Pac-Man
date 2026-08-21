import pygame
from collections import deque


def pixel_to_cell(pos, cell_size, origin_x, origin_y):
    return [(pos[0] - origin_x) // cell_size,
            (pos[1] - origin_y) // cell_size]


def cell_to_pixel(cell, cell_size, origin_x, origin_y):
    return [origin_x + cell[0] * cell_size,
            origin_y + cell[1] * cell_size]


def find_short_path(maze, ghost_coords, pacman_coords):
    # BFS: shortest ghost->pacman path in O(cells).
    moves = [(0, -1, 1, 'N'), (1, 0, 2, 'E'),
             (0, 1, 4, 'S'), (-1, 0, 8, 'W')]   # dx, dy, wall code, letter
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
    DIRECTION_DELTA = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}

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
        # arrived at (or has no) target -> pick the next cell via BFS
        if self.target_pixel is None or self.ghost.position == self.target_pixel:
            ghost_coords = pixel_to_cell(self.ghost.position, self.cell_size,
                                          self.origin_x, self.origin_y)
            pacman_coords = pixel_to_cell(self.pacman.position, self.cell_size,
                                           self.origin_x, self.origin_y)
            path = find_short_path(self.maze, ghost_coords, pacman_coords)

            if not path:  # no path found, or already on pacman's cell
                return

            direction = path[0]
            dx, dy = self.DIRECTION_DELTA[direction]
            self.target_cell = (ghost_coords[0] + dx, ghost_coords[1] + dy)
            self.target_pixel = cell_to_pixel(self.target_cell, self.cell_size,
                                               self.origin_x, self.origin_y)

        # step self.ghost.speed pixels toward target_pixel, without overshooting
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


class frightened:
    def move(self):
        pass


class ghost:
    def __init__(self, maze, name, behavior, position, speed=2, image_path=None):
        self.state = "chase"
        self.speed = speed
        self.name = name
        self.behavior = behavior
        self.position = list(position)  # mutable [x, y] pixel coords
        if image_path:
            self.image = pygame.image.load(right2.png)
        else:
            # fallback red circle so you can test without an image file
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (20, 20), 18)

    def moving_algorithm(self):
        self.behavior.move()

    def draw(self, surface):
        surface.blit(self.image, self.position)
