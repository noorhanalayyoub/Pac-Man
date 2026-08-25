import sys
from types import TracebackType
import random


try:
    import pygame
    from mazegenerator import MazeGenerator
    from maze_visualizer import display_maze
    from player import Player
    import collision
    import var
    from pacgums import draw_gums, place_gums, place_super_pacgums
    from ghost import ghost, chase, frightened
    import parser
    from scoreboard import add_score, get_player_name, display_scoreboard
    from instructions import display_instructions
except ImportError as error:
    print(f"Error: missing game dependency: {error}", file=sys.stderr)
    sys.exit(1)


def handle_unexpected_error(
    error_type: type[BaseException],
    error: BaseException,
    traceback: TracebackType | None,
) -> None:
    """Report an uncaught application error without a traceback."""
    del error_type, traceback
    pygame.quit()
    print(f"Error: {error}", file=sys.stderr)


sys.excepthook = handle_unexpected_error


def load_image(path: str) -> pygame.Surface:
    """Load an image or terminate with a clear error message."""
    try:
        return pygame.image.load(path)
    except (OSError, pygame.error) as error:
        print(
            f"Error: unable to load asset '{path}': {error}",
            file=sys.stderr,
        )
        pygame.quit()
        raise SystemExit(1) from error


def validate_maze(generated_maze: MazeGenerator) -> None:
    """Reject malformed or unsolvable mazes before gameplay starts."""
    grid = generated_maze.maze
    if len(grid) != 14 or any(len(row) != 30 for row in grid):
        raise ValueError("generated maze has invalid dimensions")
    if any(
        not isinstance(cell, int) or cell < 0 or cell > 15
        for row in grid
        for cell in row
    ):
        raise ValueError("generated maze contains invalid cells")
    if not generated_maze.shortest_path:
        raise ValueError("generated maze has no valid path")


try:
    parser.load_from_args(sys.argv)
except parser.ConfigError as error:
    print(f"Error: {error}", file=sys.stderr)
    sys.exit(1)

try:
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("pacman")
except (OSError, pygame.error) as error:
    pygame.quit()
    print(f"Error: unable to start Pygame: {error}", file=sys.stderr)
    sys.exit(1)

start_button_color = (255, 255, 255)
menu = True

try:
    player = Player(screen)
    title_image = load_image("images/pacman_title.jpg").convert_alpha()
    clock = pygame.time.Clock()
except (OSError, pygame.error) as error:
    pygame.quit()
    print(f"Error: unable to load game assets: {error}", file=sys.stderr)
    sys.exit(1)

CELL_SIZE = 60
ORIGIN_X = 60
ORIGIN_Y = 120
path1 = "right2.png"
path2 = "scared_1.png"

ghost_names = ["blinky", "clyde", "twinky", "inky"]
ghost_starts = [[90, 150], [1830, 150], [90, 930], [1830, 930]]

maze: MazeGenerator
gums: list[list[int]]
num_of_gums: int = 0
ghosts: list[ghost] = []
resume_rect: pygame.Rect | None = None
quit_to_menu_rect: pygame.Rect | None = None
start_button_rect: pygame.Rect | None = None
high_score_rect: pygame.Rect | None = None
instructions_rect: pygame.Rect | None = None
exit_button_rect: pygame.Rect | None = None


class LevelSetupError(Exception):
    """Raised when a maze level cannot be prepared."""


def point_in_rect(rect: pygame.Rect, point: tuple[int, int]) -> bool:
    """Return whether a point is inside a rectangle."""
    x, y = point
    return bool(rect.left <= x < rect.right and rect.top <= y < rect.bottom)


def setup_level() -> None:
    global maze, gums, num_of_gums, ghosts

    try:
        if var.level ==1:
            new_maze = MazeGenerator(seed=parser.seed,size=(30,14))
        else:
            new_maze = MazeGenerator(size=(30, 14))
        validate_maze(new_maze)
        new_gums, new_num_of_gums = place_gums(screen, new_maze)
        new_ghosts: list[ghost] = []
        for i, name in enumerate(ghost_names):
            new_ghost = ghost(
                new_maze,
                name,
                None,
                list(ghost_starts[i]),
                speed=2,
                image_path=path1,
            )
            new_ghost.behavior = chase(
                new_maze, new_ghost, player, CELL_SIZE, ORIGIN_X, ORIGIN_Y
            )
            new_ghosts.append(new_ghost)
    except Exception as error:
        raise LevelSetupError(f"unable to prepare level: {error}") from error

    maze = new_maze
    gums = new_gums
    num_of_gums = new_num_of_gums
    ghosts = new_ghosts

    var.removed = []
    var.num_of_eaten_gums = 0
    var.super1 = 0
    var.super2 = 0
    var.super3 = 0
    var.super4 = 0
    var.edible = False
    var.row = 14
    var.col = 6
    var.level_complete = False

    player.pos = [930, 510]

    var.timer_start = pygame.time.get_ticks()


