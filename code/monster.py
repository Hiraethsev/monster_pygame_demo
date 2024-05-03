from random import randint

from support import *

Monster_Data = import_data_json('..', 'data', 'game_data', 'MONSTER_DATA.json')

Attack_Data = import_data_json('..', 'data', 'game_data', 'ATTACK_DATA.json')


class Monster:
    def __init__(self, name, level, monster_data=Monster_Data):
        self.name, self.level = name, level

        # stats
        self.element = monster_data[name]['stats']['element']
        self.base_stats = monster_data[name]['stats']
        self.abilities = monster_data[name]['abilities']

        self.energy = max(0, self.base_stats['max_energy'] * self.level - randint(0, 200))
        self.health = max(0, self.base_stats['max_health'] * self.level - randint(0, 200))

        # xp
        self.level_up = self.level * 50
        self.xp = randint(0, self.level_up)

    def get_stat(self, stat):
        return self.base_stats[stat] * self.level

    def get_stats(self):
        return {
            'health': self.get_stat('max_health'),
            'energy': self.get_stat('max_energy'),
            'attack': self.get_stat('attack'),
            'defense': self.get_stat('defense'),
            'speed': self.get_stat('speed'),
            'recovery': self.get_stat('recovery'),
        }

    def get_abilities(self):
        return [ability for lvl, ability in self.abilities.items() if self.level >= int(lvl)]
