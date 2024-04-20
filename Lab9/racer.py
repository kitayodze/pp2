import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("C:\\Users\\Асет\\Desktop\\pp2\\lab8\\resources\\AnimatedStreet.png")
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\Асет\\Desktop\\pp2\\lab8\\resources\\Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:\\Users\\Асет\\Desktop\\pp2\\lab8\\resources\\Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load("C:\\Users\\Асет\\Desktop\\pp2\\lab8\\resources\\Coin.jpg")
        self.image = pygame.transform.scale(original_image, (25, 25)) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0, SCREEN_WIDTH - 25), 0)
        self.collected = False
        self.speed = SPEED - 1 

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > 600:
            self.reset()

    def reset(self):
        self.rect.topleft = (random.randint(0, SCREEN_WIDTH - 25), 0)
        self.collected = False  


P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
coins = pygame.sprite.Group()

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

COIN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(COIN_EVENT, 4000) 

collected_coins_counter = 0

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == COIN_EVENT:
            new_coin = Coin()
            coins.add(new_coin)

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    collected_coins_text = font_small.render(f"Collected Coins: {collected_coins_counter}", True, BLACK)  
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(collected_coins_text, (200, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    for coin in coins:
        DISPLAYSURF.blit(coin.image, coin.rect)
        coin.move()

    if pygame.sprite.spritecollide(P1, coins, True):
        collected_coins_counter += 1  

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("C:\\Users\\Асет\\Desktop\\pp2\\lab8\\resources\\crash.wav").play()
        pygame.mixer.music.stop()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)