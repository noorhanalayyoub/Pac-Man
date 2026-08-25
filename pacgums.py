import random
import pygame
import var
from mazegenerator import MazeGenerator


GUM_CHANCE = [1, 1, 1, 1, 1, 0]


def place_gums(
    surface: pygame.Surface, maze: MazeGenerator
) -> tuple[list[list[int]], int]:
    """Randomly place pacgums in maze corridors.

    Args:
        surface: The pygame surface (unused, kept for API consistency).
        maze: The maze generator instance.

    Returns:
        Tuple of (2D gum grid, total gum count).
    """
    total_gums = []
    num_of_gums = 0
    grid = maze.maze
    x = 60
    y = 120
    r = 0
    for row in grid:
        gum_row: list[int] = []
        x = 60
        r += 1
        c = 0
        for cell in row:
            c += 1
            if (random.choice(GUM_CHANCE) and not cell == 15) and (
                not (
                    (r == 1 and (c == 1 or c == 30))
                    or (r == 14 and (c == 1 or c == 30))
                    or (r == 7 and c == 15)
                )
            ):
                gum_row.append(1)
                num_of_gums += 1
                # pygame.draw.circle(surface,(255,255,255),(x+30,y+30),1)
            else:
                gum_row.append(0)
            x += 60
        total_gums.append(gum_row)
        y += 60
    return total_gums, num_of_gums


def draw_gums(
    surface: pygame.Surface,
    maze: MazeGenerator,
    gums: list[list[int]],
    removed: list[pygame.Rect],
) -> list[pygame.Rect]:
    """Render pacgums on the surface and return their rects for collision.

    Args:
        surface: The pygame surface to draw on.
        maze: The maze generator instance.
        gums: 2D grid indicating gum placement.
        removed: List of already-eaten gum rects to skip.

    Returns:
        List of pacgum rects for collision detection.
    """
    gums_rects = []
    grid = maze.maze
    x = 60
    y = 120
    for r, row in enumerate(grid):
        x = 60
        for c, cell in enumerate(row):
            if gums[r][c]:
                gum = pygame.draw.circle(
                    surface, (255, 255, 255), (x + 30, y + 30), 1
                )
                if gum not in removed:
                    gums_rects.append(gum)
                else:
                    gum = pygame.draw.circle(
                        surface, (0, 0, 0), (x + 30, y + 30), 1
                    )
                    # remove_gums(gums_rects)
            x += 60
        y += 60
    return gums_rects


def remove_gums(surface: pygame.Surface, x: int, y: int) -> None:
    """Erase a super-pacgum visually by drawing a black circle over it.

    Args:
        surface: The pygame surface to draw on.
        x: X pixel coordinate of the super-pacgum.
        y: Y pixel coordinate of the super-pacgum.
    """
    # if var.removed:
    # gum = var.removed[0]
    # gums_rects.remove(gum)
    pygame.draw.circle(surface, (0, 0, 0), (x, y), 3)


def place_super_pacgums(surface: pygame.Surface, maze: MazeGenerator) -> None:
    """Draw four super-pacgums in the maze corners if not yet eaten.

    Args:
        surface: The pygame surface to draw on.
        maze: The maze generator instance.
    """
    grid = maze.maze
    x = 60
    y = 120
    r = 0
    for row in grid:
        x = 60
        r += 1
        c = 0
        for cell in row:
            c += 1
            if (
                r == 1
                and (
                    (c == 1 and not var.super1) or (c == 30 and not var.super2)
                )
            ) or (
                r == 14
                and (
                    (c == 1 and not var.super3) or (c == 30 and not var.super4)
                )
            ):
                pygame.draw.circle(
                    surface, (255, 255, 255), (x + 30, y + 30), 3
                )
            x += 60
        y += 60
