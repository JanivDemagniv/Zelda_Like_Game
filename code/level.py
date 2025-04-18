import pygame
from setting import *
from tile import Tile
from player import Player
from support import *
from random import choice
from debug import debug

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
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_objects.csv')
        }

        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index,col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacles_sprites],'invisiable')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[self.visable_sprites,self.obstacles_sprites],'grass',random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visable_sprites,self.obstacles_sprites],'object',surf)

        self.player = Player((2000,1430),[self.visable_sprites],self.obstacles_sprites)


    def run(self):
        #update and draw the gaem
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()
        debug(self.player.status)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_heigth = self.display_surface.get_size()[1] // 2
        self.offest = pygame.math.Vector2()

        #creating floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0)) 

    def custom_draw(self, player):
        self.offest.x = player.rect.centerx - self.half_width
        self.offest.y = player.rect.centery - self.half_heigth

        #drawing the floor
        offset_floor_position = self.floor_rect.topleft - self.offest
        self.display_surface.blit(self.floor_surf, offset_floor_position)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offest
            self.display_surface.blit(sprite.image,offset_position)

