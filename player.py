import pygame
from collision import collide_rect
from maze_visualizer import display_maze
import var
from pacgums import remove_gums
import parser

class Player():
    def __init__(self,surface):
        self.last = pygame.time.get_ticks()
        self.cooldown = 100
        self.move_last = pygame.time.get_ticks()
        self.move_cooldown =200
        self.lives = parser.lives
        self.pos = [930,510] # cell_size(60) * (width /2 +1) - 30  ..... cell_size * (height / 2 +2) -30
                             # -30 to be in the middle of the cell 
        self.surface=surface
        self.score = 0
        self.rect = None

        pacman1= pygame.image.load("images/pacman1.png")
        pacman2= pygame.image.load("images/2.png")
        pacman3= pygame.image.load("images/3.png")
        pacman4= pygame.image.load("images/4.png")

        self.pacman =[pacman1,pacman2,pacman3,pacman4]
        self.pacman_index = 0
        self.image = self.pacman[self.pacman_index]
        self.direction = None 
       # self.rect = self.image.get_rect(topleft= (self.pos[0],self.pos[1]))

    def draw(self,surface):
        self.rect = self.image.get_rect(center= (self.pos[0],self.pos[1]))
        surface.blit(self.image,self.rect)
        
    def check_ghost_collision(self, ghosts):
        if not ghosts:
            return None
        for g in ghosts:
            if g.respawning or g.edible:
                continue
            dx = self.pos[0] - g.position[0]
            dy = self.pos[1] - g.position[1]
            if (dx**2 + dy**2)**0.5 < 60:
                return g
        return None

    def move(self,maze, lines,possible_moves, ghosts=None):
        now = pygame.time.get_ticks()
        if now - self.move_last < self.move_cooldown:
            return None
        self.move_last = now
        keys = pygame.key.get_pressed()
        speed =1
        if keys[pygame.K_UP] and possible_moves["n"]:
            for i in range (60):
                self.pos[1] -= speed
                self.rotate("up")
                hit = self.check_ghost_collision(ghosts)
                if hit:
                    return hit
            if (self.pos[1] - 150)% 60 ==0:
                var.col -=1
        elif keys[pygame.K_DOWN] and possible_moves["s"]:
            for i in range (60):
                self.pos[1] +=speed
                self.rotate("down")
                hit = self.check_ghost_collision(ghosts)
                if hit:
                    return hit
            if (self.pos[1] - 150 )%60 ==0:
                var.col+=1
        elif keys[pygame.K_RIGHT] and  possible_moves["e"] :
            for i in range (60):
                self.pos[0]+=speed
                self.rotate("right")
                hit = self.check_ghost_collision(ghosts)
                if hit:
                    return hit
            if (self.pos[0] - 90)%60 == 0:
                var.row+=1
        elif keys[pygame.K_LEFT] and possible_moves["w"] :
            for i in range (60):
                self.pos[0]-=speed
                self.rotate("left")
                hit = self.check_ghost_collision(ghosts)
                if hit:
                    return hit
            if (self.pos[0] - 90) % 60 == 0:
                var.row-=1
        return None

    def animate(self):
        now = pygame.time.get_ticks() 
        # change image only if cooldown has been 0.1 seconds since last
        if now - self.last >= self.cooldown:
            self.last = now
            if self.pacman_index < 3:
                
                #pygame.time.wait(100)
                self.pacman_index += 1
            else:
                self.pacman_index = 0
            self.update_image()

    def rotate(self,goal_direction):
        if self.direction == goal_direction :
            return
        self.direction = goal_direction
        self.update_image()

    def update_image(self):
        rotation =0
        if self.direction == "up":
           rotation = 90
        elif self.direction == "down":
           rotation = 270
        elif self.direction == "right":
            rotation = 0
        elif self.direction == "left":
            rotation = 180
        self.image = pygame.transform.rotozoom(self.pacman[self.pacman_index],rotation,2)

    def ate_gum(self,gum_rect):
        for gum in gum_rect:
            #print(gum.x,gum.y)
            if self.pos[0] == gum.x+1 and self.pos[1] == gum.y+1:
                self.score += parser.points_per_pacgum
                var.num_of_eaten_gums+=1
                var.removed.append(gum)
        if self.ate_super():
            var.num_of_eaten_gums+=1
            self.score += parser.points_per_super_pacgum 
        return self.score
    def ate_super(self):
        if self.pos[0] == 90 and self.pos[1] == 150 and not var.super1:
            x=90
            y=150
            var.super1 = 1
            print("super")
            remove_gums(self.surface,x=90,y=150)
            var.edible = True
            return True
        elif self.pos[0] == 1830 and self.pos[1] == 150 and not var.super2:
            x=1830
            y=150
            var.super2 = 1
            print("super")
            remove_gums(self.surface,x=1830,y=150)
            var.edible = True
            return True
        elif self.pos[0] == 90 and self.pos[1] == 930 and not var.super3:
            x=90
            y=930
            var.super3 = 1
            print("super")
            remove_gums(self.surface,x=90,y=930)
            var.edible = True
            return True

        elif self.pos[0] == 1830 and self.pos[1] == 930 and not var.super4:
            x=1830
            y=930
            var.super4 = 1
            print("super")
            remove_gums(self.surface,x=1830,y=930)  
            var.edible = True
            return True
    

        
