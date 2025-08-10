import pygame



class Object:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
    
    def draw(self, w):

        if hasattr(self, 'image'):
            w.blit(self.image, self.rect)
        else:
            pygame.draw.rect(w, (0, 255, 0), self.rect)
