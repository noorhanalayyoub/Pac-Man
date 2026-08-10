import pygame
class Player():
    def __init__(self,surface):
        self.lives =3
        self.pos = [940,540]
        self.surface=surface
        #self.draw(surface)
        #self.move()
    def draw(self,surface):
        pygame.draw.circle(surface,(255,255,0),(self.pos[0],self.pos[1]),8)
        
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
