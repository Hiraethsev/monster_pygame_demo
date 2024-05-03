import pygame.time

from setting import *
# 加载 TMX 格式的地图文件，并将其转换为 Pygame 中的表面对象
from pytmx.util_pygame import load_pygame
# 解决不同操作系统上路径兼容问题
from os.path import join
# 从文件夹中读取并保存图片，操作图片
from support import *
# 精灵类
from sprites import Sprite,AnimatedSprite,MonsterPatchSprite,BorderSprite, CollidableSprite,TransitionSprite
# 玩家,NPC
from entities import Player,Character
# 所有精灵
from groups import AllSprites
# 怪物
from monster import Monster
from monster_display import *
# 战斗
from battle import *
# 对话类
from dialog import *

class Game:
  # 总体设置
  def __init__(self):
    pygame.init()
    # 创建一个指定大小的游戏窗口，并赋值给 Game 类的 display_surface 属性
    self.display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption('Monster Hunter')
    # 通过一个时钟对象，控制游戏的帧速率
    self.clock=pygame.time.Clock()
    # 加载地图等数据
    self.import_assets()

    # player monsters
    self.player_monsters = {
      0: Monster('Ivieron', 20),
      1: Monster('Atrox', 15),
      2: Monster('Cindrill', 36),
      3: Monster('Friolera', 20),
      4: Monster('Sparchu', 17),
      5: Monster('Gulfin', 19),
      6: Monster('Jacana', 14),
      7: Monster('Larvea', 10)
    }

    self.dummy_monsters={
      0: Monster('Jacana', 10),
      1: Monster('Atrox', 15),
      2: Monster('Jacana', 10),
      4: Monster('Sparchu', 11),
      5: Monster('Gulfin', 9)
    }

    # groups
    # 创建精灵组，保存所有游戏中的精灵对象
    self.all_sprites=AllSprites()
    # 识别可碰撞的精灵
    self.collision_sprites=pygame.sprite.Group()
    # 识别所有NPC
    self.character_sprites=pygame.sprite.Group()
    # 识别所有的跳转图层
    self.transition_sprites=pygame.sprite.Group()

    # transition
    self.transition_target=None
    self.tint_surf=pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
    self.tint_mode='unable'
    self.tint_progress=0
    self.tint_direction=-1
    self.tint_speed=600

    # dialog
    self.dialog_tree=None

    #overlays
    self.monster_display=MonsterDisplay(self.player_monsters,self.fonts,self.monster_frames)
    self.monster_display_open=False

    self.battle=Battle(self.player_monsters,self.dummy_monsters,self.monster_frames,self.battle_bg_frames['forest1'],self.fonts)

    self.below_display=BelowDisplay(self.fonts)

    self.setup(self.tmx_maps['world'],'water')

  def import_assets(self):
    self.tmx_maps={
      'world':load_pygame(join('..','data','maps','world.tmx')),
      'hospital': load_pygame(join('..', 'data', 'maps', 'hospital.tmx')),
      'hospital2': load_pygame(join('..', 'data', 'maps', 'hospital2.tmx')),
      'arena':load_pygame(join('..', 'data', 'maps', 'arena.tmx')),
      'fire':load_pygame(join('..', 'data', 'maps', 'fire.tmx')),
      'house': load_pygame(join('..', 'data', 'maps', 'house.tmx')),
      'plant': load_pygame(join('..', 'data', 'maps', 'plant.tmx')),
      'water': load_pygame(join('..', 'data', 'maps', 'water.tmx'))

    }

    self.overworld_frames={
      'water':import_folder('..','graphics','tilesets','water'),
      'coast':coast_importer(24,12,'..','graphics','tilesets','coast'),
      'characters':all_character_import('..','graphics','characters')
    }

    self.monster_frames={
      'icons':import_folder_dict('..','graphics','icons'),
      'monsters':monster_importer(4,2,'..','graphics','monsters'),
      'ui': import_folder_dict('..', 'graphics', 'ui'),
    }

    self.fonts={
      'dialog':pygame.font.Font(join('..','graphics','fonts','STZHONGS.ttf'),28),
      'regular': pygame.font.Font(join('..', 'graphics', 'fonts', 'STZHONGS.ttf'), 18),
      'mini': pygame.font.Font(join('..', 'graphics', 'fonts', 'STZHONGS.ttf'), 14),
      'bold': pygame.font.Font(join('..', 'graphics', 'fonts', 'dogicapixelbold.otf'), 20),
      'monster_name':pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 18),
      'monster_name_large': pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 20)

    }


    self.battle_bg_frames=import_folder_dict('..', 'graphics', 'backgrounds')

    self.game_data={
      'TRAINER_DATA':import_data_json('..','data','game_data','TRAINER_DATA.json'),
      'MONSTER_DATA':import_data_json('..', 'data', 'game_data', 'MONSTER_DATA.json'),
      'ATTACK_DATA': import_data_json('..', 'data', 'game_data', 'ATTACK_DATA.json')
    }

  def setup(self,tmx_map,player_start_pos):
    #清除原有的地图
    for group in (self.all_sprites,self.collision_sprites,self.transition_sprites,self.character_sprites):
      group.empty()
    #创造的顺序决定了覆盖的层次=>给每个精灵一个图层来渲染
    # terrain
    # 获取地形层，并遍历这个层中的所有方块
    # 这里的x，y是方块的位置而非像素
    for layer in ['Terrain','Terrain Top']:
      for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
        Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites,WORLD_LAYERS['bg'])

    # water
    for obj in tmx_map.get_layer_by_name('Water'):
      for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
        for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
          AnimatedSprite((x, y), self.overworld_frames['water'], self.all_sprites, WORLD_LAYERS['water'])

     # coast
    for obj in tmx_map.get_layer_by_name('Coast'):
      terrain = obj.properties['terrain']
      side = obj.properties['side']
      AnimatedSprite((obj.x, obj.y), self.overworld_frames['coast'][terrain][side], self.all_sprites,
                       WORLD_LAYERS['bg'])

    #objects
    for obj in tmx_map.get_layer_by_name('Objects'):
      if obj.name=='top':
        Sprite((obj.x, obj.y), obj.image, self.all_sprites,WORLD_LAYERS['top'])
      else:
        CollidableSprite((obj.x,obj.y),obj.image,(self.all_sprites,self.collision_sprites))

  # transition objetcts
    for obj in tmx_map.get_layer_by_name('Transition'):
      TransitionSprite((obj.x,obj.y),(obj.width,obj.height),(obj.properties['target'],obj.properties['pos']),self.transition_sprites)

    # collision objects
    for obj in tmx_map.get_layer_by_name('Collisions'):
      BorderSprite((obj.x,obj.y),pygame.Surface((obj.width,obj.height)),self.collision_sprites)

    # grass patches
    for obj in tmx_map.get_layer_by_name('Monsters'):
      MonsterPatchSprite((obj.x, obj.y), obj.image, self.all_sprites,obj.properties['biome'])

    #entities
    for obj in tmx_map.get_layer_by_name('Entities'):
      if(obj.name == 'Player'):
        if obj.properties['pos']== player_start_pos:
          self.player=Player(pos=(obj.x,obj.y),frames=self.overworld_frames['characters']['player'],groups=self.all_sprites,facing_direction=obj.properties['direction'],collision_sprites=self.collision_sprites)
      else:
        Character(pos=(obj.x,obj.y),frames=self.overworld_frames['characters'][obj.properties['graphic']],groups=(self.all_sprites,self.collision_sprites,self.character_sprites),facing_direction=obj.properties['direction'],character_data=self.game_data['TRAINER_DATA'][obj.properties['character_id']])

  #对话系统
  def input(self):
    #实时检测玩家是否按下某个键
    #get_pressed 检测键盘上的某个键在当前帧是否被按下,get_just_pressed 检测键盘上的某个键是否在当前帧刚刚被按下，而在前一帧未被按下,只有在某个键从未按下变为按下的瞬间，相应的元素值才为 True
    if not self.dialog_tree:
      keys = pygame.key.get_just_pressed()
      if keys[pygame.K_SPACE]:
        for character in self.character_sprites:
          if check_connections(100, self.player, character):
            # 阻止输入
            self.player.block()
            # NPC面向玩家
            character.change_facing_direction(self.player.rect.center)
            # 对话
            self.create_dialog(character)
    if keys[pygame.K_RETURN]:
      self.monster_display_open=not self.monster_display_open
      self.player.blocked=not self.player.blocked


  def create_dialog(self,character):
    if not self.dialog_tree:
      self.dialog_tree=DialogTree(character,self.player,self.all_sprites,self.fonts['dialog'],self.end_dialog)

  def end_dialog(self,character):
    self.dialog_tree=None
    self.player.unblock()

  # 页面跳转
  def transition_check(self):
    # 检测是否有跳转图层与玩家碰撞
    sprites=[sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
    if sprites:
      self.player.block()
      self.transition_target=sprites[0].target
      self.tint_mode='able'

  def tint_screen(self,dt):
    if self.tint_mode == 'unable':
      self.tint_progress -= self.tint_speed * dt
    if self.tint_mode=='able':
      self.tint_progress+=self.tint_speed*dt
      if(self.tint_progress>=255):
        self.setup(self.tmx_maps[self.transition_target[0]],self.transition_target[1])
        self.tint_mode='unable'
        self.transition_target=None

    self.tint_progress=max(0,min(self.tint_progress,255))
    self.tint_surf.set_alpha(self.tint_progress)
    self.display_surface.blit(self.tint_surf,(0,0))

  def run(self):
    while True:
      # 我们需要经常更新位置，游戏需要帧速率独立，而保持游戏的流畅性。
      dt=self.clock.tick()/1000
      self.display_surface.fill('black')

      # 事件循环
      # 遍历所有当前发生的事件
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()

      # 更新逻辑
      self.input()
      self.transition_check()
      self.all_sprites.update(dt)

      self.all_sprites.draw(self.player.rect.center)

      #表面层
      self.tint_screen(dt)
      self.below_display.update()

      if self.monster_display_open:
        self.monster_display.update(dt)
        self.below_display.update(monster_display_open=True)

      if self.battle:
        self.battle.update(dt)

      if self.dialog_tree:
        self.dialog_tree.update()

      pygame.display.update()

# 检查当前脚本是否被直接运行
if __name__=='__main__':
  game = Game()
  game.run()