import pygame 
from sys import exit 
from mazegenerator import MazeGenerator
from maze_visualizer import display_maze
from player import Player
import random
import collision 
import var
from pacgums import place_gums,place_super_pacgums,draw_gums,remove_gums
from ghost import ghost, chase, cell_to_pixel,frightened
import parser

pygame.init()
screen = pygame.display.set_mode((1920,1080))
start_button_color=(255,255,255)
menu = True

player = Player(screen)
clock = pygame.time.Clock()

CELL_SIZE = 60
ORIGIN_X = 60
ORIGIN_Y = 120 
path1 = "right2.png"
path2 = "scared_1.png"

ghost_names = ["blinky", "clyde", "twinky", "inky"]
ghost_starts = [[90, 150], [1830, 150], [90, 930], [1830, 930]]

maze = None
gums = None
num_of_gums = 0
ghosts = []


def setup_level(level_seed):
    global maze, gums, num_of_gums, ghosts

    maze = MazeGenerator(seed=level_seed, size=(30, 14))
    gums, num_of_gums = place_gums(screen, maze)

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

    ghosts = []
    for i, name in enumerate(ghost_names):
        g = ghost(maze, name, None, list(ghost_starts[i]), speed=2, image_path=path1)
        g.behavior = chase(maze, g, player, CELL_SIZE, ORIGIN_X, ORIGIN_Y)
        ghosts.append(g)

    var.timer_start = pygame.time.get_ticks()


frightened_timeout = pygame.USEREVENT + 1
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

        if menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    print("start")
                    start_button_color = (255,0,0)
                    menu = False
                    var.level = 1
                    setup_level(parser.seed)
                if exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
 
    if menu :
        #title
        title = pygame.image.load('images/pacman_title.jpg').convert_alpha()
        title_rect = title.get_rect(center=(960,200))
        #font
        smallfont = pygame.font.SysFont('Corbel',35)

        #start button 
        start_button = smallfont.render('Start Game',True , start_button_color)
        start_button_rect = start_button.get_rect(center=(960,360))
        #high score
        high_score_button = smallfont.render('View Highscores',True, start_button_color)
        high_score_rect = high_score_button.get_rect(center =(960,400))
        # instructions
        instructions_button =smallfont.render('Instructions',True, start_button_color)
        instructions_rect = instructions_button.get_rect(center=(960,450))

        #exit
        exit_button = smallfont.render('Exit',True , (255,255,255))
        exit_button_rect = exit_button.get_rect(center = (960,500))

        screen.blit(exit_button,exit_button_rect)
        screen.blit(start_button,start_button_rect)
        screen.blit(title,title_rect)
        screen.blit(high_score_button ,high_score_rect)
        screen.blit(instructions_button ,instructions_rect)
        
    else:
        possible_moves=collision.get_possible_moves(maze.maze[var.col][var.row])
        screen.fill((0,0,0))
        lines= display_maze(maze,screen)
        gum_rects = draw_gums(screen,maze,gums,var.removed)
        place_super_pacgums(screen,maze)
        player.draw(screen)
        collided_ghost = player.move(maze,lines,possible_moves, ghosts)
        score= player.ate_gum(gum_rects)
        player.animate()

        hud_font = pygame.font.SysFont('Corbel', 30)
        lives_text = hud_font.render(f'Lives: {player.lives}', True, (255, 255, 255))
        score_text = hud_font.render(f'Score: {score}', True, (255, 255, 255))
        level_text = hud_font.render(f'Level: {var.level}', True, (255, 255, 255))
        now = pygame.time.get_ticks()
        remaining_ms = parser.level_max_time - (now - var.timer_start)
        remaining_sec = max(0, remaining_ms // 1000)
        timer_color = (255, 0, 0) if remaining_sec <= 10 else (255, 255, 255)
        timer_text = hud_font.render(f'Time: {remaining_sec}', True, timer_color)
        screen.blit(lives_text, (30, 40))
        screen.blit(score_text, (960 - score_text.get_width() // 2, 40))
        screen.blit(timer_text, (1920 - timer_text.get_width() - 30, 10))
        screen.blit(level_text, (1920 - level_text.get_width() - 30, 40))

        died = False
        if not collided_ghost:
            for g in ghosts:
                if not g.respawning and not g.edible:
                    dx = player.pos[0] - g.position[0]
                    dy = player.pos[1] - g.position[1]
                    if (dx**2 + dy**2)**0.5 < 60:
                        collided_ghost = g
                        break
        if collided_ghost:
            player.lives -= 1
            player.pos = [930, 510]
            var.row = 14
            var.col = 6
            for gg, ss in zip(ghosts, ghost_starts):
                gg.position = list(ss)
                gg.behavior.target_pixel = None
            died = True

        for g, start in zip(ghosts, ghost_starts):
            was_respawning = g.respawning
            g.update()

            if was_respawning and not g.respawning:
                g.position = list(start)
                g.image = pygame.image.load(path1)
                g.behavior = chase(maze, g, player, CELL_SIZE, ORIGIN_X, ORIGIN_Y)
                g.behavior.target_pixel = None
                g.draw(screen)
                continue

            if g.respawning:
                continue

            if var.edible and not g.edible:
                g.image = pygame.image.load(path2)
                g.make_edible()
                g.behavior = frightened(maze, g, player, CELL_SIZE, ORIGIN_X, ORIGIN_Y)
            if not var.edible and g.edible:
                g.image = pygame.image.load(path1)
                g.edible = False
                g.behavior = chase(maze, g, player, CELL_SIZE, ORIGIN_X, ORIGIN_Y)

            if not died:
                g.moving_algorithm()
            g.draw(screen)

            if not died and g.edible:
                dx = player.pos[0] - g.position[0]
                dy = player.pos[1] - g.position[1]
                if (dx**2 + dy**2)**0.5 < CELL_SIZE / 2:
                    g.edible = False
                    g.start_respawn()
                    player.score += parser.points_per_ghost

        if died:
            if player.lives <= 0:
                screen.fill((0,0,0))
                go_font = pygame.font.SysFont('Corbel', 60)
                go_text = go_font.render('Game Over', True, (255, 0, 0))
                go_rect = go_text.get_rect(center=(960, 400))
                screen.blit(go_text, go_rect)
                pygame.display.update()
                pygame.time.wait(3000)
                pygame.quit()
                exit()

        if num_of_gums + 4 == var.num_of_eaten_gums and not var.level_complete:
            var.level_complete = True
            player.score += 20
            screen.fill((0,0,0))
            win_font = pygame.font.SysFont('Corbel', 60)
            if var.level < var.MAX_LEVELS:
                win_text = win_font.render(f'Level {var.level} Complete!', True, (0, 255, 0))
            else:
                win_text = win_font.render('You Win the Game!', True, (0, 255, 0))
            win_rect = win_text.get_rect(center=(960, 400))
            screen.blit(win_text, win_rect)
            pygame.display.update()
            pygame.time.wait(3000)

            if var.level < var.MAX_LEVELS:
                var.level += 1
                setup_level(random.randint(1, 1000))
            else:
                pygame.quit()
                exit()

        if remaining_ms <= 0:
            screen.fill((0,0,0))
            go_font = pygame.font.SysFont('Corbel', 60)
            go_text = go_font.render('Time\'s Up! Game Over', True, (255, 0, 0))
            go_rect = go_text.get_rect(center=(960, 400))
            screen.blit(go_text, go_rect)
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            exit()


    pygame.display.update()
    clock.tick(40)
    
