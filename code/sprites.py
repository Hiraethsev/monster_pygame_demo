from data_set import *
from timer import Timer


class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, surface, groups, z_index = Layer_Z_Index['main']):
		super().__init__(groups)
		self.image = surface
		self.rect = self.image.get_frect(topleft = pos)
		self.z = z_index
		self.y_order = self.rect.centery
		# 将碰撞检测和绘制逻辑分开
		self.hitbox = self.rect.copy()


class TransitionSprite(Sprite):
	def __init__(self, pos, size, target, groups):
		surf = pygame.Surface(size)
		super().__init__(pos, surf, groups)
		self.target = target

class CollideSprite(Sprite):
	def __init__(self, pos, surf, groups,status=False):
		super().__init__(pos, surf, groups)
		if status==True:
			self.hitbox = self.rect.inflate(0, -self.rect.height * 0.6)
		else:
			self.hitbox = self.rect.copy()

class MonsterPatchSprite(Sprite):
	def __init__(self, pos, surf, groups, biome, monsters, level):
		self.biome = biome
		super().__init__(pos, surf, groups, Layer_Z_Index['main' if biome != 'sand' else 'background'])
		self.y_order -= 40
		self.biome = biome
		self.monsters = monsters.split(',')
		self.level = level

class AnimatedSprite(Sprite):
	def __init__(self, pos, frames, groups, z = Layer_Z_Index['main']):
		self.frame_index, self.frames = 0, frames
		super().__init__(pos, frames[self.frame_index], groups, z)

	def animate(self, dt):
		self.frame_index += 6* dt
		self.image = self.frames[int(self.frame_index % len(self.frames))]

	def update(self, dt):
		self.animate(dt)


