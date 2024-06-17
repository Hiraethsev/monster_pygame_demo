from data_set import * 
from import_method import load_image
from entities import Entity
from data_import import COLORS

class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = vector()
		self.shadow_surf = load_image('..', 'graphics', 'other', 'shadow')
		self.notice_surf = load_image('..', 'graphics', 'ui', 'notice')

	def draw(self, player):
		# 根据玩家中心位置的偏移量来确定它们的绘制位置，以确保玩家所在位置始终在窗口的中心
		# 背景的运动方向与玩家运动方向相反
		self.offset.x = -(player.rect.centerx - 1280 / 2)
		self.offset.y = -(player.rect.centery - 720 / 2)

		bg_sprites = [sprite for sprite in self if sprite.z < Layer_Z_Index['main']]
		# 按 y_order 排序，以确保正确的渲染顺序（从上到下）。
		main_sprites = sorted([sprite for sprite in self if sprite.z == Layer_Z_Index['main']], key = lambda sprite: sprite.y_order)
		fg_sprites = [sprite for sprite in self if sprite.z > Layer_Z_Index['main']]

		for layer in (bg_sprites, main_sprites, fg_sprites):
			for sprite in layer:
				if isinstance(sprite, Entity):

					# 用于将阴影图像绘制到游戏的主显示表面
					self.display_surface.blit(self.shadow_surf, sprite.rect.topleft + self.offset + vector(40,100))
				# 将精灵的图像绘制到表面，根据精灵的矩形位置来确定位置
				self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

				if sprite == player and player.noticed:
					rect = self.notice_surf.get_frect(midbottom = sprite.rect.midtop)
					self.display_surface.blit(self.notice_surf, rect.topleft + self.offset)

class BattleSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()

	def draw(self, current_sprite, side, target_index, player_sprites, opponent_sprites):
		# 获取可用位置
		sprite_group = opponent_sprites if side == 'opponent' else player_sprites

		sprites = {sprite.pos_index: sprite for sprite in sprite_group}
		# 检查 target_index 是否超出范围
		keys_list = list(sprites.keys())
		if target_index < 0 or target_index >= len(keys_list):
			pass
		else:
			monster_sprite = sprites[keys_list[target_index]]

			for sprite in sorted(self, key=lambda sprite: sprite.z):
				self.display_surface.blit(sprite.image, sprite.rect)

				if sprite.z == Battle_Drawing_Layers['name']:
					if (sprite.monster_sprite == current_sprite or sprite.monster_sprite == monster_sprite):
						if sprite.monster_sprite.entity == 'player':
							sprite.col = COLORS['light-yellow']
						else:
							sprite.col = COLORS['red']
					else:
						sprite.col = COLORS['black']

				if sprite.z == Battle_Drawing_Layers['layer'] and hasattr(sprite, "monster_sprite"):
					if sprite.monster_sprite.entity == 'player':
						if sprite.monster_sprite == current_sprite:
							sprite.col = '#f5eac1'
						else:
							sprite.col = '#ffffff'


