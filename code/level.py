import pygame
from setting import *
from tile import Tile
from player import Player
from support import *
from random import choice
from debug import debug
from weapon import *
from ui import UI

class Level:
    def __init__(self):
        #display surface
        self.display_surface = pygame.display.get_surface()
        
        #sprites groups setups
        self.visable_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        #attacks sprites
        self.current_attack = None

        #sprite setup
        self.create_map()

        #player interface
        self.ui = UI()

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

        self.player = Player(
            pos = (2000,1430),
            groups = [self.visable_sprites],
            obstacle_sprites = self.obstacles_sprites,
            create_attack = self.create_attack,
            destroy_attack= self.destroy_attack,
            create_magic = self.create_magic)

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visable_sprites])

    def create_magic(self,style,strength,cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        #update and draw the gaem
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()
        self.ui.display(self.player)

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

