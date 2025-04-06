import pygame
from setting import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):
        #display surface
        self.display_surface = pygame.display.get_surface()
        
        #sprites groups setups
        self.visable_sprites = pygame.sprite.Group()
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
        self.visable_sprites.draw(self.display_surface)
        self.visable_sprites.update()