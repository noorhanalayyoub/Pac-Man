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

pygame.init()
screen = pygame.display.set_mode((1920,1080))
#screen.fill((255, 192, 203))
start_button_color=(255,255,255)
menu = True

seed = random.randint(1,1000)
player = Player(screen)
clock = pygame.time.Clock() 
maze = MazeGenerator(seed=seed,size=(30,14))
gums,num_of_gums = place_gums(screen,maze)

CELL_SIZE = 60
ORIGIN_X = 60
ORIGIN_Y = 120 
path1 = "right2.png"
path2 = "scared_1.png"

ghost_names = ["blinky", "clyde", "twinky", "inky"]
ghost_starts = [[90, 150], [1830, 150], [90, 930], [1830, 930]]

ghosts = []
for i, name in enumerate(ghost_names):
    g = ghost(maze, name, None, list(ghost_starts[i]), speed=2, image_path=path1)
    g.behavior = chase(maze, g, player, CELL_SIZE, ORIGIN_X, ORIGIN_Y)
    ghosts.append(g)


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
                if (dx**2 + dy**2)**0.5 < CELL_SIZE:
                    g.edible = False
                    g.start_respawn()

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

        print(score)
        if num_of_gums+20  == score:
            screen.fill((0,0,0))
            win_image = pygame.image.load('images/win.png').convert_alpha()
            win_rect = win_image.get_rect(center=(960,200))
            screen.blit(win_image,win_rect)
            print("win")


    print(f"pacman:{player.pos[0],player.pos[1]}\n")
    for g in ghosts:
        print(f"{g.name}:{g.position}\n")
    pygame.display.update()
    clock.tick(40)
    

