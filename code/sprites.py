from random import uniform

import pygame

from setting import *


# 继承来创建自己的精灵类
# 表示游戏中的角色、道具、敌人等各种实体的类
class Sprite(pygame.sprite.Sprite):
  def __init__(self, pos, surf, groups, z=WORLD_LAYERS['main']):
    # 调用了父类的构造函数，确保精灵对象被正确地添加到指定的精灵组中
    super().__init__(groups)
    self.image = surf
    # rect 属性表示精灵在屏幕上的位置和大小。
    self.rect = self.image.get_frect(topleft=pos)
    self.z = z
    self.y_sort = self.rect.centery
    self.hitbox = self.rect.copy()


class TransitionSprite(Sprite):
  def __init__(self, pos, size, target, groups):
    surf = pygame.Surface(size)
    super().__init__(pos, surf, groups)
    self.target = target


class BorderSprite(Sprite):
  def __init__(self, pos, surf, groups):
    super().__init__(pos, surf, groups)
    self.hitbox = self.rect.copy()


class CollidableSprite(Sprite):
  def __init__(self, pos, surf, groups):
    super().__init__(pos, surf, groups)
    self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height * 0.7)


class MonsterPatchSprite(Sprite):
  def __init__(self, pos, surf, groups, biome):
    self.biome = biome
    super().__init__(pos, surf, groups, WORLD_LAYERS['main' if biome != 'sand' else 'bg'])
    self.y_sort -= 40


# battle sprites
class MonsterSprite(pygame.sprite.Sprite):
  def __init__(self, pos, frames, groups, monster, index, pos_index, entity):
    super().__init__(groups)
    self.index = index
    self.pos_index = pos_index
    self.entity = entity
    self.monster = monster
    self.frame_index, self.frames, self.state = 0, frames, 'idle'
    self.animation_speed = ANIMATION_SPEED + uniform(-1, 1)

    self.image = self.frames[self.state][self.frame_index]
    self.rect = self.image.get_frect(center=pos)

  def animate(self, dt):
    self.frame_index += self.animation_speed * dt
    self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

  def update(self, dt):
    self.animate(dt)


class AnimatedSprite(Sprite):
  def __init__(self, pos, frames, groups, z=WORLD_LAYERS['main']):
    self.frame_index, self.frames = 0, frames
    super().__init__(pos, frames[self.frame_index], groups, z)

  def animate(self, dt):
    self.frame_index += ANIMATION_SPEED * dt
    self.image = self.frames[int(self.frame_index % len(self.frames))]

  def update(self, dt):
    self.animate(dt)
