import pygame
from setting import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hit_box = self.rect.inflate(-10,-26)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keyboard = pygame.key.get_pressed()
        
        if keyboard[pygame.K_UP]:
            self.direction.y = -1
        elif keyboard[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keyboard[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keyboard[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hit_box.x += self.direction.x * speed
        self.collision('horizontal')
        self.hit_box.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hit_box.center
    
    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hit_box.colliderect(self.hit_box):
                    if self.direction.x > 0:
                        self.hit_box.right = sprite.hit_box.left
                    if self.direction.x < 0:
                        self.hit_box.left = sprite.hit_box.right
        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hit_box.colliderect(self.hit_box):
                    if self.direction.y < 0:
                        self.hit_box.top = sprite.hit_box.bottom
                    if self.direction.y > 0:
                        self.hit_box.bottom = sprite.hit_box.top

    def update(self):
        self.input()
        self.move(self.speed)