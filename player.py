import pygame

class Player():
    def __init__(self,surface):
        self.last = pygame.time.get_ticks()
        self.cooldown = 100
        self.lives =3
        self.pos = [940,540]
        self.surface=surface
        self.score = 0 

        pacman1= pygame.image.load("images/pacman1.png")
        pacman2= pygame.image.load("images/2.png")
        pacman3= pygame.image.load("images/3.png")
        pacman4= pygame.image.load("images/4.png")

        self.pacman =[pacman1,pacman2,pacman3,pacman4]
        self.pacman_index = 0
        self.image = self.pacman[self.pacman_index]
        self.direction = None
    

    def draw(self,surface):
        self.rect = self.image.get_rect(topleft= (self.pos[0],self.pos[1]))
        surface.blit(self.image,self.rect)
        
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.pos[1] -= 1
            self.rotate("up")
        elif keys[pygame.K_DOWN]:
            self.pos[1] +=1
            self.rotate("down")
        elif keys[pygame.K_RIGHT]: 
            self.pos[0]+=1
            self.rotate("right")
        elif keys[pygame.K_LEFT]: 
            self.pos[0]-=1
            self.rotate("left")

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
           #self.image = pygame.transform.rotate(original_image,90)
           rotation = 90
        elif self.direction == "down":
          # self.image = pygame.transform.rotate(original_image,270)
           rotation = 270
        elif self.direction == "right":
            #self.image = pygame.transform.rotate(original_image,0)
            rotation = 0
        elif self.direction == "left":
            #self.image = pygame.transform.rotate(original_image,180)
            rotation = 180
        self.image = pygame.transform.rotozoom(self.pacman[self.pacman_index],rotation,2)



        
