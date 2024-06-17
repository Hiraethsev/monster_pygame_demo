# 从文件夹中读取并操作
from import_method import *

Monster_Data = import_data_json( 'data/game_data/MONSTER_DATA.json')
Attack_Data = import_data_json('data/game_data/ATTACK_DATA.json')
NPC_Data=import_data_json('data/game_data/NPC_DATA.json')
COLORS=import_data_json('data/game_data/COLOR_DATA.json')

# Monster_Data = import_data_json_from_folder( '../data/game_data/MONSTER_DATA.json')
# Attack_Data = import_data_json_from_folder('../data/game_data/ATTACK_DATA.json')
# NPC_Data=import_data_json_from_folder('../data/game_data/NPC_DATA.json')
# COLORS=import_data_json_from_folder('../data/game_data/COLOR_DATA.json')



Fonts = {
	'dialog':pygame.font.Font(join('..','graphics','fonts','STZHONGS.TTF'),28),
	'regular': pygame.font.Font(join('..', 'graphics', 'fonts', 'STZHONGS.ttf'), 18),
	'small': pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 14),
	'bold': pygame.font.Font(join('..', 'graphics', 'fonts', 'dogicapixelbold.otf'), 20),
	'mini': pygame.font.Font(join('..', 'graphics', 'fonts', 'STZHONGS.ttf'), 14),
      'monster_name':pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 18),
      'monster_name_large': pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 20),
      'monster_name_mini': pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 14),
      'monster_choice_large': pygame.font.Font(join('..', 'graphics', 'fonts', 'STZHONGS.ttf'), 25),
      'monster_choice_middle': pygame.font.Font(join('..', 'graphics', 'fonts', 'STZHONGS.ttf'), 20),
      'monster_choice_mini': pygame.font.Font(join('..', 'graphics', 'fonts', 'STZHONGS.ttf'), 16)
}

Player_Monsters_Dict={
	0: ('Friolera', 40,130),
	1: ('Atrox', 15,160),
	2: ('Ivieron', 20,70),
	3: ('Sparchu', 17,190),
	4: ('Gulfin', 19,356),
	5: ('Jacana', 14,298),
	6: ('Larvea', 10,567)
}