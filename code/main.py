from random import randint
# 精灵类
# 静态、动画精灵、怪物区域、边界、可碰撞、跳转
from sprites import *
# 玩家,NPC
from entities import Player, Character
# 所有精灵组
from groups import AllSprites
# 对话类
from dialog import DialogPara
# 怪物
from monster_display import *
# 战斗
from battle import Battle
from timer import Timer
from monster import *

class Game:
	# 总体设置
	def __init__(self):
		pygame.init()
		# 创建一个指定大小的游戏窗口，并赋值给 Game 类的 display_surface 属性
		self.display_surface =Display_Surface
		pygame.display.set_caption('口袋精灵demo')
		# 通过一个时钟对象，控制游戏的帧速率
		self.clock = pygame.time.Clock()
		# 每隔 2000 毫秒调用一次monster_encounter
		self.encounter_timer = Timer(2000, func = self.monster_encounter)

		# 初始化玩家的怪物数据
		self.player_monsters =update_player_monster()


		# 加载地图等数据
		self.tmx_maps = Tmx_Maps

		self.overworld_frames = Overworld_Frames
		self.monster_frames = Monster_Frames


		self.bg_frames = Bg_Frames
		# 加载开始动画帧数据
		self.start_animation_frames = Start_Animation_Frames
		

		# 创建精灵组，保存所有游戏中的精灵对象
		self.all_sprites = AllSprites()
		# 识别可碰撞的类
		self.collision_sprites = pygame.sprite.Group()
		# 识别所有NPC
		self.character_sprites = pygame.sprite.Group()
		# 识别所有的跳转图层
		self.transition_sprites = pygame.sprite.Group()

		self.monster_sprites = pygame.sprite.Group()

		# 跳转、显示
		self.transition_target = None
		self.tint_surf = pygame.Surface((1280, 720))
		self.scene_status = 'untint'
		self.tint_progress = 0
		self.tint_direction = -1
		self.tint_speed = 600

		# 对话
		self.dialog_para = None

		# 显示
		self.monster_display = MonsterDisplay(self.player_monsters, self.monster_frames)
		self.monster_display_open = False
		self.index_open = False
		self.battle = None
		self.evolution = None

		self.below_display = BelowDisplay()

		# 设置起始点和音频
		self.player = None
		self.setuppos(self.tmx_maps['world'], 'house')
		pygame.mixer.music.load('../music/world.mp3')
		pygame.mixer.music.play(-1)



	def setuppos(self, map, player_start_pos):
		#清除原有的精灵组等
		for ele in (self.all_sprites, self.collision_sprites, self.transition_sprites, self.character_sprites):
			ele.empty()

		# 创造的顺序决定了覆盖的层次=>给每个精灵一个图层来渲染
		# 获取地形层，并遍历这个层中的所有方块
		# 这里的x，y是方块的位置而非像素
		for x, y, surface in map.get_layer_by_name('Terrain').tiles():
			Sprite((x * 64, y * 64), surface, self.all_sprites, Layer_Z_Index['background'])

		for x, y, surface in map.get_layer_by_name('Terrain Top').tiles():
			Sprite((x * 64, y * 64), surface, self.all_sprites, Layer_Z_Index['background'])

		# water 
		for obj in map.get_layer_by_name('Water'):
			for x in range(int(obj.x), int(obj.x + obj.width), 64):
				for y in range(int(obj.y), int(obj.y + obj.height), 64):
					AnimatedSprite((x,y), self.overworld_frames['water'], self.all_sprites, Layer_Z_Index['water'])

		# coast
		for obj in map.get_layer_by_name('Coast'):
			AnimatedSprite((obj.x, obj.y), self.overworld_frames['coast'][obj.properties['terrain']][obj.properties['side']], self.all_sprites, Layer_Z_Index['background'])
		
		# objects 
		for obj in map.get_layer_by_name('Objects'):
			if obj.name == 'top':
				Sprite((obj.x, obj.y), obj.image, self.all_sprites, Layer_Z_Index['top'])
			else:
				CollideSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites),True)

		# transition objects
		for obj in map.get_layer_by_name('Transition'):
			TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']), self.transition_sprites)

		# collision objects 
		for obj in map.get_layer_by_name('Collisions'):
			CollideSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites,False)

		# grass patches 
		for obj in map.get_layer_by_name('Monsters'):
			MonsterPatchSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.monster_sprites), obj.properties['biome'], obj.properties['monsters'], obj.properties['level'])

		# entities 
		for obj in map.get_layer_by_name('Entities'):
			if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
				self.player = Player((obj.x, obj.y),
				self.overworld_frames['characters']['player'],
				self.all_sprites,obj.properties['direction'],
				self.collision_sprites)
			elif obj.name == 'Character':
				Character((obj.x, obj.y),self.overworld_frames['characters'][obj.properties['graphic']],(self.all_sprites, self.collision_sprites, self.character_sprites),obj.properties['direction'],NPC_Data[obj.properties['character_id']],self.player,self.create_dialog,
					self.collision_sprites,
					obj.properties['radius'],
					obj.properties['character_id'] == 'Nurse'
					)

	#对话系统
	def input(self):
		# 实时检测玩家是否按下某个键
		# get_just_pressed 检测键盘上的某个键是否在当前帧刚刚被按下，而在前一帧未被按下,只有在某个键从未按下变为按下的瞬间，相应的元素值才为 True
		if not self.dialog_para and not self.battle:
			keys = pygame.key.get_just_pressed()

			if keys[pygame.K_SPACE]:
				for character in self.character_sprites:
					if check_distance(100, self.player, character):
						# 阻止输入
						self.player.block()
						# NPC面向玩家
						character.change_facing_direction(self.player.rect.center)
						# 对话
						self.create_dialog(character)
						

			if keys[pygame.K_RETURN]:
				self.monster_display_open=not self.monster_display_open
				self.player.blocked = not self.player.blocked


	def create_dialog(self, character):
		if not self.dialog_para:
			self.dialog_para = DialogPara(character, self.player, self.all_sprites, self.end_dialog)

	def end_dialog(self, character):
		self.dialog_para = None
		if character.nurse:
			for monster in self.player_monsters.values():
				monster.current_health = monster.status['max_health']
				monster.current_energy = monster.status['max_energy']

			self.player.unblock()
		elif not character.character_data['defeated']:
			pygame.mixer.music.stop()  # 停止当前播放的音乐
			pygame.mixer.music.load('../music/battle.mp3')  # 加载新的音乐文件
			pygame.mixer.music.play(-1)  # 循环播放新音乐
			self.transition_target = Battle(
				player_monsters = self.player_monsters, 
				opponent_monsters = character.monsters, 
				monster_frames = self.monster_frames, 
				bg_surf = self.bg_frames[character.character_data['biome']],  
				end_battle = self.end_battle,
				character = character)
			self.scene_status = 'tint'
		else:
			self.player.unblock()
			self.check_evolution()

	# 页面跳转
	def transition_check(self):
		# 检测是否有跳转图层与玩家碰撞
		sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
		if sprites:
			self.player.block()
			self.transition_target = sprites[0].target
			self.scene_status = 'tint'

	def enter_scene(self, dt):
		if self.scene_status == 'untint':
			self.tint_progress -= self.tint_speed * dt

		if self.scene_status == 'tint':
			# 屏幕逐渐变暗
			self.tint_progress += self.tint_speed * dt

			if self.tint_progress >= 255:
				if type(self.transition_target) == Battle:
					# 设置当前战斗为目标战斗
					self.battle = self.transition_target
				elif self.transition_target == 'level':
					self.battle = None
				else:
					# 切换到目标地图和位置
					self.setuppos(self.tmx_maps[self.transition_target[0]], self.transition_target[1])
				self.scene_status = 'untint'
				self.transition_target = None

		self.tint_progress = max(0, min(self.tint_progress, 255))
		self.tint_surf.set_alpha(self.tint_progress)
		self.display_surface.blit(self.tint_surf, (0,0))
	
	def end_battle(self, character,status):
		pygame.mixer.music.stop()  # 停止当前播放的音乐
		pygame.mixer.music.load('../music/world.mp3')  # 加载新的音乐文件
		pygame.mixer.music.play(-1)  # 循环播放新音乐

		self.transition_target = 'level'
		self.scene_status = 'tint'
		if character:
			character.character_data['defeated'] = True
			self.create_dialog(character)

		if status==False:
			self.setuppos(self.tmx_maps['hospital'], 'world')
		
		if not self.evolution:
			self.player.unblock()
			self.check_evolution()

	def check_evolution(self):
		for index, monster in self.player_monsters.items():
			if monster.evolution:
				if monster.level == monster.evolution[1]:
					self.player_monsters[index] = Monster(monster.evolution[0], monster.level)


	def end_evolution(self):
		self.evolution = None
		self.player.unblock()					

	# 检查是否有怪物与玩家碰撞
	def check_monster(self):
		
		colliding_sprites = [sprite for sprite in self.monster_sprites if sprite.rect.colliderect(self.player.hitbox)]

		# 条件1: 存在碰撞的怪物
		has_collision = bool(colliding_sprites)

		# 条件2: 当前不在战斗状态
		not_in_battle = not self.battle

		# 条件3: 玩家有移动方向
		player_is_moving = bool(self.player.direction)

		if has_collision and not_in_battle and player_is_moving:
			if not self.encounter_timer.active:
				self.encounter_timer.activate()

	def monster_encounter(self):
		# 碰撞的怪物精灵将被存储在 sprites 列表中。
		colliding_sprites = [sprite for sprite in self.monster_sprites if sprite.rect.colliderect(self.player.hitbox)]

		if colliding_sprites and self.player.direction:
			# 为战斗计时器设置一个持续时间
			self.encounter_timer.duration = randint(1000, 2000)
			# 阻止玩家移动
			self.player.block()

			pygame.mixer.music.stop()  # 停止当前播放的音乐
			pygame.mixer.music.load('../music/battle.mp3')  # 加载新的音乐文件
			pygame.mixer.music.play(-1)  # 循环播放新音乐

			opponent_monsters = {}
			for index, monster in enumerate(colliding_sprites[0].monsters):
				level = colliding_sprites[0].level + randint(-3, 3)
				opponent_monsters[index] = Monster(monster, level)

			self.transition_target = Battle(
				player_monsters = self.player_monsters,
				opponent_monsters = opponent_monsters,
				monster_frames = self.monster_frames, 
				bg_surf = self.bg_frames[colliding_sprites[0].biome],
				end_battle = self.end_battle,
				character = None)

			self.scene_status = 'tint'

	def run(self):
		# 我们需要经常更新位置，需要帧速率独立，而保持游戏的流畅性。
		while True:
			dt = self.clock.tick(60) / 1000
			self.display_surface.fill('black')

			# 事件循环
			# 遍历所有当前发生的事件
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			# 更新逻辑
			self.encounter_timer.update()
			self.input()
			self.transition_check()
			self.all_sprites.update(dt)
			self.check_monster()
			
			
			self.all_sprites.draw(self.player)

			# 表面层
			self.enter_scene(dt)
			self.below_display.update()

			if self.monster_display_open:
				self.monster_display.update(dt)
				self.below_display.update(monster_display_open=True)

			if self.battle:
				self.battle.update(dt)

			if self.dialog_para:
				self.dialog_para.update()

			if self.index_open:
				self.monster_display_open.update(dt)

			if self.evolution:
				self.evolution.update(dt)


			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()