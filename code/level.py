import pygame
from setting import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):
        #display surface
        self.display_surface = pygame.display.get_surface()
        
        #sprites groups setups
        self.visable_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()

    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y),[self.visable_sprites,self.obstacles_sprites])
                if col == 'p':
                    self.player = Player((x,y),[self.visable_sprites],self.obstacles_sprites)

    def run(self):
        #update and draw the gaem
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_heigth = self.display_surface.get_size()[1] // 2
        self.offest = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offest.x = player.rect.centerx - self.half_width
        self.offest.y = player.rect.centery - self.half_heigth

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offest
            self.display_surface.blit(sprite.image,offset_position)

