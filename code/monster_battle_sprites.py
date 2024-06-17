from data_set import *
from random import uniform
from import_method import draw_bar
from timer import Timer
from data_import import COLORS
from sprites import Sprite,AnimatedSprite
# battle sprites
class MonsterSprite(pygame.sprite.Sprite):
	def __init__(self, pos, frames, groups, monster, index, pos_index, entity, apply_attack, create_monster):
		# data
		# 怪兽在队伍中的位置索引
		self.index = index
		self.pos_index = pos_index

		self.entity = entity
		self.monster = monster

		# 动画相关
		self.frame_index, self.frames, self.state = 0, frames, 'idle'
		self.animation_speed = 6+ uniform(-1, 1)

		self.z = Battle_Drawing_Layers['monster-display']

		# 是否高亮显示
		self.highlight = False

		# 攻击目标和当前攻击
		self.target_sprite = None
		self.current_attack = None

		# 回调函数，用于应用攻击和创建新怪兽
		self.apply_attack = apply_attack
		self.create_monster = create_monster

		# sprite setup
		# 设置精灵的图像和矩形，使其在指定位置居中
		super().__init__(groups)
		self.image = self.frames[self.state][self.frame_index]
		self.rect = self.image.get_frect(center = pos)

		# timers
		self.timers = {
			'remove highlight': Timer(300, func = lambda: self.set_highlight(False)),
			'kill': Timer(600, func = self.destroy)
		}

	def animate(self, dt):
		self.frame_index += 6* dt
		if self.state == 'attack' and self.frame_index >= len(self.frames['attack']):
			self.apply_attack(self.target_sprite, self.current_attack, self.monster.get_base_damage(self.current_attack))
			self.state = 'idle'

		self.adjusted_frame_index = int(self.frame_index % len(self.frames[self.state]))
		self.image = self.frames[self.state][self.adjusted_frame_index]

		if self.highlight:
			white_surf = pygame.mask.from_surface(self.image).to_surface()
			white_surf.set_colorkey('black')
			self.image = white_surf

	def set_highlight(self, value):
		self.highlight = value
		if value:
			self.timers['remove highlight'].activate()

	# 攻击
	def activate_attack(self, target_sprite, attack):
		self.state = 'attack'
		self.frame_index = 0
		self.target_sprite = target_sprite
		self.current_attack = attack
		self.monster.reduce_energy(attack)
		

	# 延迟销毁
	def delayed_kill(self, new_monster):
		if not self.timers['kill'].active:
			self.next_monster_data = new_monster
			self.timers['kill'].activate()

	def destroy(self):
		if self.next_monster_data:
			# 参数解包
			self.create_monster(*self.next_monster_data)
		self.kill()
		

	def update(self, dt):
		for timer in self.timers.values():
			timer.update()
		self.animate(dt)
		self.monster.update(dt)

class AttackSprite(AnimatedSprite):
	def __init__(self, pos, frames, groups):
		super().__init__(pos, frames, groups, Battle_Drawing_Layers['layer'])
		self.rect.center = pos

	def animate(self, dt):
		self.frame_index += 6* dt
		if self.frame_index < len(self.frames):
			self.image = self.frames[int(self.frame_index)]
		else:
			self.kill()

	def update(self, dt):
		self.animate(dt)


class DisplayShortSprite(Sprite):
	def __init__(self, position, surface, groups, duration):
		super().__init__(position, surface, groups, z = Battle_Drawing_Layers['layer'])
		self.rect.center = position
		self.death_timer = Timer(duration, autostart = True, func = self.kill)

	def update(self, _):
		self.death_timer.update()

class MonsterNameSprite(pygame.sprite.Sprite):
	def __init__(self, pos, monster_sprite, groups, font):
		super().__init__(groups)

		self.monster_sprite = monster_sprite
		self.z = Battle_Drawing_Layers['name']
		self.col = COLORS['black']
		self.font = font
		self.pos = pos

		text_surf = self.font.render(self.monster_sprite.monster.name, False, self.col)
		padding = 10

		self.image = pygame.Surface((text_surf.get_width(), text_surf.get_height() + padding), flags=pygame.SRCALPHA)

		self.image.fill((0, 0, 0, 0))
		self.image.blit(text_surf, (0, padding))
		self.rect = self.image.get_frect(midleft=self.pos)

	def update(self, _):
		text_surf = self.font.render(self.monster_sprite.monster.name, False, self.col)
		padding = 10

		self.image = pygame.Surface((text_surf.get_width(), text_surf.get_height() + padding), flags=pygame.SRCALPHA)

		self.image.fill((0, 0, 0, 0))
		self.image.blit(text_surf, (0, padding))
		self.rect = self.image.get_frect(midleft=self.pos)

		if not self.monster_sprite.groups():
			self.kill()

class MonsterLevelSprite(pygame.sprite.Sprite):
  def __init__(self,entity,corner,monster_sprite,groups,font):
    super().__init__(groups)
    self.monster_sprite=monster_sprite
    self.font=font
    self.z = Battle_Drawing_Layers['name']
    self.col=COLORS['black']

    self.image=pygame.Surface((60,26),flags=pygame.SRCALPHA)
    self.image.fill((0, 0, 0, 0))

    self.rect=self.image.get_frect(topleft =corner) if entity =='player' else self.image.get_frect(topright=corner)
    # 经验条紧贴着 self.rect 的底部，留出2单位的高度
    self.xp_rect = pygame.FRect(0, self.rect.height - 2, self.rect.width, 2)


  def update(self,_):
    text_surf = self.font.render(f'Lvl {self.monster_sprite.monster.level}', False, self.col)
    text_rect = text_surf.get_frect(center=(self.rect.width / 2, self.rect.height / 2-2))
    self.image.blit(text_surf, text_rect)


    draw_bar(self.image, self.xp_rect, self.monster_sprite.monster.xp, self.monster_sprite.monster.level_up,
            COLORS['white'], COLORS['black'])

    if not self.monster_sprite.groups():
      self.kill()

class MonsterStatsSprite(pygame.sprite.Sprite):
    def __init__(self,pos,monster_sprite,size,groups,font):
        super().__init__(groups)

        self.monster_sprite=monster_sprite
        self.z = Battle_Drawing_Layers['layer']
        self.col=COLORS['white']

        self.image = pygame.Surface(size,flags=pygame.SRCALPHA)
        self.image.set_alpha(240)

        self.rect = self.image.get_frect(midbottom=pos)
        self.font = font

    def update(self,dt):
        self.monster_sprite.monster.update(dt)
        self.image.fill(self.col)
        for index, (value, max_value) in enumerate(self.monster_sprite.monster.get_info()):
            color = (COLORS['red'], COLORS['blue'], COLORS['gray'])[index]
            if index < 2:  
								# health and energy
                text_surf = self.font.render(f'{int(value)}/{max_value}', False, COLORS['black'])
                text_rect = text_surf.get_frect(topleft=(self.rect.width * 0.05, index * self.rect.height / 2))
                bar_rect = pygame.FRect(text_rect.bottomleft + vector(0, -2), (self.rect.width * 0.9, 4))

                self.image.blit(text_surf, text_rect)
                draw_bar(self.image, bar_rect, value, max_value, color, COLORS['black'])

            else:  # preparation
                init_rect = pygame.FRect((0,self.rect.height - 2), (self.rect.width, 2))
                draw_bar(self.image, init_rect, value, max_value, color, COLORS['white'], 0)

        if not self.monster_sprite.groups():
            self.kill()
