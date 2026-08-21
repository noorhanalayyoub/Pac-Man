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
GHOST_IMAGE = pygame.image.load("right2.png")  # same image ghost.__init__ loads
entry_cell = maze.maze_entry
ghost_start = cell_to_pixel(entry_cell, CELL_SIZE, ORIGIN_X, ORIGIN_Y, GHOST_IMAGE.get_size())
blinky = ghost(maze, "blinky", None, ghost_start,speed=2,image_path=path1)
blinky.behavior = chase(maze, blinky, player, CELL_SIZE, ORIGIN_X, ORIGIN_Y)


frightened_timeout = pygame.USEREVENT + 1
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        #if event.type == frightened_timeout:
         #    pygame.time.set_timer(frightened_timeout, 20000)
          #   blinky.behavior =(maze, blinky, player, CELL_SIZE, ORIGIN_X, ORIGIN_Y)

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
        player.move(maze,lines,possible_moves)
        score= player.ate_gum(gum_rects)
        player.animate()

        #blinky.moving_algorithm()
        #blinky.draw(screen)
        blinky.update()
        if var.edible and not blinky.edible:
            blinky.image=pygame.image.load(path2)
            blinky.make_edible()
            blinky.behavior=frightened(maze,blinky,player,CELL_SIZE,ORIGIN_X,ORIGIN_Y)
        if not var.edible and blinky.edible:
            blinky.image= pygame.image.load(path1)
            blinky.edible = False
            blinky.behavior = chase(maze, blinky, player,
                                    CELL_SIZE, ORIGIN_X, ORIGIN_Y)

        blinky.moving_algorithm()
        blinky.draw(screen)
        print(score)
        if num_of_gums+20  == score:
            screen.fill((0,0,0))
            win_image = pygame.image.load('images/win.png').convert_alpha()
            win_rect = win_image.get_rect(center=(960,200))
            screen.blit(win_image,win_rect)
            print("win")

    pygame.display.update()
    clock.tick(40)
    

