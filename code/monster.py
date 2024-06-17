from data_import import *
from timer import Timer

def update_player_monster():
	Player_Monsters={}
	for key in Player_Monsters_Dict.keys():
		name=Player_Monsters_Dict[key][0]
		level = Player_Monsters_Dict[key][1]
		xp = Player_Monsters_Dict[key][2]

		ele=Monster(name,level,xp)
		if ele.update_xp(0):
			Player_Monsters_Dict[key][1]=ele.level
			Player_Monsters_Dict[key][2] = ele.xp

		Player_Monsters[key]=ele

	return Player_Monsters

class Monster:
	def __init__(self, name, level,xp=0):
		self.name, self.level = name, level

		# stats 
		self.element = Monster_Data[name]['stats']['element']
		self.base_stats = Monster_Data[name]['stats']
		self.status= {
			'max_health': self.base_stats['max_health'] * self.level,
			'max_energy': self.base_stats['max_health'] * self.level,
			'attack': self.base_stats['attack'] * self.level,
			'defense': self.base_stats['defense'] * self.level,
			'speed': self.base_stats['speed'],
			'recovery': self.base_stats['recovery'] * self.level,
		}
		self.current_health=self.status['max_health']
		self.current_energy=self.status['max_energy']

		self.preparation = 0
		self.abilities = Monster_Data[name]['abilities']
		self.paused = False
		self.defending = False

		# experience
		self.xp = xp
		self.level_up = self.level * 150
		self.evolution = Monster_Data[name]['evolve']

		# energy timer
		self.energy_timer = Timer(5000, repeat=True, autostart=True, func=self.increase_energy)

	def increase_energy(self):
		self.current_energy = min(self.current_energy + 50, self.status['max_energy'])


	def get_abilities(self, all  = True):
		if all:
			return [ability for lvl, ability in self.abilities.items() if self.level >= int(lvl)]
		else:
			return [ability for lvl, ability in self.abilities.items() if self.level >= int(lvl) and Attack_Data[ability]['cost'] < self.current_energy]

	def get_info(self):
		return (
			(self.current_health, self.status['max_health']),
			(self.current_energy, self.status['max_energy']),
			(self.preparation, 100)
			)

	def reduce_energy(self, attack):
		self.current_energy -= Attack_Data[attack]['cost']

	def get_base_damage(self, attack):
		return self.status['attack'] * Attack_Data[attack]['amount']

	def update_xp(self, increase):
		if self.level_up  > increase+self.xp:
			self.xp += increase
			return False
		else:
			self.level += 1
			self.xp = increase - (self.level_up - self.xp)
			self.level_up = self.level * 150
			return True


	def update(self, dt):
		self.current_health = max(0, min(self.current_health, self.status['max_health']))
		self.current_energy = max(0, min(self.current_energy
		, self.status['max_energy']))
		if not self.paused:
			self.preparation += self.status['speed'] * dt
			self.energy_timer.update()
			