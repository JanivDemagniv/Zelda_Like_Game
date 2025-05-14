import pygame
from setting import *
from support import *
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites , create_attack, destroy_attack,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hit_box = self.rect.inflate(-10,-26)

        #graphics setup
        self.import_player_assests()
        self.status = 'down'

        #movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        #weapons
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200
        
        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        #stats
        self.stats = {
            'health':100,
            'energy': 100,
            'attack': 10,
            'magic': 4,
            'speed': 5
        }
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

    def import_player_assests(self):
        player_path = 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'right': [], 'left': [],
                        'up_idle':[], 'down_idle': [],'right_idle': [], 'left_idle': [],
                        'up_attack':[], 'down_attack': [],'right_attack': [], 'left_attack': []
                        }
        
        for animation in self.animations.keys():
            full_path = player_path  + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking:
            keyboard = pygame.key.get_pressed()
            
            #input movement
            if keyboard[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keyboard[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            if keyboard[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keyboard[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            #input attack
            if keyboard[pygame.K_z]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            
            #input magic
            if keyboard[pygame.K_x]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style,strength,cost)

            #input weapon switch
            if keyboard[pygame.K_a] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1 
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            #input magic switch
            if keyboard[pygame.K_s] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1 
                else:
                    self.magic_index = 0
                self.magic = list(weapon_data.keys())[self.weapon_index]

    def get_status(self):
        
        #idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        
        #attacking
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_cooldown >= self.attack_time:
                self.attacking = False
                self.destroy_attack()
        
        if not self.can_switch_weapon:
            if current_time - self.switch_duration_cooldown >= self.weapon_switch_time:
                self.can_switch_weapon = True
        
        if not self.can_switch_magic:
            if current_time - self.switch_duration_cooldown >= self.magic_switch_time:
                self.can_switch_magic = True

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        #set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hit_box.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)