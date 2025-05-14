import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
    
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
