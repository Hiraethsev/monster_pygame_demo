import pygame.display

from entities import Entity
from setting import *
from support import import_image


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.shadow_surf = import_image('..', 'graphics', 'other', 'shadow')

    def draw(self, player_center):
        # 根据玩家中心位置的偏移量来确定它们的绘制位置，以确保玩家所在位置始终在窗口的中心
        # 背景的运动方向与玩家运动方向相反
        self.offset.x = -(player_center[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(player_center[1] - WINDOW_HEIGHT / 2)

        bg_sprites = [sprite for sprite in self if sprite.z < WORLD_LAYERS['main']]
        main_sprites = sorted([sprite for sprite in self if sprite.z == WORLD_LAYERS['main']],
                              key=lambda sprite: sprite.y_sort)
        fg_sprites = [sprite for sprite in self if sprite.z > WORLD_LAYERS['main']]

        for layer in (bg_sprites, main_sprites, fg_sprites):
            for sprite in layer:
                if isinstance(sprite, Entity):
                    # 用于将阴影图像绘制到游戏的主显示表面
                    self.display_surface.blit(self.shadow_surf, sprite.rect.topleft + self.offset + vector(40, 100))
                # 将精灵的图像绘制到表面，根据精灵的矩形位置来确定位置
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
