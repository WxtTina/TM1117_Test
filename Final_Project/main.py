# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 14:41:40 2022

@author: ic2140
"""

import pygame
import random
import launcher
#import data

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("image/jet.png").convert_alpha()
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [0, resolution[1] / 2]
            )
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= resolution[0]:
            self.rect.right = resolution[0]
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= resolution[1]:
            self.rect.bottom = resolution[1]

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("image/missile.png").convert_alpha()
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [
                random.randint(resolution[0] + 20, resolution[0] + 100),
                random.randint(0, resolution[1])
                ]
            )
        self.speed = random.randint(5, 20)
        
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("image/cloud.png").convert_alpha()
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [
                random.randint(resolution[0] + 20, resolution[0] + 100),
                random.randint(0, resolution[1])
                ]
            )
        
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
            
class Shot(pygame.sprite.Sprite):
    def __init__(self):
        super(Shot, self).__init__()
        self.surf = pygame.image.load("image/shot.png").convert_alpha()
        self.surf.set_colorkey([255, 255, 255], RLEACCEL)
        self.rect = self.surf.get_rect(
            center = [
                player.rect.right,
                player.rect.bottom
                ]
            )
        
    def update(self):
        self.rect.move_ip(20, 0)
        if self.rect.left > resolution[0]:
            self.kill()

def exp_requirement(level):
    global requirement_total
    requirement_total = (level + 1) * level * 5
    return requirement_total

playing = True
    
while playing:
    # Initialization
    pygame.init()
    running = False
    launcher.main_menu(True)
    pygame.display.set_caption('Sky Wars')
    font_small = pygame.font.Font('font.ttf', 16)
    font = pygame.font.Font('font.ttf', 36)
    resolution = [800, 600]
    screen = pygame.display.set_mode(resolution)
    player = Player()
    start = pygame.time.get_ticks()
    level = 1
    life_total = 8
    exp_total = 0
    shot_total = 3
    cdbar_value = 8
    
    running = True
    shooting = True
    lifebar_list = []
    expbar_list = []
    powerbar_list = []
    cdbar_list = []
    for i in range(0, 9):
        lifebar_list += ["image/lifebar/{}.png".format(str(i))]
        expbar_list += ["image/expbar/{}.png".format(str(i))]
        powerbar_list += ["image/powerbar/{}.png".format(str(i))]
        cdbar_list += ["image/cdbar/{}.png".format(str(i))]

    # Sprites Groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites.add(player)

    # Events
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 300)
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)
    SHOOTING = pygame.USEREVENT + 3
    pygame.time.set_timer(SHOOTING, 15000)
    RECOVERING = pygame.USEREVENT + 4
    pygame.time.set_timer(RECOVERING, 10000)
    EXPUP = pygame.USEREVENT + 5
    pygame.time.set_timer(EXPUP, 1000)
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    
                if event.key == K_SPACE:
                    if shooting:
                        shot = Shot()
                        all_sprites.add(shot)
                        shot_total -= 1
                        shooting = False
                        shooting_start = pygame.time.get_ticks()
                        
            
            elif event.type == QUIT:
                running = False
            
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
            
            elif event.type == SHOOTING:
                if shot_total < 8:
                    shot_total += 1
            
            elif event.type == RECOVERING:
                if life_total < 8:
                    life_total += 1
                    
            elif event.type == EXPUP:
                exp_total += 1
        
        # Clock
        clock = pygame.time.get_ticks()
        survival = (clock - start) // 1000
        pygame.display.flip()
        pygame.time.Clock().tick(30)
        
        # Texts
        display_level = font_small.render("Level", True, [255, 0, 0])
        display_level_Rect = display_level.get_rect(center = [400, 30])
        display_level_value = font.render(str(level), True, [255, 0, 0])
        display_level_value_Rect = display_level_value.get_rect(center = [400, 55])
        
        # Shooting Related
        try:
            shooting_cd = clock - shooting_start
            cdbar_value = int(shooting_cd * 1.6 // 1000)
            
            if shooting_cd >= 5000:
                cdbar_value = 8
                shooting = True
            
            shot.update()
            
            if pygame.sprite.spritecollideany(shot, enemies):
                hit = pygame.sprite.spritecollide(shot, enemies, True)
                exp_total += 10
                shot.kill()
            
        except:
            pass 
        
        # Bars
        lifebar = pygame.image.load(lifebar_list[life_total]).convert_alpha()
        lifebar.set_colorkey([255, 255, 255], RLEACCEL)
        lifebar_rect = lifebar.get_rect(center = [700, 30])
        
        level = int((20 * exp_total + 25) ** 0.5 / 10 - 0.5) + 1
        exp_level = exp_total - exp_requirement(level - 1)
        expbar_value = int(round(exp_level / (level * 10) * 8 + 0.5))
        expbar = pygame.image.load(expbar_list[expbar_value]).convert_alpha()
        expbar.set_colorkey([255, 255, 255], RLEACCEL)
        expbar_rect = expbar.get_rect(center = [700, 50])
        
        powerbar = pygame.image.load(powerbar_list[shot_total]).convert_alpha()
        powerbar.set_colorkey([255, 255, 255], RLEACCEL)
        powerbar_rect = powerbar.get_rect(center = [80, 30])
        cdbar = pygame.image.load(cdbar_list[cdbar_value]).convert_alpha()
        cdbar.set_colorkey([255, 255, 255], RLEACCEL)
        cdbar_rect = cdbar.get_rect(center = [80, 50])
        
        # Display
        screen.fill("black")
        BackgroundList=["image/B1_1.png","image/B2_2.png","image/B3_3.png"]
        display = pygame.image.load(BackgroundList[launcher.transfer[0]]).convert_alpha()
        display.set_colorkey([255, 255, 255], RLEACCEL)
        display_rect = display.get_rect(center = [400,300])
        screen.blit(display, display_rect)
        
        screen.blit(display_level, display_level_Rect)
        screen.blit(display_level_value, display_level_value_Rect)
        screen.blit(lifebar, lifebar_rect)
        screen.blit(expbar, expbar_rect)
        screen.blit(powerbar, powerbar_rect)
        screen.blit(cdbar, cdbar_rect)
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()
        clouds.update()
        
        # Collision Detecting
        if pygame.sprite.spritecollideany(player, enemies):
            hit = pygame.sprite.spritecollide(player, enemies, True)
            life_total -= 3
            if life_total <= 0:
                player.kill()
                running = False
    
    launcher.main_menu(True)
    running = True

pygame.quit()