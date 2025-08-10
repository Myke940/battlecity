import pygame
import time as t
from bullet import Bullet
from abc import ABC, abstractmethod


class Enemy(ABC):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 15, 15)
        self.health = 1
        self.bullets = []
    
    @abstractmethod
    def move(self, obstacles):
        pass
    
    @abstractmethod
    def shoot(self):
        pass
    
    @abstractmethod
    def draw(self, screen):
        pass

class Upbot(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ls = 0
        self.r = 2000
        self.direction = 'Up'
        # Завантаження та масштабування картинок для вертикального руху
        self.images = {
            'Up': pygame.transform.scale(pygame.image.load('manUp.png'), (15, 15)),
            'Down': pygame.transform.scale(pygame.image.load('manDown.png'), (15, 15))
        }

    def move(self, obstacle):
        if self.direction == 'Up':
            dy = -5
        else:
            dy = 5
        newy = self.rect.y + dy

        a = pygame.Rect(self.rect.x, newy, 15, 15)    
        for o in obstacle:
            if a.colliderect(o.rect):
                if self.direction == 'Up':
                    self.direction = 'Down' 
                else:
                    self.direction = 'Up'
                return
        if newy < 0 or newy > 400:
            if self.direction == 'Up':
                self.direction = 'Down' 
            else:
                self.direction = 'Up'

        self.rect.y = newy

    def shoot(self):
        nowtime = pygame.time.get_ticks()
        if nowtime - self.ls >= self.r:
            if self.direction == 'Up':
                dx = 0
                dy = -1
            else:
                dx = 0
                dy = 1

            b = Bullet(self.rect.centerx, self.rect.centery, dx, dy)
            if hasattr(self, 'bullet_img'):
                b.image = self.bullet_img
            self.bullets.append(b)
            self.ls = nowtime
            
    def draw(self, p): 
        # Відображаємо відповідну картинку залежно від напрямку
        p.blit(self.images[self.direction], self.rect)

        for b in self.bullets:
            b.move()
            b.draw(p)

class Squarebot(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.direction = 'left'
        self.ls = 0
        self.r = 2000
        # Завантаження та масштабування картинок для горизонтального руху
        self.images = {
            'left': pygame.transform.scale(pygame.image.load('manLeft.png'), (15, 15)),
            'right': pygame.transform.scale(pygame.image.load('manRight.png'), (15, 15))
        }

    def move(self, obstacle):
        if self.direction == 'left':
            dx = -5
        else:
            dx = 5
        newx = self.rect.x + dx

        a = pygame.Rect(newx, self.rect.y, 15, 15)    
        for o in obstacle:
            if a.colliderect(o.rect):
                if self.direction == 'left':
                    self.direction = 'right' 
                else:
                    self.direction = 'left'
                return
        if newx < 0 or newx > 350:
            if self.direction == 'left':
                self.direction = 'right' 
            else:
                self.direction = 'left'
                    
        self.rect.x = newx

    def shoot(self):
        nowtime = pygame.time.get_ticks()
        if nowtime - self.ls >= self.r:
            if self.direction == 'left':
                dx = -1
                dy = 0
            else:
                dx = 1
                dy = 0

            b = Bullet(self.rect.centerx, self.rect.centery, dx, dy)
            if hasattr(self, 'bullet_img'):
                b.image = self.bullet_img
            self.bullets.append(b)
            self.ls = nowtime

    def draw(self, p): 
        # Відображаємо відповідну картинку залежно від напрямку
        p.blit(self.images[self.direction], self.rect)
        for b in self.bullets:
            b.move()
            b.draw(p)

class EnemyFactory:
    @staticmethod
    def createnemy(type, x, y, bullet_img):
        if type == 'h':
            enemy = Upbot(x, y)
            enemy.bullet_img = bullet_img
            return enemy
        else:
            enemy = Squarebot(x, y)
            enemy.bullet_img = bullet_img
            return enemy