import pygame
from setting import *
from tile import Tile
from player import Player
from support import *
from random import choice , randint
from debug import debug
from weapon import *
from ui import UI
from enemy import Enemy
from particales import *
from magic import MagicPlayer
from upgrade import Upgrade

class Level:
    def __init__(self):
        #display surface
        self.display_surface = pygame.display.get_surface()
        self.game_pused = False
        
        #sprites groups setups
        self.visable_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        #attacks sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()

        #player interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        #particales
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
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
                            Tile((x,y),[self.obstacles_sprites],'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(pos = (x,y),
                                groups = [self.visable_sprites,self.obstacles_sprites, self.attackable_sprites],
                                sprite_type = 'grass',
                                surface = random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visable_sprites,self.obstacles_sprites],'object',surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    pos = (x,y),
                                    groups = [self.visable_sprites],
                                    obstacle_sprites = self.obstacles_sprites,
                                    create_attack = self.create_attack,
                                    destroy_attack= self.destroy_attack,
                                    create_magic = self.create_magic)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391': 
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(
                                    monster_name = monster_name,
                                    pos = (x,y),
                                    obstacle_sprites = self.obstacles_sprites,
                                    damage_player = self.damage_player,
                                    triger_death_particale= self.triger_death_particales,
                                    add_exp= self.add_exp,
                                    groups = [self.visable_sprites, self.attackable_sprites])

    def create_attack(self):
        self.current_attack = Weapon(player = self.player,groups = [self.visable_sprites, self.attack_sprites])

    def create_magic(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,self.visable_sprites)

        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visable_sprites,self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particales(pos - offset,self.visable_sprites)
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particales(attack_type,self.player.rect.center,[self.visable_sprites])

    def triger_death_particales(self,particale_type,pos):
        self.animation_player.create_particales(particale_type,pos,self.visable_sprites)

    def add_exp(self,amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_pused = not self.game_pused

    def run(self):
        self.visable_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_pused:
            self.upgrade.display()
        else:
            self.visable_sprites.update()
            self.visable_sprites.enemny_update(self.player)
            self.player_attack_logic()
            

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

    def enemny_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)