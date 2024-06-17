from data_set import * 
from import_method import check_distance
from timer import Timer
from random import choice
from monster import Monster
from pgzero import *
class Entity(pygame.sprite.Sprite):
	def __init__(self, pos, frames, groups, facing_direction):
		super().__init__(groups)
		# 实体的渲染层次
		self.z = Layer_Z_Index['main']

		# 动画相关
		self.frames=frames
		self.frame_index= 0 
		self.facing_direction = facing_direction

		# 移动相关 
		# 实体的移动方向（一个二维向量）
		self.direction = vector()
		self.speed = 250
		self.blocked = False

		# 精灵设置
		self.image = self.frames[self.get_state()][self.frame_index]
		self.rect = self.image.get_frect(center = pos)
		# 收缩实体的 rect，碰撞的宽度减小一半，高度减小60像素
		self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)

		# 垂直排序，决定实体的渲染顺序
		self.y_sort = self.rect.centery

	def animate(self, dt):
		self.frame_index += 6* dt
		self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]

	def get_state(self):
		# 判断是否在运动
		moving = bool(self.direction)
		if moving:
			if self.direction.x != 0:
				self.facing_direction = 'right' if self.direction.x > 0 else 'left'
			if self.direction.y != 0:
				self.facing_direction = 'down' if self.direction.y > 0 else 'up'
		return f"{self.facing_direction}{'' if moving else '_idle'}"

	# 根据玩家位置来使npc朝向玩家
	def change_facing_direction(self, target_pos):
		relation = vector(target_pos) - vector(self.rect.center)
		# 检测近似在一个水平轴上还是在一个竖直轴上
		if abs(relation.y) < 30:
			self.facing_direction = 'right' if relation.x > 0 else 'left'
		else:
			self.facing_direction = 'down' if relation.y > 0 else 'up'

	def block(self):
		self.blocked = True
		self.direction = vector(0,0)

	def unblock(self):
		self.blocked = False

class Character(Entity):
	def __init__(self, pos, frames, groups, facing_direction, character_data, player, create_dialog, collision_sprites, radius, nurse):
		super().__init__(pos, frames, groups, facing_direction)
		self.character_data = character_data
		self.player = player
		self.create_dialog = create_dialog
		self.collision_rects = [sprite.rect for sprite in collision_sprites if sprite is not self]
		# 标记角色是否是护士
		self.nurse = nurse
		# 存储角色的怪物数据，如果有的话
		self.monsters = {i: Monster(name, lvl) for i, (name, lvl) in character_data['monsters'].items()} if 'monsters' in character_data else None

		# movement 
		self.has_moved = False
		self.has_noticed = False
		self.radius = int(radius)
		self.view_directions = character_data['directions']

		self.timers = {
			'notice': Timer(500, func = self.start_move)
		}

	def get_dialog(self):
		return self.character_data['dialog'][f"{'defeated' if self.character_data['defeated'] else 'default'}"]

	# 检测玩家是否在角色的视野内
	def check_around(self):
		if check_distance(self.radius, self, self.player) and not self.has_moved and not self.has_noticed:
			self.player.block()
			self.player.change_facing_direction(self.rect.center)
			self.timers['notice'].activate()
			self.has_noticed = True
			self.player.noticed = True
			pygame.mixer.Sound(f'../sounds/notice.wav').play()


	def start_move(self):
		# 将向量转换为单位向量，得到方向信息而不考虑距离大小。
		relation = (vector(self.player.rect.center) - vector(self.rect.center)).normalize()
		self.direction = vector(round(relation.x), round(relation.y))

	def move(self, dt):
		if not self.has_moved and self.direction:
			if not self.hitbox.inflate(10,10).colliderect(self.player.hitbox):
				self.rect.center += self.direction * self.speed * dt
				self.hitbox.center = self.rect.center
			else:
				self.direction = vector()
				self.has_moved = True
				self.create_dialog(self)
				self.player.noticed = False

	def update(self, dt):
		for timer in self.timers.values():
			timer.update()

		self.animate(dt)
		if self.character_data['look_around']:
			self.check_around()
			self.move(dt)


class Player(Entity):
	def __init__(self, pos, frames, groups, facing_direction, collision_sprites):
		super().__init__(pos, frames, groups, facing_direction)
		self.collision_sprites = collision_sprites
		self.noticed = False

	def input(self):
		# 实时检测玩家是否按下某个键
		keys = pygame.key.get_pressed()
		# 通过输入向量
		input_vector = vector()
		if keys[pygame.K_UP]:
			input_vector.y -= 1
		if keys[pygame.K_DOWN]:
			input_vector.y += 1
		if keys[pygame.K_LEFT]:
			input_vector.x -= 1
		if keys[pygame.K_RIGHT]:
			input_vector.x += 1

		# 保持在斜方向移动时速度也保持一致
		self.direction = input_vector.normalize() if input_vector else input_vector

	def move(self, dt):
		self.rect.centerx += self.direction.x * self.speed * dt
		self.hitbox.centerx = self.rect.centerx
		self.collisions('x')

		self.rect.centery += self.direction.y * self.speed * dt
		self.hitbox.centery = self.rect.centery
		self.collisions('y')

	# 检查碰撞
	def collisions(self, direction):
		for sprite in self.collision_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if direction == 'x':
					if self.direction.x > 0: 
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right
					self.rect.centerx = self.hitbox.centerx
				else:
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery = self.hitbox.centery

	def update(self, dt):
		self.y_sort = self.rect.centery
		if not self.blocked:
			self.input()
			self.move(dt)
		self.animate(dt)