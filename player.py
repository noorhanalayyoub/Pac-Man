import pygame
class Player():
    def __init__(self,surface):
        self.clock = pygame.time.Clock()
        self.lives =3
        self.pos = [940,540]
        self.surface=surface
        #self.draw(surface)
        #self.move()
        pacman1= pygame.image.load("images/pacman1.png")
        pacman2= pygame.image.load("images/2.png")
        pacman3= pygame.image.load("images/3.png")
        pacman4= pygame.image.load("images/4.png")
        self.pacman =[pacman1,pacman2,pacman3,pacman4]
        self.pacman_index = 0
        self.image = self.pacman[self.pacman_index]
    def draw(self,surface):
        self.rect = self.image.get_rect(topleft= (self.pos[0],self.pos[1]))
        surface.blit(self.image,self.rect)
        
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: 
            self.pos[1] -= 1
        elif keys[pygame.K_DOWN]:
            self.pos[1] +=1
        elif keys[pygame.K_RIGHT]: 
            self.pos[0]+=1
        elif keys[pygame.K_LEFT]: 
            self.pos[0]-=1
    def animate(self):
        # print(pygame.time.get_ticks())
        if  (int(pygame.time.get_ticks()) % 60) == 0:
            if self.pacman_index < 3:
                self.pacman_index += 1
            else:
                self.pacman_index = 0
            self.image= self.pacman[self.pacman_index]
