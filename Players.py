import pygame
from bullet import Bullet

class Player:
    def __init__(self, x, y, speed = 10):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.s = speed
        self.b = []
        self.d = (0, -1)
        self.l = 100
        self.points = 0
    def draw(self, w):
        pygame.draw.rect(w, (255, 0, 0), self.rect)
        for b in self.b:
            b.move()
            b.draw(w)
    def moveTo(self, dx, dy, obstacles):

        newx = self.rect.x + self.s * dx 
        newy = self.rect.y + self.s * dy
        test_rect = pygame.Rect(newx, newy, 15, 15)

        for o in obstacles:
            if test_rect.colliderect(o.rect):
                return
            
        self.rect.x = newx
        self.rect.y = newy

        if dx != 0 or dy != 0:
            self.d = (dx, dy)
    

    def shoot(self, bullet_img):
        q = Bullet(self.rect.centerx, self.rect.centery, self.d[0], self.d[1])
        q.image = bullet_img
        self.b.append(q)


            