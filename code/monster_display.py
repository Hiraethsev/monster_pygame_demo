from data_set import *
from data_import import *

class BelowDisplay:
    def __init__(self):
        self.display_surf = pygame.display.get_surface()
  

        # tint surf
        self.tint_surf = pygame.Surface((1280, 30))
        self.tint_surf.fill((255, 255, 255))

        self.font = Fonts['regular']
        self.text_color = COLORS['black']
        self.fontpos = (1280 - 150, 720 - 30)



    def update(self, monster_display_open=False):
        self.display_surf.blit(self.tint_surf, (0, 720 - 30))
        if monster_display_open:
            self.text = "SPACE-交换精灵顺序   ENTER-返回"
            self.fontpos = (1280 - 320, 720 - 30)
        else:
            self.text = "SPACE-进入对话  ENTER-进入面板"
            self.fontpos = (1280 - 300, 720 - 30)

        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.display_surf.blit(self.text_surface, self.fontpos)


class MonsterDisplay:
	def __init__(self, monsters, monster_frames):
		self.display_surf = pygame.display.get_surface()
		self.monsters = monsters
		self.frame_index = 0

		# 图像
		self.icon_frames = monster_frames['icons']
		self.monster_frames = monster_frames['monsters']
		self.ui_frames = monster_frames['ui']

		# 背景的带透明度的表面 
		self.tint_surf = pygame.Surface((1280, 720))
		self.tint_surf.set_alpha(200)

		# 中间有内容部分
		self.main_rect = pygame.FRect(0,0,1280 * 0.6,720 * 0.8).move_to(center = (1280 / 2, 720 / 2))

		# 列表选择
		self.visible_items = 6
		self.list_width = self.main_rect.width * 0.3
		self.item_height = self.main_rect.height / self.visible_items
		self.index = 0
		self.selected_index = None

		# 最大值参考
		self.max_stats = {}
		for data in Monster_Data.values():
			for stat, value in data['stats'].items():
				if stat != 'element':
					if stat not in self.max_stats:
						self.max_stats[stat] = value
					else:
						self.max_stats[stat] = value if value > self.max_stats[stat] else self.max_stats[stat]


	def input(self):
		keys = pygame.key.get_just_pressed()
		if keys[pygame.K_UP]:
			self.index -= 1
		if keys[pygame.K_DOWN]:
			self.index += 1
		if keys[pygame.K_SPACE]:
			if self.selected_index != None:
				selected_monster = self.monsters[self.selected_index]
				current_monster  = self.monsters[self.index]
				self.monsters[self.index] = selected_monster
				self.monsters[self.selected_index] = current_monster
				self.selected_index = None
			else:
				self.selected_index = self.index

		self.index = self.index % len(self.monsters)

	# 在游戏的显示表面上绘制文本
	def draw_surf(self, text, base, position, pos, font=Fonts['bold'], color=COLORS['white'], relative=None):
		if isinstance(font, tuple):
			raise TypeError(f"Expected font to be a pygame.font.Font object, got {type(font)} instead.")
		surf = font.render(str(text), False, color)
		rect = self.calculate_rect(surf, base, position, pos, relative)
		self.display_surf.blit(surf, rect)
		return rect

	# 矩形位置计算方法
	def calculate_rect(self, surf, base, position, pos, relative):
		positions = {
			'topleft': base.topleft + vector(pos[0], pos[1]),
			'bottomleft': base.topleft + vector(pos[0], pos[1]) if relative == 'topleft' else base.bottomleft + vector(
				pos[0], pos[1]),
			'bottomright': base.bottomright + vector(pos[0], pos[1]),
			'midleft': base.topleft + vector(pos[0], pos[1]) if relative == 'topleft' else base.midleft + vector(pos[0],
																												 pos[1])
		}
		return surf.get_frect(**{position: positions[position]})

	# 显示左侧怪兽列表
	def display_list(self):
		if self.index < self.visible_items:
			v_offset = 0
		else:
			v_offset = -(self.index - self.visible_items + 1) * self.item_height

		for index, monster in self.monsters.items():
			if self.index == index:
				bg_color = COLORS['light-blue']
			else:
				bg_color = COLORS['light']

			if self.selected_index == index:
				text_color = COLORS['light-yellow']
			else:
				text_color = COLORS['white']

			top = self.main_rect.top + index * self.item_height + v_offset
			item_rect = pygame.FRect(self.main_rect.left, top, self.list_width, self.item_height)


			# 检测两个矩形是否相交=>是否显示
			if item_rect.colliderect(self.main_rect):
				pygame.draw.rect(self.display_surf, bg_color, item_rect)
				# text
				self.draw_surf(monster.name, item_rect, 'midleft', (85, 0), Fonts['monster_name'],text_color)

				icon_surf = self.icon_frames[monster.name]
				icon_rect = icon_surf.get_frect(center=item_rect.midleft + vector(40, 0))
				self.display_surf.blit(icon_surf, icon_rect)


	def display_main(self, dt):
		monster = self.monsters[self.index]

		# 总体部分背景
		rect = pygame.FRect(self.main_rect.left + self.list_width, self.main_rect.top,
							self.main_rect.width - self.list_width + 5, self.main_rect.height)

		pygame.draw.rect(self.display_surf, COLORS['gray'], rect)

		# 上边部分
		# 背景
		top_rect = pygame.FRect(rect.topleft, (rect.width, rect.height * 0.4))
		pygame.draw.rect(self.display_surf, COLORS[monster.element], top_rect)

		# 动画
		self.frame_index += 6* dt
		monster_surf = self.monster_frames[monster.name]['idle'][
			int(self.frame_index) % len(self.monster_frames[monster.name]['idle'])]
		# 创建rect对象，其center值为背景的center值
		monster_rect = monster_surf.get_frect(center=top_rect.center)
		self.display_surf.blit(monster_surf, monster_rect)

		# 怪兽名字
		self.draw_surf(monster.name, top_rect, 'topleft', (10,10))
		# 怪兽等级
		level_rect=self.draw_surf( f'Lv:{monster.level}', top_rect, 'bottomleft', (10, -15),Fonts['monster_name'])
		# 怪兽属性
		self.draw_surf(monster.element, top_rect, 'bottomright', (-10, -7),Fonts['monster_name'])


		# 等级经验
		draw_bar(self.display_surf, pygame.FRect(level_rect.bottomleft + vector(-2, 3), (100, 4)), monster.xp,
				 monster.level_up, COLORS['white'], COLORS['dark'])


		# 下面部分
		bar_data = {
			'width': rect.width * 0.45,
			'height': 30,
			'top': top_rect.bottom + rect.width * 0.05,
			'left_side': rect.left + rect.width / 4,
			'right_side': rect.left + rect.width * 3 / 4
		}

		# 生命条
		healthbar_rect = pygame.FRect((0, 0), (bar_data['width'], bar_data['height'])).move_to(
			midtop=(bar_data['left_side'], bar_data['top']))
		draw_bar(self.display_surf, healthbar_rect, monster.current_health, monster.status['max_health'], COLORS['red'],
				 COLORS['dark'])


		hp_display_text=f"HP: {int(monster.current_health)}/{int(monster.status['max_health'])}"
		self.draw_surf(hp_display_text, healthbar_rect, 'midleft', (10, 0), Fonts['monster_name'])

		# 能量条
		energybar_rect = pygame.FRect((0, 0), (bar_data['width'], bar_data['height'])).move_to(
			midtop=(bar_data['right_side'], bar_data['top']))
		draw_bar(self.display_surf, energybar_rect, monster.current_energy,  monster.status['max_energy'], COLORS['blue'],
				 COLORS['dark'])

		ep_display_text = f"EP: {int(monster.current_energy)}/{int(monster.status['max_energy'])}"
		self.draw_surf(ep_display_text, energybar_rect, 'midleft', (10, 0), Fonts['monster_name'])


		# 状态和技能的信息
		sides = {'left': healthbar_rect.left, 'right': energybar_rect.left}
		info_height = rect.bottom - healthbar_rect.bottom

		# 状态
		stats_rect = pygame.FRect(sides['left'], healthbar_rect.bottom, healthbar_rect.width, info_height).inflate(0,-60).move(0, 5)

		self.draw_surf('Status', stats_rect, 'bottomleft', (10, 0),  Fonts['monster_name_large'],COLORS['white'],'topleft')


		stat_height = stats_rect.height / len(monster.status)

		for index, (stat, value) in enumerate(monster.status.items()):
			single_stat_rect = pygame.FRect(stats_rect.left, stats_rect.top + index * stat_height, stats_rect.width,
											stat_height)

			# 图标
			icon_surf = self.ui_frames[stat]
			icon_rect = icon_surf.get_frect(midleft=single_stat_rect.midleft + vector(5, 0))
			self.display_surf.blit(icon_surf, icon_rect)

			# 文字
			text_rect=self.draw_surf(stat, icon_rect, 'topleft', (30, -12), Fonts['monster_name'])


			# bar
			bar_rect = pygame.FRect((text_rect.left, text_rect.bottom + 2),(single_stat_rect.width - (text_rect.left - single_stat_rect.left) - 10, 4))

			draw_bar(self.display_surf, bar_rect, value, self.max_stats[stat] * monster.level, COLORS['white'],
					 COLORS['dark'])

			# 技能
			ability_rect = stats_rect.copy().move_to(left=sides['right'])

			self.draw_surf('Ability', ability_rect, 'bottomleft', (0, 0), Fonts['monster_name_large'], COLORS['white'],'topleft')


			for index, ability in enumerate(monster.get_abilities()):
				element = Attack_Data[ability]['element']

				text_surf = Fonts['monster_name'].render(ability, False, COLORS['black'])
				x = ability_rect.left + 5
				y = 20 + ability_rect.top + index * (text_surf.get_height() + 20)

				rect = text_surf.get_frect(topleft=(x, y))
				pygame.draw.rect(self.display_surf, COLORS[element], rect.inflate(10, 10), 0, 4)
				self.display_surf.blit(text_surf, rect)

	def update(self, dt):
		# input
		self.input()
		
		self.display_surf.blit(self.tint_surf, (0, 0))
		pygame.draw.rect(self.display_surf, '#f2f2f2', self.main_rect)

		self.display_list()
		self.display_main(dt)