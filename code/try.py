import json
from os.path import join

TRAINER_DATA = {
	'o1': {
		'monsters': {0: ('Jacana', 14), 1: ('Cleaf', 15)},
		'dialog': {
			'default': ['Hey, how are you?', 'Oh, so you want to fight?', 'FIGHT!'],
			'defeated': ['You are very strong!', 'Let\'s fight again sometime?']},
		'directions': ['down'],
		'look_around': True,
		'defeated': False,
		'biome': 'forest'
	},
	'o2': {
		'monsters': {0: ('Atrox', 14), 1: ('Pouch', 15), 2: ('Draem', 13), 3: ('Cindrill', 13)},
		'dialog': {
			'default': ['我不喜欢沙滩', '因为我刚买的海景谷被海鸥叼走了', '什么？你居然不知道谷子是什么？',
						'开战吧！可恶的现充！'],
			'defeated': ['等我拿回我失去的谷子我就会强的可怕！']},
		'directions': ['left', 'down'],
		'look_around': False,
		'defeated': False,
		'biome': 'sand'
	},
	'o3': {
		'monsters': {0: ('Atrox', 14), 1: ('Pouch', 15), 2: ('Draem', 13), 3: ('Cindrill', 13)},
		'dialog': {
			'default': ['I love skating!', 'FIGHT!'],
			'defeated': ['Good luck with the boss', 'It\'s so cold in here']},
		'directions': ['left', 'right', 'up', 'down'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
	},
	'o4': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Atrox', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['I love skating!', 'FIGHT!'],
			'defeated': ['Good luck with the boss', 'It\'s so cold in here']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'forest'
	},
	'o5': {
		'monsters': {0: ('Plumette', 20), 1: ('Ivieron', 22), 2: ('Atrox', 24), 3: ('Pouch', 19)},
		'dialog': {
			'default': ['So you want to challenge the big ones', 'This will be fun!'],
			'defeated': ['I hope the lawyers will never spot you', '<3']},
		'directions': ['up', 'right'],
		'look_around': True,
		'defeated': False,
		'biome': 'forest'
	},
	'o6': {
		'monsters': {0: ('Finsta', 15), 1: ('Finsta', 15), 2: ('Finsta', 15)},
		'dialog': {
			'default': ['I love skating!', 'FIGHT!'],
			'defeated': ['Good luck with the boss', 'It\'s so cold in here']},
		'directions': ['down'],
		'look_around': False,
		'defeated': False,
		'biome': 'ice'
	},
	'o7': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Atrox', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['There are no bugs in the snow!'],
			'defeated': ['Maybe I should check a vulcano...', 'It\'s so cold in here']},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'ice'
	},
	'p1': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Atrox', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['I love trees', 'and fights'],
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
	},
	'p2': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Atrox', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['I love trees', 'and fights'],
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
	},
	'p3': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Atrox', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['I love trees', 'and fights'],
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
	},
	'p4': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Atrox', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['I love trees', 'and fights'],
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
	},
	'px': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Atrox', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['I love trees', 'and fights'],
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
	},
	'w1': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Draem', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['It\'s so cold in here', 'maybe a fight will warm me up'],
			'defeated': ['Good luck with the boss!']},
		'directions': ['left'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
	},
	'w2': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Draem', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['It\'s so cold in here', 'maybe a fight will warm me up'],
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
	},
	'w3': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Draem', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['It\'s so cold in here', 'maybe a fight will warm me up'],
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
	},
	'w4': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Draem', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['It\'s so cold in here', 'maybe a fight will warm me up'],
			'defeated': ['Good luck with the boss!']},
		'directions': ['left'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
	},
	'w5': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Draem', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['It\'s so cold in here', 'maybe a fight will warm me up'],
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
	},
	'wx': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Draem', 24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['I hope you brought rations', 'This will be a long journey'],
			'defeated': ['Congratultion!']},
		'directions': ['down'],
		'look_around': False,
		'defeated': False,
		'biome': 'ice'
	},
	'f1': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem', 24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['This place feels kinda warm...', 'fight!'],
			'defeated': ['Congratultion!']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
	},
	'f2': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem', 24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['This place feels kinda warm...', 'fight!'],
			'defeated': ['Congratultion!']},
		'directions': ['right', 'left'],
		'look_around': False,
		'defeated': False,
		'biome': 'sand'
	},
	'f3': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem', 24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['This place feels kinda warm...', 'fight!'],
			'defeated': ['Congratultion!']},
		'directions': ['right', 'left'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
	},
	'f4': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem', 24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['This place feels kinda warm...', 'fight!'],
			'defeated': ['Congratultion!']},
		'directions': ['up', 'right'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
	},
	'f5': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem', 24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['This place feels kinda warm...', 'fight!'],
			'defeated': ['Congratultion!']},
		'directions': ['left'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
	},
	'f6': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem', 24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['This place feels kinda warm...', 'fight!'],
			'defeated': ['Congratultion!']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
	},
	'fx': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem', 24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['Time to bring the heat', 'fight!'],
			'defeated': ['Congratultion!']},
		'directions': ['down'],
		'look_around': False,
		'defeated': False,
		'biome': 'sand'
	},
	'Nurse': {
		'direction': 'down',
		'radius': 0,
		'look_around': False,
		'dialog': {
			'default': ['Welcome to the hospital', 'Your monsters have been healed'],
			'defeated': None},
		'directions': ['down'],
		'defeated': False,
		'biome': None
	}
}
MONSTER_DATA = {
	'Plumette': {
		'stats': {'element': 'plant', 'max_health': 15, 'max_energy': 17, 'attack': 4, 'defense': 8, 'recovery': 1,
				  'speed': 1},
		'abilities': {0: 'scratch', 5: 'spark'},
		'evolve': ('Ivieron', 15)},
	'Ivieron': {
		'stats': {'element': 'plant', 'max_health': 18, 'max_energy': 20, 'attack': 5, 'defense': 10, 'recovery': 1.2,
				  'speed': 1.2},
		'abilities': {0: 'scratch', 5: 'spark'},
		'evolve': ('Pluma', 32)},
	'Pluma': {
		'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 26, 'attack': 6, 'defense': 12, 'recovery': 1.8,
				  'speed': 1.8},
		'abilities': {0: 'scratch', 5: 'spark'},
		'evolve': None},
	'Sparchu': {
		'stats': {'element': 'fire', 'max_health': 15, 'max_energy': 7, 'attack': 3, 'defense': 8, 'recovery': 1.1,
				  'speed': 1},
		'abilities': {0: 'scratch', 5: 'fire', 15: 'battlecry', 26: 'explosion'},
		'evolve': ('Cindrill', 15)},
	'Cindrill': {
		'stats': {'element': 'fire', 'max_health': 18, 'max_energy': 10, 'attack': 3.5, 'defense': 10, 'recovery': 1.2,
				  'speed': 1.1},
		'abilities': {0: 'scratch', 5: 'fire', 15: 'battlecry', 26: 'explosion'},
		'evolve': ('Charmadillo', 33)},
	'Charmadillo': {
		'stats': {'element': 'fire', 'max_health': 29, 'max_energy': 12, 'attack': 4, 'defense': 17, 'recovery': 1.35,
				  'speed': 1.1},
		'abilities': {0: 'scratch', 5: 'fire', 15: 'battlecry', 26: 'explosion', 45: 'annihilate'},
		'evolve': None},
	'Finsta': {
		'stats': {'element': 'water', 'max_health': 13, 'max_energy': 17, 'attack': 2, 'defense': 8, 'recovery': 1.5,
				  'speed': 1.8},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
		'evolve': ('Gulfin', 34)},
	'Gulfin': {
		'stats': {'element': 'water', 'max_health': 18, 'max_energy': 20, 'attack': 3, 'defense': 10, 'recovery': 1.8,
				  'speed': 2},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
		'evolve': ('Finiette', 45)},
	'Finiette': {
		'stats': {'element': 'water', 'max_health': 27, 'max_energy': 23, 'attack': 4, 'defense': 17, 'recovery': 2,
				  'speed': 2.5},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
		'evolve': None},
	'Atrox': {
		'stats': {'element': 'fire', 'max_health': 18, 'max_energy': 20, 'attack': 3, 'defense': 10, 'recovery': 1.3,
				  'speed': 1.9},
		'abilities': {0: 'scratch', 5: 'spark', 30: 'fire'},
		'evolve': None},
	'Pouch': {
		'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 25, 'attack': 4, 'defense': 12, 'recovery': 1,
				  'speed': 1.5},
		'abilities': {0: 'scratch', 5: 'spark', 25: 'heal'},
		'evolve': None},
	'Draem': {
		'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 25, 'attack': 4, 'defense': 12, 'recovery': 1.2,
				  'speed': 1.4},
		'abilities': {0: 'scratch', 5: 'heal', 20: 'explosion', 25: 'splash'},
		'evolve': None},
	'Larvea': {
		'stats': {'element': 'plant', 'max_health': 15, 'max_energy': 17, 'attack': 1, 'defense': 8, 'recovery': 1,
				  'speed': 1},
		'abilities': {0: 'scratch', 5: 'spark'},
		'evolve': ('Cleaf', 4)},
	'Cleaf': {
		'stats': {'element': 'plant', 'max_health': 18, 'max_energy': 20, 'attack': 3, 'defense': 10, 'recovery': 1.7,
				  'speed': 1.6},
		'abilities': {0: 'scratch', 5: 'heal'},
		'evolve': None},
	'Jacana': {
		'stats': {'element': 'fire', 'max_health': 12, 'max_energy': 19, 'attack': 3, 'defense': 10, 'recovery': 2.1,
				  'speed': 2.6},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'burn', 20: 'explosion', 25: 'heal'},
		'evolve': None},
	'Friolera': {
		'stats': {'element': 'water', 'max_health': 13, 'max_energy': 20, 'attack': 4, 'defense': 6, 'recovery': 1.3,
				  'speed': 2},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
		'evolve': None},
}
ATTACK_DATA = {
	'burn': {'target': 'opponent', 'amount': 2, 'cost': 15, 'element': 'fire', 'animation': 'fire'},
	'heal': {'target': 'player', 'amount': -1.2, 'cost': 600, 'element': 'plant', 'animation': 'green'},
	'battlecry': {'target': 'player', 'amount': -1.4, 'cost': 20, 'element': 'normal', 'animation': 'green'},
	'spark': {'target': 'opponent', 'amount': 1.1, 'cost': 20, 'element': 'fire', 'animation': 'fire'},
	'scratch': {'target': 'opponent', 'amount': 1.2, 'cost': 20, 'element': 'normal', 'animation': 'scratch'},
	'splash': {'target': 'opponent', 'amount': 2, 'cost': 15, 'element': 'water', 'animation': 'splash'},
	'fire': {'target': 'opponent', 'amount': 2, 'cost': 15, 'element': 'fire', 'animation': 'fire'},
	'explosion': {'target': 'opponent', 'amount': 2, 'cost': 90, 'element': 'fire', 'animation': 'explosion'},
	'annihilate': {'target': 'opponent', 'amount': 3, 'cost': 30, 'element': 'fire', 'animation': 'explosion'},
	'ice': {'target': 'opponent', 'amount': 2, 'cost': 15, 'element': 'water', 'animation': 'ice'},
}

with open(join('..', 'data', 'game_data', 'ATTACK_DATA.json'), "w", encoding='utf-8') as f:
	json.dump(ATTACK_DATA, f, ensure_ascii=False)

# def import_data_json(*path):
#     with open(join(*path), "r") as fp:
#         data = json.load(fp)
#         data = json.loads(data)
#     return data
#
# game_data={
#       'TRAINER_DATA':import_data_json('..','data','game_data','TRAINER_DATA.json'),
#       'MONSTER_DATA':import_data_json('..', 'data', 'game_data', 'MONSTER_DATA.json'),
#       'ATTACK_DATA': import_data_json('..', 'data', 'game_data', 'ATTACK_DATA.json')
#     }
