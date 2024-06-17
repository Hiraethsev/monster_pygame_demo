from data_set import *
from os.path import join
from os import walk,listdir
import os
# 加载 TMX 格式的地图文件，并将其转换为 Pygame 中的表面对象
from pytmx.util_pygame import load_pygame
import json
import pygame
from pygame.math import Vector2 as vector
import requests

pygame.init()


# 加载和处理图像文件
def load_image(*path, alpha = True, format = 'png'):
	full_path = join(*path) + f'.{format}'
	if alpha:
		surf = pygame.image.load(full_path).convert_alpha()
	else:
		surf = pygame.image.load(full_path).convert()
	return surf




def import_data_json(url):
		base_url='https://mp-84c5d27f-2255-4204-b28f-a1601d5b822b.cdn.bspapp.com/master-demo/'
		url=base_url+url

		try:
				# 发送GET请求
				response = requests.get(url)
				
				# 如果响应成功，检查状态码
				response.raise_for_status()
				
				# 解析JSON响应
				data = response.json()
				
				return data
				
		except requests.exceptions.HTTPError as http_err:
				print(f"HTTP error occurred: {http_err}")
		except Exception as err:
				print(f"Other error occurred: {err}")

def import_data_json_from_folder(path):
    with open(path, encoding="utf-8") as fp:
        data = json.load(fp)
    return data

def import_tilemap(cols, rows, *path):
	frames = {}
	surf = load_image(*path)
	cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
	for col in range(cols):
		for row in range(rows):
			cutout_rect = pygame.Rect(col * cell_width, row * cell_height,cell_width,cell_height)
			cutout_surf = pygame.Surface((cell_width, cell_height))
			cutout_surf.fill('green')
			cutout_surf.set_colorkey('green')
			cutout_surf.blit(surf, (0,0), cutout_rect)
			frames[(col, row)] = cutout_surf
	return frames

def character_importer(cols, rows, *path):
	frame_dict = import_tilemap(cols, rows, *path)
	new_dict = {}
	for row, direction in enumerate(('down', 'left', 'right', 'up')):
		new_dict[direction] = [frame_dict[(col, row)] for col in range(cols)]
		new_dict[f'{direction}_idle'] = [frame_dict[(0, row)]]
	return new_dict

def all_character_import(*path):
	new_dict = {}
	for _, __, image_names in walk(join(*path)):
		for image in image_names:
			image_name = image.split('.')[0]
			new_dict[image_name] = character_importer(4,4,*path, image_name)
	return new_dict

def coast_importer(cols, rows, *path):
	frame_dict = import_tilemap(cols, rows, *path)
	new_dict = {}
	terrains = ['grass', 'grass_i', 'sand_i', 'sand', 'rock', 'rock_i', 'ice', 'ice_i']
	sides = {
		'topleft': (0,0), 'top': (1,0), 'topright': (2,0), 
		'left': (0,1), 'right': (2,1), 'bottomleft': (0,2), 
		'bottom': (1,2), 'bottomright': (2,2)}
	for index, terrain in enumerate(terrains):
		new_dict[terrain] = {}
		for key, pos in sides.items():
			new_dict[terrain][key] = [frame_dict[(pos[0] + index * 3, pos[1] + row)] for row in range(0,rows, 3)]
	return new_dict


def monster_importer(cols, rows, *path):
	monster_dict = {}
	for folder_path, sub_folders, image_names in walk(join(*path)):
		for image in image_names:
			image_name = image.split('.')[0]
			monster_dict[image_name] = {}
			frame_dict = import_tilemap(cols, rows, *path, image_name)
			for row, key in enumerate(('idle', 'attack')):
				monster_dict[image_name][key] = [frame_dict[(col,row)] for col in range(cols)]
	return monster_dict


def attack_importer(*path):
	attack_dict = {}
	for folder_path, _, image_names in walk(join(*path)):
		for image in image_names:
			image_name = image.split('.')[0]
			attack_dict[image_name] = list(import_tilemap(4,1,folder_path, image_name).values())
	return attack_dict



def draw_bar(surface, rect, value, max_value, color, bg_color, radius = 1):
	ratio = rect.width / max_value
	bg_rect = rect.copy()
	progress = max(0, min(rect.width,value * ratio))
	progress_rect = pygame.FRect(rect.topleft, (progress,rect.height))
	pygame.draw.rect(surface, bg_color, bg_rect, 0, radius)
	pygame.draw.rect(surface, color, progress_rect, 0, radius)


# 检查一个实体是否与目标（如玩家）之间的范围是否在一个设定的视野
def check_distance(radius, entity, target, tolerance = 30):
	relation = vector(target.rect.center) - vector(entity.rect.center)

	if relation.length() >= radius:
		return False

	direction_checks = {
		'left': relation.x < 0 and abs(relation.y) < tolerance,
		'right': relation.x > 0 and abs(relation.y) < tolerance,
		'up': relation.y < 0 and abs(relation.x) < tolerance,
		'down': relation.y > 0 and abs(relation.x) < tolerance
	}

	# 如果entity.facing_direction在direction_checks中存在对应的键，则返回相应的布尔值，否则返回False
	return direction_checks.get(entity.facing_direction, False)