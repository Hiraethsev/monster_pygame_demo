import pygame.transform

from setting import *
from sprites import MonsterSprite


class Battle:
    def __init__(self, player_monsters, op_monsters, monsters_frames, bg_surf, fonts):
        self.display_surface = pygame.display.get_surface()
        self.bg_surf = bg_surf
        self.monster_frames = monsters_frames
        self.fonts = fonts
        self.monster_data = {'player': player_monsters, 'op': op_monsters}

        self.battle_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.op_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        for entity, monster in self.monster_data.items():
            for index, monster in {k: v for k, v in monster.items() if k <= 2}.items():
                self.create_monster(monster, index, index, entity)

    def create_monster(self, monster, index, pos_index, entity):
        frames = self.monster_frames['monsters'][monster.name]
        if entity == 'player':
            pos = list(BATTLE_POSITIONS['left'].values())[pos_index]
            groups = (self.battle_sprites, self.player_sprites)
            frames = {state: [pygame.transform.flip(frame, True, False) for frame in frames] for state, frames in
                      frames.items()}

        else:
            pos = list(BATTLE_POSITIONS['right'].values())[pos_index]
            groups = (self.battle_sprites, self.op_sprites)

        MonsterSprite(pos, frames, groups, monster, index, pos_index, entity)

    def update(self, dt):
        self.display_surface.blit(self.bg_surf, (0, 0))
        self.battle_sprites.update(dt)
        self.battle_sprites.draw(self.display_surface)
