import pygame
from collections import deque
import random
import var
from typing import Protocol, Sequence
from mazegenerator import MazeGenerator


Cell = tuple[int, int]


class Behavior(Protocol):
    """Protocol for ghost movement behaviors."""

    target_pixel: list[int] | None

    def move(self) -> None: ...


class PlayerLike(Protocol):
    """Protocol for objects with a position attribute."""

    pos: list[float]


def pixel_to_cell(
    pos: Sequence[float], cell_size: int, origin_x: int, origin_y: int
) -> list[int]:
    """Convert pixel coordinates to grid cell indices.

    Args:
        pos: Pixel position [x, y].
        cell_size: Size of each grid cell in pixels.
        origin_x: X offset of the maze origin.
        origin_y: Y offset of the maze origin.

    Returns:
        Grid cell indices [col, row].
    """
    return [
        int((pos[0] - origin_x) // cell_size),
        int((pos[1] - origin_y) // cell_size),
    ]


def cell_to_pixel(
    cell: Cell,
    cell_size: int,
    origin_x: int,
    origin_y: int,
    image_size: tuple[int, int] = (0, 0),
) -> list[int]:
    """Convert grid cell coordinates to centered pixel position.

    Args:
        cell: Grid cell (x, y).
        cell_size: Size of each grid cell in pixels.
        origin_x: X offset of the maze origin.
        origin_y: Y offset of the maze origin.
        image_size: Optional sprite dimensions for centering.

    Returns:
        Pixel position [x, y] centered in the cell.
    """
    offset_x = (cell_size - image_size[0]) // 2
    offset_y = (cell_size - image_size[1]) // 2
    return [
        origin_x + cell[0] * cell_size + offset_x,
        origin_y + cell[1] * cell_size + offset_y,
    ]


def find_short_path(
    maze: MazeGenerator,
    ghost_coords: Sequence[int],
    pacman_coords: Sequence[int],
) -> str | bool:
    """Find the shortest path from ghost to pacman using BFS.

    Args:
        maze: The maze generator instance.
        ghost_coords: Ghost grid position [x, y].
        pacman_coords: Pacman grid position [x, y].

    Returns:
        String of direction letters (N/E/S/W) or False if unreachable.
    """
    moves = [(0, -1, 1, "N"), (1, 0, 2, "E"), (0, 1, 4, "S"), (-1, 0, 8, "W")]
    start = (ghost_coords[0], ghost_coords[1])
    goal = (pacman_coords[0], pacman_coords[1])
    prev: dict[Cell, tuple[Cell, str] | None] = {start: None}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break
        for dx, dy, code, letter in moves:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < maze._width
                and 0 <= ny < maze._height
                and (maze._maze[y][x] & code) == 0
                and (nx, ny) not in prev
            ):
                prev[(nx, ny)] = ((x, y), letter)
                queue.append((nx, ny))
    if goal not in prev:
        return False
    letters = []
    cur = goal
    previous = prev[cur]
    while previous is not None:
        parent, letter = previous
        letters.append(letter)
        cur = parent
        previous = prev[cur]
    return "".join(reversed(letters))


class chase:
    """Ghost behavior that chases the player using BFS pathfinding."""

    DIRECTION_DELTA = {
        "N": (0, -1),
        "S": (0, 1),
        "E": (1, 0),
        "W": (-1, 0),
    }

    def __init__(
        self,
        maze: MazeGenerator,
        ghost: "ghost",
        pacman: PlayerLike,
        cell_size: int,
        origin_x: int,
        origin_y: int,
    ) -> None:
        """Initialize chase behavior.

        Args:
            maze: The maze generator instance.
            ghost: The ghost entity this behavior controls.
            pacman: The player entity to chase.
            cell_size: Grid cell size in pixels.
            origin_x: X offset of the maze origin.
            origin_y: Y offset of the maze origin.
        """
        self.maze = maze
        self.ghost = ghost
        self.pacman = pacman
        self.cell_size = cell_size
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.target_cell: Cell | None = None
        self.target_pixel: list[int] | None = None

    def move(self) -> None:
        """Move one step toward the player using BFS shortest path."""
        if (
            self.target_pixel is None
            or self.ghost.position == self.target_pixel
        ):
            ghost_coords = pixel_to_cell(
                self.ghost.position,
                self.cell_size,
                self.origin_x,
                self.origin_y,
            )
            pacman_coords = pixel_to_cell(
                self.pacman.pos, self.cell_size, self.origin_x, self.origin_y
            )
            path = find_short_path(self.maze, ghost_coords, pacman_coords)

            if not isinstance(path, str) or not path:
                return

            direction = path[0]
            step_x, step_y = self.DIRECTION_DELTA[direction]
            self.target_cell = (
                ghost_coords[0] + step_x,
                ghost_coords[1] + step_y,
            )
            self.target_pixel = cell_to_pixel(
                self.target_cell,
                self.cell_size,
                self.origin_x,
                self.origin_y,
                self.ghost.image.get_size(),
            )

        pos = self.ghost.position
        tx, ty = self.target_pixel
        dx = tx - pos[0]
        dy = ty - pos[1]
        dist = (dx**2 + dy**2) ** 0.5

        if dist <= self.ghost.speed:
            pos[0], pos[1] = tx, ty
        else:
            pos[0] += self.ghost.speed * dx / dist
            pos[1] += self.ghost.speed * dy / dist


def possible_moves(
    maze: MazeGenerator, current_cell: Sequence[int]
) -> list[str]:
    """Return list of passable directions from the given cell.

    Args:
        maze: The maze generator instance.
        current_cell: Grid cell position [x, y].

    Returns:
        List of direction letters (N/E/S/W) that are passable.
    """
    x, y = int(current_cell[0]), int(current_cell[1])
    moves = []

    # CHANGED: the maze uses a set bit to mean there is a WALL.
    # Therefore a direction is possible when its bit is 0.
    cell = maze._maze[y][x]
    if (cell & 8) == 0:
        moves.append("W")
    if (cell & 4) == 0:
        moves.append("S")
    if (cell & 2) == 0:
        moves.append("E")
    if (cell & 1) == 0:
        moves.append("N")

    return moves


class frightened:
    """Ghost behavior that moves randomly when edible."""

    # CHANGED: frightened mode now uses the same cell-to-cell movement
    # system as chase, but chooses a random legal direction.
    def __init__(
        self,
        maze: MazeGenerator,
        ghost: "ghost",
        pacman: PlayerLike,
        cell_size: int,
        origin_x: int,
        origin_y: int,
    ) -> None:
        """Initialize frightened behavior.

        Args:
            maze: The maze generator instance.
            ghost: The ghost entity this behavior controls.
            pacman: The player entity to flee from.
            cell_size: Grid cell size in pixels.
            origin_x: X offset of the maze origin.
            origin_y: Y offset of the maze origin.
        """
        self.maze = maze
        self.ghost = ghost
        self.pacman = pacman
        self.cell_size = cell_size
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.target_pixel: list[int] | None = None

    def move(self) -> None:
        """Move one step in a random legal direction."""
        # CHANGED: choose a new random target cell when we reach the old one.
        if (
            self.target_pixel is None
            or self.ghost.position == self.target_pixel
        ):
            ghost_coords = pixel_to_cell(
                self.ghost.position,
                self.cell_size,
                self.origin_x,
                self.origin_y,
            )
            moves = possible_moves(self.maze, ghost_coords)

            if not moves:
                return

            direction = random.choice(moves)
            step_x, step_y = chase.DIRECTION_DELTA[direction]
            target_cell = (ghost_coords[0] + step_x, ghost_coords[1] + step_y)
            self.target_pixel = cell_to_pixel(
                target_cell,
                self.cell_size,
                self.origin_x,
                self.origin_y,
                self.ghost.image.get_size(),
            )

        # CHANGED: move toward the selected cell instead of jumping 60 pixels.
        pos = self.ghost.position
        tx, ty = self.target_pixel
        dx = tx - pos[0]
        dy = ty - pos[1]
        dist = (dx**2 + dy**2) ** 0.5

        if dist <= self.ghost.speed:
            pos[0], pos[1] = tx, ty
        else:
            pos[0] += self.ghost.speed * dx / dist
            pos[1] += self.ghost.speed * dy / dist


class ghost:
    """Ghost entity with AI behavior, edibility, and respawn logic.

    Attributes:
        speed: Movement speed in pixels per frame.
        name: Ghost identifier.
        position: Current pixel position [x, y].
        edible: Whether the ghost is currently edible.
        respawning: Whether the ghost is currently respawning.
    """

    def __init__(
        self,
        maze: MazeGenerator,
        name: str,
        behavior: Behavior | None,
        position: Sequence[float],
        speed: float = 2,
        image_path: str | None = None,
    ) -> None:
        """Initialize a ghost entity.

        Args:
            maze: The maze generator instance.
            name: Ghost identifier string.
            behavior: Initial movement behavior.
            position: Starting pixel position [x, y].
            speed: Movement speed in pixels per frame.
            image_path: Path to the ghost sprite image.

        Raises:
            ValueError: If image_path is None.
        """
        self.speed: float = speed
        self.name: str = name
        self.behavior: Behavior | None = behavior
        self.position: list[float] = list(position)
        if image_path is None:
            raise ValueError("A ghost image path is required")
        self.image = pygame.image.load(image_path)
        self.edible: bool = False
        self.edible_start: int = 0
        self.edible_duration: int = 20000
        self.respawning: bool = False
        self.respawn_start: int = 0
        self.respawn_duration: int = 5000

    def make_edible(self) -> None:
        """Mark the ghost as edible and start the edibility timer."""
        self.edible = True
        self.edible_start = pygame.time.get_ticks()

    def start_respawn(self) -> None:
        """Start the respawn timer after being eaten."""
        self.respawning = True
        self.respawn_start = pygame.time.get_ticks()

    def update(self) -> None:
        """Update respawn and edibility timers each frame."""
        if self.respawning:
            if (
                pygame.time.get_ticks() - self.respawn_start
                >= self.respawn_duration
            ):
                self.respawning = False
            return
        if self.edible:
            current_time = pygame.time.get_ticks()

            if current_time - self.edible_start >= self.edible_duration:
                var.edible = False

    def moving_algorithm(self) -> None:
        """Delegate movement to the current behavior."""
        if self.behavior is not None:
            self.behavior.move()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the ghost sprite onto the surface."""
        surface.blit(self.image, self.position)