def try_setup_level() -> bool:
    """Prepare a level and report setup failures without a traceback."""
    try:
        setup_level()
    except LevelSetupError as error:
        print(f"Error: {error}", file=sys.stderr)
        return False
    return True


def complete_game(message: str) -> None:
    """Display the result and safely process the final score."""
    try:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont("Corbel", 60)
        result = font.render(message, True, (0, 255, 0))
        score_text = font.render(
            f"Final Score: {player.score}", True, (255, 255, 255)
        )
        screen.blit(result, result.get_rect(center=(960, 380)))
        screen.blit(score_text, score_text.get_rect(center=(960, 470)))
        pygame.display.update()
        pygame.time.wait(3000)
    except (OSError, pygame.error) as error:
        print(f"Error: unable to display result: {error}", file=sys.stderr)

    try:
        name = get_player_name(screen)
        add_score(name, player.score)
        display_scoreboard(screen)
    except (OSError, pygame.error, ValueError) as error:
        print(f"Error: unable to record final score: {error}", file=sys.stderr)


frightened_timeout = pygame.USEREVENT + 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
            and not menu
        ):
            var.paused = not var.paused
            if var.paused:
                var.pause_time = pygame.time.get_ticks()
            else:
                var.timer_start += pygame.time.get_ticks() - var.pause_time

        if var.paused:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if resume_rect and point_in_rect(resume_rect, mouse_pos):
                    var.paused = False
                if quit_to_menu_rect and point_in_rect(
                    quit_to_menu_rect, mouse_pos
                ):
                    var.paused = False
                    menu = True
            continue

        if event.type == pygame.KEYDOWN and not menu:
            if event.key == pygame.K_c:
                var.cheat_mode = not var.cheat_mode
            if (
                event.key == pygame.K_n
                and var.cheat_mode
                and var.level < var.MAX_LEVELS
            ):
                var.level += 1
                if not try_setup_level():
                    menu = True

        if menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect is not None and point_in_rect(
                    start_button_rect, mouse_pos
                ):
                    start_button_color = (255, 0, 0)
                    menu = False
                    var.level = 1
                    player.score = 0
                    player.lives = parser.lives
                    var.cheat_mode = False
                    if not try_setup_level():
                        menu = True
                if high_score_rect is not None and point_in_rect(
                    high_score_rect, mouse_pos
                ):
                    display_scoreboard(screen)
                    screen.fill((0, 0, 0))
                if instructions_rect is not None and point_in_rect(
                    instructions_rect, mouse_pos
                ):
                    display_instructions(screen)
                    screen.fill((0, 0, 0))
                if exit_button_rect is not None and point_in_rect(
                    exit_button_rect, mouse_pos
                ):
                    pygame.quit()
                    sys.exit(0)

    if menu:
        screen.fill((0, 0, 0))
        # title
        title = title_image
        title_rect = title.get_rect(center=(960, 200))
        # font
        smallfont = pygame.font.SysFont("Corbel", 35)

        # start button
        start_button = smallfont.render("Start Game", True, start_button_color)
        start_button_rect = start_button.get_rect(center=(960, 360))
        # high score
        high_score_button = smallfont.render(
            "View Highscores", True, start_button_color
        )
        high_score_rect = high_score_button.get_rect(center=(960, 400))
        # instructions
        instructions_button = smallfont.render(
            "Instructions", True, start_button_color
        )
        instructions_rect = instructions_button.get_rect(center=(960, 450))

        # exit
        exit_button = smallfont.render("Exit", True, (255, 255, 255))
        exit_button_rect = exit_button.get_rect(center=(960, 500))

        screen.blit(exit_button, exit_button_rect)
        screen.blit(start_button, start_button_rect)
        screen.blit(title, title_rect)
        screen.blit(high_score_button, high_score_rect)
        screen.blit(instructions_button, instructions_rect)

    else:
        if not var.paused:
            possible_moves = collision.get_possible_moves(
                maze.maze[var.col][var.row]
            )
        screen.fill((0, 0, 0))
        lines = display_maze(maze, screen)
        gum_rects = draw_gums(screen, maze, gums, var.removed)
        place_super_pacgums(screen, maze)
        player.draw(screen)
        if not var.paused:
            collided_ghost = player.move(maze, lines, possible_moves, ghosts)
            score = player.ate_gum(gum_rects)
            player.animate()
        else:
            score = player.score

        hud_font = pygame.font.SysFont("Corbel", 30)
        if var.cheat_mode:
            lives_text = hud_font.render("Lives: \u221e", True, (255, 255, 0))
        else:
            lives_text = hud_font.render(
                f"Lives: {player.lives}", True, (255, 255, 255)
            )
        score_text = hud_font.render(f"Score: {score}", True, (255, 255, 255))
        level_text = hud_font.render(
            f"Level: {var.level}", True, (255, 255, 255)
        )
        now = pygame.time.get_ticks()
        if var.paused:
            remaining_ms = parser.level_max_time - (
                var.pause_time - var.timer_start
            )
        else:
            remaining_ms = parser.level_max_time - (now - var.timer_start)
        remaining_sec = max(0, remaining_ms // 1000)
        if var.cheat_mode:
            timer_text = hud_font.render("Time: \u221e", True, (255, 255, 0))
        else:
            timer_color = (
                (255, 0, 0) if remaining_sec <= 10 else (255, 255, 255)
            )
            timer_text = hud_font.render(
                f"Time: {remaining_sec}", True, timer_color
            )
        screen.blit(lives_text, (30, 40))
        screen.blit(score_text, (960 - score_text.get_width() // 2, 40))
        screen.blit(timer_text, (1920 - timer_text.get_width() - 30, 10))
        screen.blit(level_text, (1920 - level_text.get_width() - 30, 40))
        if var.cheat_mode:
            cheat_text = hud_font.render("CHEAT MODE", True, (255, 255, 0))
            screen.blit(cheat_text, (30, 10))

        if not var.paused:
            died = False
            if not collided_ghost:
                for g in ghosts:
                    if not g.respawning and not g.edible:
                        dx = player.pos[0] - g.position[0]
                        dy = player.pos[1] - g.position[1]
                        if (dx**2 + dy**2) ** 0.5 < 60:
                            collided_ghost = g
                            break
            if collided_ghost:
                if not var.cheat_mode:
                    player.lives -= 1
                player.pos = [930, 510]
                var.row = 14
                var.col = 6
                for gg, ss in zip(ghosts, ghost_starts):
                    gg.position = list(ss)
                    if gg.behavior is not None:
                        gg.behavior.target_pixel = None
                died = True

            for g, start in zip(ghosts, ghost_starts):
                was_respawning = g.respawning
                g.update()

                if was_respawning and not g.respawning:
                    g.position = list(start)
                    g.image = load_image(path1)
                    behavior = chase(
                        maze, g, player, CELL_SIZE, ORIGIN_X, ORIGIN_Y
                    )
                    g.behavior = behavior
                    behavior.target_pixel = None
                    g.draw(screen)
                    continue

                if g.respawning:
                    continue

                if var.edible and not g.edible:
                    g.image = load_image(path2)
                    g.make_edible()
                    g.behavior = frightened(
                        maze, g, player, CELL_SIZE, ORIGIN_X, ORIGIN_Y
                    )
                if not var.edible and g.edible:
                    g.image = load_image(path1)
                    g.edible = False
                    g.behavior = chase(
                        maze, g, player, CELL_SIZE, ORIGIN_X, ORIGIN_Y
                    )

                if not died:
                    g.moving_algorithm()
                g.draw(screen)

                if not died and g.edible:
                    dx = player.pos[0] - g.position[0]
                    dy = player.pos[1] - g.position[1]
                    if (dx**2 + dy**2) ** 0.5 < CELL_SIZE / 2:
                        g.edible = False
                        g.start_respawn()
                        player.score += parser.points_per_ghost

            if died:
                if player.lives <= 0:
                    complete_game("Game Over")
                    menu = True
                    continue

            if (
                num_of_gums + 4 == var.num_of_eaten_gums
                and not var.level_complete
            ):
                var.level_complete = True
                player.score += 20
                if var.level < var.MAX_LEVELS:
                    screen.fill((0, 0, 0))
                    win_font = pygame.font.SysFont("Corbel", 60)
                    win_text = win_font.render(
                        f"Level {var.level} Complete!", True, (0, 255, 0)
                    )
                    win_rect = win_text.get_rect(center=(960, 400))
                    screen.blit(win_text, win_rect)
                    pygame.display.update()
                    pygame.time.wait(3000)
                    var.level += 1
                    if not try_setup_level(random.randint(1, 1000)):
                        menu = True
                else:
                    complete_game("You Win the Game!")
                    menu = True

            if remaining_ms <= 0 and not var.cheat_mode:
                complete_game("Time's Up! Game Over")
                menu = True
                continue
        else:
            for g in ghosts:
                g.draw(screen)

            overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            pause_font = pygame.font.SysFont("Corbel", 60)
            pause_title = pause_font.render("PAUSED", True, (255, 255, 255))
            screen.blit(pause_title, (960 - pause_title.get_width() // 2, 300))

            btn_font = pygame.font.SysFont("Corbel", 40)
            resume_btn = btn_font.render("Resume", True, (255, 255, 255))
            resume_rect = resume_btn.get_rect(center=(960, 420))
            screen.blit(resume_btn, resume_rect)

            quit_menu_btn = btn_font.render("Main Menu", True, (255, 255, 255))
            quit_to_menu_rect = quit_menu_btn.get_rect(center=(960, 500))
            screen.blit(quit_menu_btn, quit_to_menu_rect)

    pygame.display.update()
    clock.tick(40)
