from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain_man = []
    with open(path) as level_map:
        layout = reader(level_map,delimiter=',')
        for row in layout:
            terrain_man.append(list(row))
        return terrain_man
    
def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for img in img_files:
            full_path = path + '/' + img
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    
    return surface_list