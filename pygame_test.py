import pygame
from sys import exit

from pygame.constants import KEYDOWN

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((720, 400))
pygame.display.set_caption("game")

#variables
orientation = "right"
jump = False

class Animation():
    def __init__(self):
        self.background = pygame.image.load("background/bg.png").convert_alpha()
        self.bg_rect = self.background.get_rect()

        self.last = pygame.time.get_ticks()
        self.frame_index = 0
        
        self.idle = []
        for i in range (4):
            img = pygame.image.load(f"player/idle/adventurer-idle-0{str(i)}.png").convert_alpha()
            self.idle.append(pygame.transform.scale(img, (img.get_width()*5, img.get_height()*5)))

        self.run = []
        for i in range (6):
            img = pygame.image.load(f"player/run/adventurer-run3-0{str(i)}.png").convert_alpha()
            self.run.append(pygame.transform.scale(img, (img.get_width()*5, img.get_height()*5)))

        self.jump = []
        for i in range (4):
            img = pygame.image.load(f"player/jump/adventurer-jump-0{str(i)}-1.3.png").convert_alpha()
            self.jump.append(pygame.transform.scale(img, (img.get_width()*5, img.get_height()*5)))


    def frame_update(self, cooldown, anim_length):
        if pygame.time.get_ticks() - self.last > cooldown:
            self.frame_index+=1
            self.last = pygame.time.get_ticks()
        if self.frame_index >= anim_length:
            self.frame_index = 0

animation = Animation()

class Player():
    def __init__(self, x, y):
        self.pos = [x, y]
        self.idle_cooldown = 300
        self.run_cooldown = 200
        self.jump_cooldown = 170

    def idle(self):
        animation.frame_update(self.idle_cooldown, len(animation.idle))
        if orientation == "right":
            img = animation.idle[animation.frame_index]
        elif orientation == "left":
            img = pygame.transform.flip(animation.idle[animation.frame_index], True, False)
        self.idle_rect = img.get_rect(bottomleft = self.pos)
        screen.blit(img, self.idle_rect)        


    def run(self):
        animation.frame_update(self.run_cooldown, len(animation.run))
        if orientation == "right":
            img = animation.run[animation.frame_index]
            if self.pos[0] < 550:
                self.pos[0]+=10
        elif orientation == "left":
            img = pygame.transform.flip(animation.run[animation.frame_index], True, False)
            if self.pos[0] > -80 :
                self.pos[0]-=10
        self.run_rect = img.get_rect(bottomleft = self.pos)
        screen.blit(img, self.run_rect)
        
        
    def jump(self):
        animation.frame_update(self.jump_cooldown, len(animation.jump))
        if orientation == "right":
            img = animation.jump[animation.frame_index]
            if self.pos[0] < 550:
                self.pos[0]+=10
        elif orientation == "left":
            img = pygame.transform.flip(animation.jump[animation.frame_index], True, False)
            if self.pos[0] > -80 :
                self.pos[0]-=10

        self.jump_rect = img.get_rect(bottomleft = self.pos)
        screen.blit(img, self.jump_rect)

    

player = Player(0, 360)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                jump = True
    
    screen.blit(animation.background, animation.bg_rect)

    keys = pygame.key.get_pressed()

    if jump :
        animation.frame_index = 0
        for i in range(-20, 21, 2):
            screen.blit(animation.background, animation.bg_rect)
            player.pos[1] += i
            player.jump()
            clock.tick(30)
            pygame.display.update()
        jump = False

    if keys[pygame.K_d] or keys[pygame.K_a]:
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            orientation = "right"
        elif keys[pygame.K_a] and not keys[pygame.K_d]:
            orientation = "left"
        player.run()

    else :
        player.idle()
    pygame.display.update()
    clock.tick(30) 
