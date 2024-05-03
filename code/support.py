import pygame.image
import json
from setting import *
from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame

# import function
# 加载和处理图像文件
def import_image(*path,alpha=True,format='png'):
    full_path=join(*path)+f'.{format}'
    surf=pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf

# 遍历指定文件夹中的所有图像文件
# 顺序存储在列表=>序列帧
def import_folder(*path):
    frames=[]
    # 使用walk函数递归地访问每个文件夹，并返回每个目录的路径、子目录列表和文件列表。
    for folder_path,sub_folders,image_names in walk(join(*path)):
        # 基于文件名前的数字排序
        for image_name in sorted(image_names,key=lambda name:int(name.split('.')[0])):
            full_path=join(folder_path,image_name)
            surf=pygame.image.load(full_path).convert_alpha()
            frames.append(surf)
    return frames

#存储在字典中=>可以通过特定的键快速访问每个图像,而且保留了图像的名字
def import_folder_dict(*path):
    frames={}
    for folder_path,sub_folders,image_names in walk(join(*path)):
        # 基于文件名前的数字排序
        for image_name in image_names:
            full_path=join(folder_path,image_name)
            surf=pygame.image.load(full_path).convert_alpha()
            frames[image_name.split('.')[0]]=surf
    return frames

#针对包含多个子目录的文件夹，导入每个子目录内的图像，将它们按子目录名分类
def import_sub_folders(*path):
    frames={}
    # 当前目录路径，当前目录下的子目录列表，和当前目录下的文件名列表
    for _,sub_folders,__ in walk(join(*path)):
        if sub_folders:
            for sub_folder in sub_folders:
                frames[sub_folder]=import_folder(*path,sub_folder)
    return frames

# 基于原图的列和行数处理和分割一个大的图像（spritesheet）为多个小的图像，并将它们存储在一个字典中
# 包含多个小图像（sprites），小图像表示一个角色或物体在不同状态或执行不同动作
def import_tilemap(cols,rows,*path):
    frames={}
    surf=import_image(*path)
    cell_width,cell_height=surf.get_width()/cols,surf.get_height()/rows
    for col in range(cols):
        for row in range(rows):
            cutout_rect=pygame.Rect(col*cell_width,row*cell_height,cell_width,cell_height)
            cutout_surf=pygame.Surface((cell_width,cell_height))
            # 只保留裁剪的小部分而忽略其周围背景的其他像素
            cutout_surf.fill('green')
            cutout_surf.set_colorkey('green')
            # 将原始图像 surf 的 cutout_rect 区域复制到新创建的 cutout_surf 上
            cutout_surf.blit(surf,(0,0),cutout_rect)
            frames[(col,row)]=cutout_surf
    return frames

def character_import(cols,rows,*path):
    frame_dict=import_tilemap(cols,rows,*path)
    new_dict={}
    for row,direction in enumerate(('down','left','right','up')):
        new_dict[direction]=[frame_dict[(col,row)] for col in range(cols)]
        new_dict[f'{direction}_idle'] = [frame_dict[(0, row)]]
    return new_dict

def all_character_import(*path):
    new_dict = {}
    for _,__, image_names in walk(join(*path)):
        for image in image_names:
            image_name=image.split('.')[0]
            new_dict[image_name]=character_import(4,4,*path,image_name)
    return new_dict

#获取coast
def coast_importer(cols,rows,*path):
    frames_dict=import_tilemap(cols,rows,*path)
    new_dict={}
    terrains = ['grass', 'grass_i', 'sand_i', 'sand', 'rock', 'rock_i', 'ice', 'ice_i']
    sides = {
        'topleft': (0, 0), 'top': (1, 0), 'topright': (2, 0),
        'left': (0, 1), 'right': (2, 1), 'bottomleft': (0, 2),
        'bottom': (1, 2), 'bottomright': (2, 2)}
    # 通过遍历，确定每一个terrains对应的sides，即边缘位置的坐标
    for index,terrain in enumerate(terrains):
        new_dict[terrain]={}
        for key,pos in sides.items():
            new_dict[terrain][key]=[frames_dict[(pos[0]+index*3,pos[1]+row)] for row in range(0,rows,3)]

    return new_dict

#获取data
def import_data_json(*path):
    with open(join(*path), encoding="utf-8") as fp:
        data = json.load(fp)
    return data

# 获取 monster
def monster_importer(cols,rows,*path):
    monster_dict={}
    for folder_path,sub_folders,image_names in walk(join(*path)):
        for image in image_names:
            image_name=image.split('.')[0]
            monster_dict[image_name]={}
            frame_dict=import_tilemap(cols,rows,*path,image_name)
            for row,key in enumerate(('idle','attack')):
                monster_dict[image_name][key]=[frame_dict[(col,row)] for col in range(cols)]

    return monster_dict

# game function
def check_connections(radius,entity,target,tolerance=30):
    relation=vector(target.rect.center)-vector(entity.rect.center)
    if relation.length()<radius:
        if (entity.facing_direction=='left' and relation.x<0 and abs(relation.y)<tolerance) or (entity.facing_direction=='right' and relation.x>0 and abs(relation.y)<tolerance) or (entity.facing_direction=='up' and relation.y<0 and abs(relation.x)<tolerance) or (entity.facing_direction=='down' and relation.y>0 and abs(relation.x)<tolerance):
            return True

def draw_bar(surface,rect,value,max_value,color,bgc,radius=1):
    ratio=rect.width/max_value
    bg_rect=rect.copy()
    proress=max(0,min(rect.width,value*ratio))
    progress_rect=pygame.FRect(rect.topleft,(proress,rect.height))
    pygame.draw.rect(surface,bgc,bg_rect,0,radius)
    pygame.draw.rect(surface,color,progress_rect,0,radius)
