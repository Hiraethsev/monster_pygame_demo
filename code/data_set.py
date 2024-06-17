import pygame
from pygame.math import Vector2 as vector
from import_method import *
from pytmx.util_pygame import load_pygame
from os.path import join





Display_Surface = pygame.display.set_mode((1280, 720))

def load_images_from_folder(*path,status):
	folder_path = join(*path)
	if status=='order':
		# 遍历指定文件夹中的所有图像文件
		# 顺序存储在列表=>序列帧
		images = []
		# 获取文件夹中的所有文件名，对文件名进行排序，确保按数字顺序加载图像文件
		image_names = sorted(listdir(folder_path), key=lambda name: int(name.split('.')[0]))
	elif status=='dict':
		#存储在字典中=>可以通过特定的键快速访问每个图像,而且保留了图像的名字
		images = {}
		# 获取文件夹中的所有文件名
		image_names = listdir(folder_path)

	# 加载每个图像文件
	for image_name in image_names:
		full_path = join(folder_path, image_name)
		if os.path.isfile(full_path):  # 确保是文件
			surf = pygame.image.load(full_path).convert_alpha()
			if status=='order':
				images.append(surf)
			elif status=='dict':
				images[os.path.splitext(image_name)[0]] = surf

	return images




Layer_Z_Index = {
	'water': 0,
	'background': 1,
	'shadow': 2,
	'main': 3,
	'top': 4
}

BattleMosterPos = {
	'left': {'top': (360, 110), 'center': (190, 250), 'bottom': (410, 370)},
	'right': {'top': (900, 110), 'center': (1110, 270), 'bottom': (900, 390)}
}

Battle_Drawing_Layers =  {
	'name': 1,
	'monster-display': 2,
	'layer': 3
}

BattleChoice = {
		'fight':  {'pos' : vector(30, -60), 'icon': 'sword'},
		'defend': {'pos' : vector(40, -20), 'icon': 'shield'},
		'switch': {'pos' : vector(40, 20), 'icon': 'arrows'},
		'catch':  {'pos' : vector(30, 60), 'icon': 'hand'},
}



Tmx_Maps = {
			'world': load_pygame(join('..', 'data', 'maps', 'world.tmx')),
			'hospital': load_pygame(join('..', 'data', 'maps', 'hospital.tmx')),
			'hospital2': load_pygame(join('..', 'data', 'maps', 'hospital2.tmx')),
			'arena': load_pygame(join('..', 'data', 'maps', 'arena.tmx')),
			'fire': load_pygame(join('..', 'data', 'maps', 'fire.tmx')),
			'house': load_pygame(join('..', 'data', 'maps', 'house.tmx')),
			'plant': load_pygame(join('..', 'data', 'maps', 'plant.tmx')),
			'water': load_pygame(join('..', 'data', 'maps', 'water.tmx'))
		}

Overworld_Frames = {
	'water': load_images_from_folder('..', 'graphics', 'tilesets', 'water',status='order'),
	'coast': coast_importer(24, 12, '..', 'graphics', 'tilesets', 'coast'),
	'characters': all_character_import('..', 'graphics', 'characters')
}

Monster_Frames = {
	'icons': load_images_from_folder('..', 'graphics', 'icons',status="dict"),
	'monsters': monster_importer(4, 2, '..', 'graphics', 'monsters'),
	'ui': load_images_from_folder('..', 'graphics', 'ui',status="dict"),
	'attack': attack_importer('..', 'graphics', 'attacks')
}


Background_Frames = load_images_from_folder('..', 'graphics', 'backgrounds',status='dict')
Start_Animation_Frames = load_images_from_folder('..', 'graphics', 'other', 'star animation',status='order')



