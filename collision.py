import pygame


def get_possible_moves(cell: int) -> dict[str, int]:
    """Decode wall bits and return passable directions for a cell.

    Args:
        cell: Maze cell integer with wall bits (N=1, E=2, S=4, W=8).

    Returns:
        Dict with keys n/s/e/w and values 1 (passable) or 0 (wall).
    """
    possible_moves = {"w": 0, "s": 0, "e": 0, "n": 0}
    if not (cell & 8):
        possible_moves["w"] = 1
    if not (cell & 4):
        possible_moves["s"] = 1
    if not (cell & 2):
        possible_moves["e"] = 1
    if not (cell & 1):
        possible_moves["n"] = 1
    return possible_moves


def collide_line(
    rect: pygame.Rect, lines: list[tuple[tuple[int, int], tuple[int, int]]]
) -> bool:
    """Check if a rect intersects any line segment.

    Args:
        rect: The rectangle to test.
        lines: List of line segments as ((x1,y1), (x2,y2)) tuples.

    Returns:
        True if any line intersects the rect, False otherwise.
    """
    for line in lines:
        clip_line = rect.clipline(line)
        if clip_line:
            return True

    return False


def collide_rect(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """Check if two rects share the same top-left position.

    Args:
        rect1: First rectangle.
        rect2: Second rectangle.

    Returns:
        True if both rects have the same x and y, False otherwise.
    """
    if rect1.x == rect2.x and rect1.y == rect2.y:
        return True
    return False
