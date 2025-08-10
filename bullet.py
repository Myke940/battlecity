import pygame

class Bullet:
    def __init__(self, x, y, dx, dy):
        self.rect = pygame.Rect(x, y, 4, 6,)
        self.dx = dx * 10
        self.dy = dy * 10

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, w):
        if hasattr(self, 'image'):
            w.blit(self.image, self.rect)
        else:
            pygame.draw.rect(w, (244, 15, 17), self.rect)
        

