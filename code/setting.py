# pygame-ce 功能更多，运行速度更快
# get_frect,get_just_pressed

# 导入 Pygame 中用于表示二维向量的类，表示平面上的位置、速度、加速度等概念。
from pygame.math import Vector2 as vector

# 用于关闭游戏

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
# 方块的尺寸
TILE_SIZE = 64
# 动画速度
ANIMATION_SPEED = 6
BATTLE_OUTLINE_WIDTH = 4

COLORS = {
	'white': '#f4fefa',
	'pure white': '#ffffff',
	'dark': '#2b292c',
	'light': '#c8c8c8',
	'gray': '#3a373b',
	'gold': '#ffd700',
	'light-yellow': '#ebc700',
	'light-green': '#75a99c',
	'light-gray': '#4b484d',
	'light-blue': '#41c6e1',
	'fire': '#f8a060',
	'water': '#50b0d8',
	'plant': '#64a990',
	'black': '#000000',
	'red': '#f03131',
	'blue': '#66d7ee',
	'normal': '#ffffff',
	'dark white': '#f0f0f0'
}

# 精灵图层次排序
WORLD_LAYERS = {
	'water': 0,
	'bg': 1,
	'shadow': 2,
	'main': 3,
	'top': 4
}

BATTLE_POSITIONS = {
	'left': {'top': (360, 260), 'center': (190, 400), 'bottom': (410, 520)},
	'right': {'top': (900, 260), 'center': (1110, 390), 'bottom': (900, 550)}
}

BATTLE_LAYERS = {
	'outline': 0,
	'name': 1,
	'monster': 2,
	'effects': 3,
	'overlay': 4
}

BATTLE_CHOICES = {
	'full': {
		'fight': {'pos': vector(30, -60), 'icon': 'sword'},
		'defend': {'pos': vector(40, -20), 'icon': 'shield'},
		'switch': {'pos': vector(40, 20), 'icon': 'arrows'},
		'catch': {'pos': vector(30, 60), 'icon': 'hand'}},

	'limited': {
		'fight': {'pos': vector(30, -40), 'icon': 'sword'},
		'defend': {'pos': vector(40, 0), 'icon': 'shield'},
		'switch': {'pos': vector(30, 40), 'icon': 'arrows'}}
}
