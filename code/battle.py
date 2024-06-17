from sprites import *
from monster_battle_sprites import *
from groups import BattleSprites
from data_import import *
from import_method import draw_bar
from timer import Timer
from random import choice

class Battle:
	# main
	def __init__(self, player_monsters, opponent_monsters, monster_frames, bg_surf, end_battle, character):
		# general
		self.display_surface = pygame.display.get_surface()
		self.bg_surf = bg_surf
		self.monster_frames = monster_frames
		self.monster_data = {'player': player_monsters, 'opponent': opponent_monsters}

		self.width, self.height = 1280 * 0.8, 150
		self.text = ''
		self.bg_rect = pygame.FRect((0, 0), (self.width, self.height)).move_to(
			midbottom=(1280 / 2, 720 - 30))

		self.battle_over = False
		self.end_battle = end_battle
		# 当前参与战斗的角色对象
		self.character = character


		# timers 
		self.timers = {
			'opponent delay': Timer(600, func = self.opponent_attack)
		}

		# groups
		self.battle_sprites   = BattleSprites()
		self.player_sprites   = pygame.sprite.Group()
		self.opponent_sprites = pygame.sprite.Group()

		# control
		self.current_monster = None
		self.selection_mode  = None
		self.selected_attack = None
		self.selection_side  = 'player'
		#  不同选择模式下的索引初始化为 0
		self.indexes = {
			'general': 0,
			'monster': 0,
			'attack': 0,
			'switch' : 0,
			'target' : 0,
		}

		self.setup()

	def setup(self):
		for entity, monsters in self.monster_data.items():
			# 筛选出索引小于等于2的怪物,确保每一方最多有 3 个怪兽参加战斗
			selected_monsters = {}
			for k, v in monsters.items():
				if int(k) <= 2:
					selected_monsters[int(k)] = v

			# 创建怪物
			for index, monster in selected_monsters.items():
				self.create_monster(monster, int(index), int(index), entity)

			# 清除已经添加到 self.opponent_sprites 的怪物数据
			for i in range(len(self.opponent_sprites)):
					if str(i) in self.monster_data['opponent']:
						del self.monster_data['opponent'][str(i)]

	def create_monster(self, monster, index, pos_index, entity):
		monster.paused = False
		frames = self.monster_frames['monsters'][monster.name]


		if entity == 'player':
			pos = list(BattleMosterPos['left'].values())[pos_index]
			groups = (self.battle_sprites, self.player_sprites)

			# 翻转玩家怪物的动画帧，使其面向对手
			frames = {state: [pygame.transform.flip(frame, True, False) for frame in frames] for state, frames in frames.items()}

		else:
			pos = list(BattleMosterPos['right'].values())[pos_index]
			groups = (self.battle_sprites, self.opponent_sprites)

		 # 检查是否已经存在相同位置的怪物，避免重复添加
		for sprite in groups[1]:  
        # groups[1] 是 player_sprites 或 opponent_sprites
			if sprite.pos_index == pos_index:
				print(f"Warning: Trying to add a monster at an already occupied position {pos_index}")
				return
			
		# 创建怪物精灵
		monster_sprite = MonsterSprite(pos, frames, groups, monster, index, pos_index, entity, self.apply_attack, self.create_monster)


		# 创建怪物的UI元素
		# 名字
		name_pos = monster_sprite.rect.midleft + vector(-30,-70) if entity == 'player' else monster_sprite.rect.midright + vector(-40, -70)
		name_sprite = MonsterNameSprite(name_pos, monster_sprite, self.battle_sprites, Fonts['monster_name'])

		# 等级
		# 设置UI元素的位置
		corner = name_sprite.rect.bottomleft if entity == 'player' else name_sprite.rect.bottomright
		MonsterLevelSprite(entity, corner, monster_sprite, self.battle_sprites, Fonts['monster_name_mini'])

		# 状态
		MonsterStatsSprite(monster_sprite.rect.midbottom + vector(0,20), monster_sprite, (150,50), self.battle_sprites, Fonts['monster_name_mini'])

	def input(self):
		# 确保当前有选择模式并且当前怪物不为空
		if self.selection_mode and self.current_monster:
			# 获取当前按下的键
			keys = pygame.key.get_just_pressed()

			# 根据不同的选择模式设置限制器
			match self.selection_mode:
				case 'general': limiter = len(BattleChoice)
				# 当前怪物可用的技能数量
				case 'attack': limiter = len(self.current_monster.monster.get_abilities(all = False))
				case 'switch': limiter = len(self.available_monsters)
				case 'target': limiter = len(self.opponent_sprites) if self.selection_side == 'opponent' else len(self.player_sprites)
				
			
			if limiter!=0:
			# 处理方向键输入（上下左右移动光标）
				if self.selection_mode == 'general' or self.selection_mode == 'target':
					if keys[pygame.K_DOWN]:
						self.indexes[self.selection_mode] = (self.indexes[self.selection_mode] + 1) % limiter
					if keys[pygame.K_UP]:
						self.indexes[self.selection_mode] = (self.indexes[self.selection_mode] - 1) % limiter
				else:
					if keys[pygame.K_RIGHT]:
						self.indexes[self.selection_mode] = (self.indexes[self.selection_mode] + 1) % limiter
					if keys[pygame.K_LEFT]:
						self.indexes[self.selection_mode] = (self.indexes[self.selection_mode] - 1) % limiter

			# 处理空格键输入（确认选择）
			if keys[pygame.K_SPACE]:

				# 切换怪物
				# 如果选择模式是切换，获取新怪物的数据，移除当前怪物，并创建新怪物。
				if self.selection_mode == 'switch':
					index, new_monster = list(self.available_monsters.items())[self.indexes['switch']]

					self.current_monster.kill()

					self.create_monster(new_monster, index, self.current_monster.pos_index, 'player')

					self.selection_mode = None
					self.update_all_monsters('continue')

				# 选择目标
				if self.selection_mode == 'target':
					# 获取目标怪物组并根据当前选择的索引获取目标怪物。
					sprite_group = self.opponent_sprites if self.selection_side == 'opponent' else self.player_sprites

					sprites = {sprite.pos_index: sprite for sprite in sprite_group}
					monster_sprite = sprites[list(sprites.keys())[self.indexes['target']]]

					# 如果选择了攻击，执行攻击并重置选择状态
					if self.selected_attack:
						self.current_monster.activate_attack(monster_sprite, self.selected_attack)
						self.selected_attack, self.current_monster, self.selection_mode = None, None, None
					else:
						if monster_sprite.monster.current_health < monster_sprite.monster.status['max_health'] * 0.5:
							self.monster_data['player'][len(self.monster_data['player'])] = monster_sprite.monster
							monster_sprite.delayed_kill(None)
							self.update_all_monsters('continue')
						else:
							DisplayShortSprite(monster_sprite.rect.center, self.monster_frames['ui']['cross'], self.battle_sprites, 1000)

				# 如果选择模式是攻击，更新选择模式为目标，并设置当前选择的攻击技能和目标。
				if self.selection_mode == 'attack':
					self.selection_mode = 'target'

					self.selected_attack = self.current_monster.monster.get_abilities(all = False)[self.indexes['attack']]

					self.selection_side = Attack_Data[self.selected_attack]['target']

				#在通用选择模式下，根据选择索引执行不同的操作，如攻击、防御、切换怪物或选择目标
				if self.selection_mode == 'general':
					if self.indexes['general'] == 0:
						self.selection_mode = 'attack'
					
					if self.indexes['general'] == 1:
						# 设置当前怪物为防御状态
						self.current_monster.monster.defending = True
						self.update_all_monsters('continue')
						self.current_monster, self.selection_mode = None, None
						self.indexes['general'] = 0
					
					if self.indexes['general'] == 2:
						self.selection_mode = 'switch'

					if self.indexes['general'] == 3:
						self.selection_mode = 'target'
						self.selection_side = 'opponent'
				# 重置选择索引
				self.indexes = {k: 0 for k in self.indexes}

			#处理退格键输入（返回上一级菜单）
			if keys[pygame.K_BACKSPACE]:
				if self.selection_mode in ('attack', 'switch','target'):
					self.selection_mode = 'general'

			if keys[pygame.K_ESCAPE]:
				self.end_battle(None,None)

	def update_timers(self):
		for timer in self.timers.values():
			timer.update()

	# battle system
	# 这个函数检查当前哪个怪物可以进行行动。
	def check_active(self):
		for monster_sprite in self.player_sprites.sprites() + self.opponent_sprites.sprites():
			if monster_sprite.monster.preparation >= 100:
				monster_sprite.monster.defending = False
				self.update_all_monsters('pause')
				monster_sprite.monster.preparation = 0
				monster_sprite.set_highlight(True)
				self.current_monster = monster_sprite

				if self.player_sprites in monster_sprite.groups():
					self.selection_mode = 'general'
				else:
					# 激活对手的定时器,触发opponent_attack
					self.timers['opponent delay'].activate()

	# 根据给定的选项暂停或恢复所有怪物的行动
	def update_all_monsters(self, status):
		for monster_sprite in self.player_sprites.sprites() + self.opponent_sprites.sprites():
			monster_sprite.monster.paused = True if status == 'pause' else False

	# 应用攻击效果，计算并更新目标怪物的健康值。
	def apply_attack(self, target_sprite, attack, amount):
		AttackSprite(target_sprite.rect.center, self.monster_frames['attack'][Attack_Data[attack]['animation']], self.battle_sprites)

		pygame.mixer.Sound(f'../sounds/{Attack_Data[attack]["animation"]}.wav').play()

		# 攻击和被攻击方的属性
		attack_element = Attack_Data[attack]['element']
		target_element = target_sprite.monster.element

		# 根据属性克制关系计算攻击数值
		if attack_element == 'fire'  and target_element == 'plant' or attack_element == 'water' and target_element == 'fire'  or attack_element == 'plant' and target_element == 'water':
			amount *= 1.2

		if attack_element == 'fire'  and target_element == 'water' or attack_element == 'water' and target_element == 'plant' or attack_element == 'plant' and target_element == 'fire':
			amount *= 0.8

		#计算防御相关
		target_defense = 1 - target_sprite.monster.status['defense'] / 2000
		if target_sprite.monster.defending:
			target_defense -= 0.3
		target_defense = max(0, min(1, target_defense))

		# 更新血量
		target_sprite.monster.current_health -= amount * target_defense
		if target_sprite.monster.current_health<0:
			target_sprite.monster.current_health=0

		self.check_death()

		self.update_all_monsters('continue')

	# 检查怪物是否死亡
	def check_death(self):
		# 遍历所有怪物精灵
		all_monsters = self.opponent_sprites.sprites() + self.player_sprites.sprites()
		for monster_sprite in all_monsters:
			if monster_sprite.monster.current_health <= 0:
				if self.player_sprites in monster_sprite.groups():
					self.handle_player_monster_death(monster_sprite)
				else:
					self.handle_opponent_monster_death(monster_sprite)

	def handle_player_monster_death(self, monster_sprite):
    # 获取当前活动的玩家怪物
		active_monsters = [(ms.index, ms.monster) for ms in self.player_sprites.sprites()]

    # 获取可用的（未死亡的）玩家怪物
    # 提取当前活动怪物的索引
		active_monster_indices = {index for index, monster in active_monsters}

    # 过滤出可用的怪物
		available_monsters = [
        (index, monster) for index, monster in self.monster_data['player'].items()
        if monster.current_health > 0 and index not in active_monster_indices
    ]

    # 选择一个替换的怪物
		if available_monsters:
			new_monster_data = available_monsters[0][1],available_monsters[0][0], monster_sprite.pos_index, 'player'
		else:
			new_monster_data = None

    # 延迟删除怪物精灵
		monster_sprite.delayed_kill(new_monster_data)


	def handle_opponent_monster_death(self, monster_sprite):
		monster_pos_index = monster_sprite.pos_index
		monster_sprite.delayed_kill(None)

    # 获取新的对手怪物数据
		if self.monster_data['opponent']:
			new_monster_index = next(iter(self.monster_data['opponent'].keys()))
			new_monster = self.monster_data['opponent'][new_monster_index]
			del self.monster_data['opponent'][new_monster_index]
			self.create_monster(new_monster, new_monster_index, monster_pos_index, 'opponent')
		else:
			self.update_all_monsters('continue')

    # 分配经验值给玩家的怪物
		xp_amount = monster_sprite.monster.level * 100 / len(self.player_sprites)
		for ele in self.player_sprites:
			ele.monster.update_xp(xp_amount)


	# 对手的怪物随机选择一个技能并攻击目标
	def opponent_attack(self):
		# 从当前怪物的技能中随机选择一个
		ability = choice(self.current_monster.monster.get_abilities())

		# 根据技能的目标类型，随机选择一个目标
		if Attack_Data[ability]['target'] == "opponent":
			random_target = choice(self.player_sprites.sprites())
		else:
			random_target = choice(self.opponent_sprites.sprites())


		# 执行攻击
		self.current_monster.activate_attack(random_target, ability)

	# 检查战斗是否结束
	def check_end_battle(self):
		# 玩家 win
		if len(self.opponent_sprites) == 0 and not self.battle_over:
			self.battle_over = True
			self.end_battle(self.character,True)
			for monster in self.monster_data['player'].values():
				monster.preparation = 0

		# 玩家 defeated,跳转到医院
		if len(self.player_sprites) == 0:
			self.battle_over = True
			self.end_battle(None,False)
			for monster in self.monster_data['player'].values():
				monster.preparation = 0


	# ui
	def update_text(self, stats):
		pygame.draw.rect(self.display_surface, COLORS['pure white'], self.bg_rect, 0, 5)
		if stats == 'general':
			self.text = f'请选择对精灵{self.current_monster.monster.name}的操作'
			text_surf = Fonts['monster_choice_large'].render(self.text, False, COLORS['black'])
			text_rect = text_surf.get_frect(center=self.bg_rect.center)
			self.display_surface.blit(text_surf, text_rect)
		if stats == 'attack':
			self.text = f'请选择精灵{self.current_monster.monster.name}的攻击技能'

		if stats == 'switch':
			self.text = f'请选择要替换{self.current_monster.monster.name}上场的精灵'

		if stats == 'switch' or stats == 'attack':
			text_surf = Fonts['monster_choice_middle'].render(self.text, False, COLORS['black'])
			text_rect = text_surf.get_frect(topleft=self.bg_rect.topleft + vector(20, 10))

			self.text1 = 'BS-返回'
			text_surf1 = Fonts['monster_choice_mini'].render(self.text1, False, COLORS['black'])
			text_rect1 = text_surf1.get_frect(bottomright=self.bg_rect.bottomright + vector(-10, -5))

			for surf, rect in ((text_surf, text_rect), (text_surf1, text_rect1)):
				self.display_surface.blit(surf, rect)

	def draw_ui(self):
		if self.current_monster:
			if self.selection_mode == 'general':
				if self.current_monster in self.player_sprites.sprites():
					self.draw_general()
			if self.selection_mode == 'attack':
				self.draw_attacks()
			if self.selection_mode == 'switch':
				self.draw_switch()

	def draw_general(self):
		self.update_text('general')
		#根据当前的选择状态，显示不同的图标高亮
		for index, (_, data_dict) in enumerate(BattleChoice.items()):
			if index == self.indexes['general']:
				surf = self.monster_frames['ui'][f"{data_dict['icon']}_highlight"]
			else:
				surf = pygame.transform.grayscale(self.monster_frames['ui'][data_dict['icon']])

			rect = surf.get_frect(center = self.current_monster.rect.midright + data_dict['pos'])
			self.display_surface.blit(surf, rect)

	def draw_attacks(self):
		# data
		abilities = self.current_monster.monster.get_abilities(all = False)
		width, height = 150, 40
		visible_attacks = 4
		item_width = self.width / visible_attacks
		v_offset = 0 if self.indexes['attack'] < visible_attacks else -(self.indexes['attack'] + 1 - visible_attacks) * item_width

		# bg
		self.update_text('attack')

		for index, ability in enumerate(abilities):
			selected = index == self.indexes['attack']
			element = Attack_Data[ability]['element']
			# text 
			if selected:
				text_surf_color = COLORS[element] if element != 'normal' else '#6e6e6e'
				text_color = COLORS['white']
			else:
				text_color = COLORS[element] if element != 'normal' else COLORS['black']
				text_surf_color = COLORS['dark white']

			text_surf=Fonts['monster_name'].render(ability, False, text_color)

			# rect 
			text_rect = text_surf.get_frect(
				center=self.bg_rect.midleft + vector(item_width / 2 + index * item_width + v_offset, 0))
			text_bg_rect = pygame.FRect((0, 0), (item_width * 0.8, height)).move_to(center=text_rect.center)

			# draw
			if self.bg_rect.collidepoint(text_rect.center):
				pygame.draw.rect(self.display_surface, text_surf_color, text_bg_rect, 0, 0, 5, 5, 5, 5)

				self.display_surface.blit(text_surf, text_rect)

	def draw_switch(self):
		# data 
		width, height = 150, 40
		visible_monsters = 4
		item_width = self.width / visible_monsters
		v_offset = 0 if self.indexes['switch'] < visible_monsters else -(self.indexes['switch'] - visible_monsters + 1) * item_width


		# monsters 
		active_monsters = [(monster_sprite.index, monster_sprite.monster) for monster_sprite in self.player_sprites]
		self.available_monsters = {index: monster for index, monster in self.monster_data['player'].items() if (index, monster) not in active_monsters and monster.current_health > 0}

		self.update_text('switch')

		for index, monster in enumerate(self.available_monsters.values()):
			selected = index == self.indexes['switch']

			if selected:
				text_surf_color = '#6e6e6e'
				text_color = COLORS['white']
			else:
				text_color = COLORS['black']
				text_surf_color = COLORS['dark white']			


			icon_surf = self.monster_frames['icons'][monster.name]
			icon_rect = icon_surf.get_frect(center=self.bg_rect.midleft + vector(item_width / 2 + index * item_width + v_offset-75, 0))

			text_surf = Fonts['monster_name'].render(f'{monster.name} ({monster.level})', False, text_color)
			text_rect = text_surf.get_frect(center=self.bg_rect.midleft + vector(item_width / 2 + index * item_width + v_offset+10, 0))
			text_bg_rect = pygame.FRect((0, 0), (item_width*0.85, height*1.5)).move_to(center=text_rect.center)



			if self.bg_rect.collidepoint(text_rect.center):
				pygame.draw.rect(self.display_surface, text_surf_color, text_bg_rect, 0, 0, 5, 5, 5, 5)
				for surf, rect in ((icon_surf, icon_rect), (text_surf, text_rect)):
					self.display_surface.blit(surf, rect)

				health_rect = pygame.FRect((text_rect.bottomleft + vector(0,4)), (100,4))
				energy_rect = pygame.FRect((health_rect.bottomleft + vector(0,2)), (100,4))

				draw_bar(self.display_surface, health_rect, monster.current_health, monster.status['max_health'], COLORS['red'], COLORS['black'])

				draw_bar(self.display_surface, energy_rect, monster.current_energy, monster.status['max_energy'], COLORS['blue'], COLORS['black'])

	def update(self, dt):
		self.check_end_battle()
		
		# updates
		self.input()
		self.update_timers()
		self.battle_sprites.update(dt)
		self.check_active()

		# drawing
		self.display_surface.blit(self.bg_surf, (0,0))
		self.battle_sprites.draw(self.current_monster, self.selection_side, self.indexes['target'], self.player_sprites, self.opponent_sprites)
		self.draw_ui()