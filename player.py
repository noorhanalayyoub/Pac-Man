import pygame
import var
from pacgums import remove_gums
import parser
from ghost import ghost
from mazegenerator import MazeGenerator
from typing import Sequence


class Player:
    """Player entity controlled by the user.

    Attributes:
        lives: Remaining lives.
        pos: Current pixel position [x, y].
        score: Current score.
    """

    def __init__(self, surface: pygame.Surface) -> None:
        self.last = pygame.time.get_ticks()
        self.cooldown = 100
        self.move_last = pygame.time.get_ticks()
        self.move_cooldown = 200
        self.lives = parser.lives
        self.pos: list[float] = [930, 510]
        # -30 to be in the middle of the cell
        self.surface: pygame.Surface = surface
        self.score: int = 0
        self.rect: pygame.Rect | None = None

        pacman1 = pygame.image.load("images/pacman1.png")
        pacman2 = pygame.image.load("images/2.png")
        pacman3 = pygame.image.load("images/3.png")
        pacman4 = pygame.image.load("images/4.png")

        self.pacman: list[pygame.Surface] = [
            pacman1,
            pacman2,
            pacman3,
            pacman4,
        ]
        self.pacman_index: int = 0
        self.image: pygame.Surface = self.pacman[self.pacman_index]
        self.direction: str | None = None

    # self.rect = self.image.get_rect(topleft= (self.pos[0],self.pos[1]))

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the player sprite onto the surface.

        Args:
            surface: The pygame surface to draw on.
        """
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        surface.blit(self.image, self.rect)

    def check_ghost_collision(
        self, ghosts: Sequence[ghost] | None
    ) -> ghost | None:
        """Check for collision with non-edible, non-respawning ghosts.

        Args:
            ghosts: List of ghost entities to check against.

        Returns:
            The first colliding ghost, or None if no collision.
        """
        if not ghosts:
            return None
        for g in ghosts:
            if g.respawning or g.edible:
                continue
            dx = self.pos[0] - g.position[0]
            dy = self.pos[1] - g.position[1]
            if (dx**2 + dy**2) ** 0.5 < 60:
                return g
        return None

    def move(
        self,
        maze: MazeGenerator,
        lines: list,
        possible_moves: dict[str, int],
        ghosts: Sequence[ghost] | None = None,
    ) -> ghost | None:
        """Move the player one cell in the pressed direction if valid.

        Args:
            maze: The current maze generator instance.
            lines: Wall line segments for collision.
            possible_moves: Dict of passable directions (n/s/e/w).
            ghosts: Optional list of ghost entities.

        Returns:
            A ghost if collision occurred during movement, else None.
        """
        now = pygame.time.get_ticks()
        if now - self.move_last < self.move_cooldown:
            return None
        self.move_last = now
        keys = pygame.key.get_pressed()
        speed = 1
        if keys[pygame.K_UP] and possible_moves["n"]:
            for i in range(60):
                self.pos[1] -= speed
                self.rotate("up")
                hit = self.check_ghost_collision(ghosts)
                if hit:
                    return hit
            if (self.pos[1] - 150) % 60 == 0:
                var.col -= 1
        elif keys[pygame.K_DOWN] and possible_moves["s"]:
            for i in range(60):
                self.pos[1] += speed
                self.rotate("down")
                hit = self.check_ghost_collision(ghosts)
                if hit:
                    return hit
            if (self.pos[1] - 150) % 60 == 0:
                var.col += 1
        elif keys[pygame.K_RIGHT] and possible_moves["e"]:
            for i in range(60):
                self.pos[0] += speed
                self.rotate("right")
                hit = self.check_ghost_collision(ghosts)
                if hit:
                    return hit
            if (self.pos[0] - 90) % 60 == 0:
                var.row += 1
        elif keys[pygame.K_LEFT] and possible_moves["w"]:
            for i in range(60):
                self.pos[0] -= speed
                self.rotate("left")
                hit = self.check_ghost_collision(ghosts)
                if hit:
                    return hit
            if (self.pos[0] - 90) % 60 == 0:
                var.row -= 1
        return None

    def animate(self) -> None:
        """Cycle through animation frames on a cooldown."""
        now = pygame.time.get_ticks()
        # change image only if cooldown has been 0.1 seconds since last
        if now - self.last >= self.cooldown:
            self.last = now
            if self.pacman_index < 3:
                # pygame.time.wait(100)
                self.pacman_index += 1
            else:
                self.pacman_index = 0
            self.update_image()

    def rotate(self, goal_direction: str) -> None:
        """Rotate the sprite to face the given direction if changed.

        Args:
            goal_direction: Target direction (up, down, left, right).
        """
        if self.direction == goal_direction:
            return
        self.direction = goal_direction
        self.update_image()

    def update_image(self) -> None:
        """Update the displayed sprite based on direction and frame."""
        rotation = 0
        if self.direction == "up":
            rotation = 90
        elif self.direction == "down":
            rotation = 270
        elif self.direction == "right":
            rotation = 0
        elif self.direction == "left":
            rotation = 180
        self.image = pygame.transform.rotozoom(
            self.pacman[self.pacman_index], rotation, 2
        )

    def ate_gum(self, gum_rect: Sequence[pygame.Rect]) -> int:
        """Check for pacgum collisions, award points, and return score.

        Args:
            gum_rect: List of pacgum rects to check against.

        Returns:
            Updated score after eating.
        """
        for gum in gum_rect:
            # print(gum.x,gum.y)
            if self.pos[0] == gum.x + 1 and self.pos[1] == gum.y + 1:
                self.score += parser.points_per_pacgum
                var.num_of_eaten_gums += 1
                var.removed.append(gum)
        if self.ate_super():
            var.num_of_eaten_gums += 1
            self.score += parser.points_per_super_pacgum
        return self.score

    def ate_super(self) -> bool:
        """Check if the player ate a super-pacgum in any corner.

        Returns:
            True if a super-pacgum was eaten, False otherwise.
        """
        if self.pos[0] == 90 and self.pos[1] == 150 and not var.super1:
            var.super1 = 1
            remove_gums(self.surface, x=90, y=150)
            var.edible = True
            return True
        elif self.pos[0] == 1830 and self.pos[1] == 150 and not var.super2:
            var.super2 = 1
            remove_gums(self.surface, x=1830, y=150)
            var.edible = True
            return True
        elif self.pos[0] == 90 and self.pos[1] == 930 and not var.super3:
            var.super3 = 1
            remove_gums(self.surface, x=90, y=930)
            var.edible = True
            return True

        elif self.pos[0] == 1830 and self.pos[1] == 930 and not var.super4:
            var.super4 = 1
            remove_gums(self.surface, x=1830, y=930)
            var.edible = True
            return True

        return False
