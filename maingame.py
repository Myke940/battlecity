import pygame
import sys
from random import randint
from Enemy import EnemyFactory
from obstacle import Object
from Players import Player


pygame.font.init()

class Game:
    def __init__(self, width, hight):
        self.screen_width = hight
        self.screen_hight = width


        self.wall_img = pygame.transform.scale(pygame.image.load('wall.png'),(15, 15))
        self.bullet_img = pygame.transform.scale(pygame.image.load('onlybullet.png'),(4, 6))
        self.bg_img = pygame.transform.scale(pygame.image.load('bg.webp'), (350, 400))

        self.w = pygame.display.set_mode((self.screen_width, self.screen_hight))
        self.c = pygame.time.Clock()
        self.ls = pygame.time.get_ticks()
        self.m = 'Menu'
        self.p = Player(0, 0)
        # Створюємо 15 перешкод у вигляді сітки 3x5 з проміжками
        self.o = [
            Object(50, 50), Object(50, 150), Object(50, 250),  # Перший стовпець
            Object(100, 100), Object(100, 200), Object(100, 300),  # Другий стовпець
            Object(150, 50), Object(150, 150), Object(150, 250),  # Третій стовпець
            Object(200, 100), Object(200, 200), Object(200, 300),  # Четвертий стовпець
            Object(250, 50), Object(250, 150), Object(250, 250)  # П'ятий стовпець
        ]
        for o in self.o:
            o.image = self.wall_img
            
        self.e = [EnemyFactory.createnemy('h', 65, 50, self.bullet_img), EnemyFactory.createnemy('v', 40, 10, self.bullet_img), EnemyFactory.createnemy('h', 300, 180, self.bullet_img)]
    def quit():
        pygame.quit()
        sys.exit()

    def menu(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.m = 'Game'
            if event.type == pygame.QUIT:
                self.quit()

        self.w.fill((0, 0 ,38))
        font = pygame.font.Font(None, 45)
        q = font.render('Menu', True, (255, 255, 255))
        self.w.blit(q, (135, 50))
        e = font.render('Press space to start', True, (255, 255, 255))
        self.w.blit(e, (25, 225))
        self.p.l = 100
        
        pygame.display.update()
        self.c.tick(60)

    def game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.p.shoot(self.bullet_img)
        btn1 = pygame.key.get_pressed()
        dx, dy = 0, 0
        if btn1[pygame.K_w] == True and self.p.rect.y > 0:
            dy = -1
        elif btn1[pygame.K_a] == True and self.p.rect.x > 0:
            dx = -1
        elif btn1[pygame.K_s] == True and self.p.rect.y < 380:
            dy = 1
        elif btn1[pygame.K_d] == True and self.p.rect.x < 330:
            dx = 1

        self.spawn_enemy()
        self.p.moveTo(dx, dy, self.o)
        self.w.blit(self.bg_img, (0,0))

        # Додано: вивід статистики
        font = pygame.font.Font(None, 20)
        lives_text = font.render(f'HP: {self.p.l}', True, (255, 255, 255))
        self.w.blit(lives_text, (10, 10))
        score_text = font.render(f'Score: {self.p.points}', True, (255, 255, 255))
        self.w.blit(score_text, (10, 30))

        self.p.draw(self.w)
        for o in self.o:
            o.draw(self.w)
        for e in self.e:
            e.move(self.o)
            e.draw(self.w)
            e.shoot()
            for b in e.bullets:
                if b.rect.colliderect(self.p.rect):
                    self.p.l -= 10
                    e.bullets.remove(b)
                    print('lol')
                    if self.p.l <= 0:
                        self.m = 'Result'
            for b in self.p.b:
                if b.rect.colliderect(e.rect):
                    e.health -= 1
                    self.p.b.remove(b)
                    if e.health <= 0:
                        self.e.remove(e)
                        self.p.points += 1
                        
        if self.p.points >= 10:
            self.m = 'Result'

        pygame.display.update()
        self.c.tick(60)

    def result(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.m = 'Menu'
            if event.type == pygame.QUIT:
                self.quit()

        self.w.fill((0, 0 ,38))
        font = pygame.font.Font(None, 45)
        q = font.render('Game Over', True, (255, 0, 90))
        self.w.blit(q, (100, 50))
        e = font.render('Press space to restart', True, (255, 255, 255))
        self.w.blit(e, (15, 225))
        
        pygame.display.update()
        self.c.tick(60)


    def spawn_enemy(self):
        
        nowtime = pygame.time.get_ticks()
        if nowtime - self.ls >= 5000:
            q = randint(0, 1)
            if q == 1:
                enemytype = 'v'
            else:
                enemytype = 'h'
            enemy = EnemyFactory.createnemy(enemytype, randint(0, 385), randint(0, 335), self.bullet_img)
            self.e.append(enemy)
            self.ls = nowtime

    def run(self):
        while True:
            if self.m == 'Menu':
                self.menu()
            elif self.m == 'Game':
                self.game()
            elif self.m == 'Result':
                self.result()


t = Game(400, 350)
t.run()


