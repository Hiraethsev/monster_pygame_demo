from data_set import * 
from timer import Timer
from data_import import COLORS,Fonts


class DialogPara:
	def __init__(self, character, player, all_sprites,end_dialog):
		self.player = player
		self.character = character
		self.font =  Fonts['dialog']
		self.all_sprites = all_sprites
		
		self.dialog = character.get_dialog()
		self.dialog_index = 0
		self.end_dialog=end_dialog

		self.current_dialog = DialogSprite(self.dialog[self.dialog_index], self.character, self.all_sprites, self.font)
		# 计时器防止按的太快
		self.prevent_timer = Timer(600, autostart = True)


	def input(self):
		keys = pygame.key.get_just_pressed()
		if keys[pygame.K_SPACE] and not self.prevent_timer.active:
			self.current_dialog.kill()
			self.dialog_index += 1
			if self.dialog_index < len(self.dialog):
				self.current_dialog = DialogSprite(self.dialog[self.dialog_index], self.character, self.all_sprites, self.font)
				self.prevent_timer.activate()
			else:
				self.end_dialog(self.character)

	def update(self):
		self.prevent_timer.update()
		self.input()

class DialogSprite(pygame.sprite.Sprite):
	def __init__(self, message, character, groups, font):
		super().__init__(groups)
		self.z = Layer_Z_Index['top']

		# text 
		text_surf = font.render(message, False, COLORS['black'])
		width = max(30, text_surf.get_width() +10)
		height = text_surf.get_height() + 10

		# background
		surf = pygame.Surface((width, height), pygame.SRCALPHA)
		pygame.draw.rect(surf, COLORS['white'], surf.get_frect(topleft = (0,0)),0, 4)
		surf.blit(text_surf, text_surf.get_frect(center = (width / 2, height / 2)))

		self.image = surf
		self.rect = self.image.get_frect(midbottom = character.rect.midtop + vector(0,-10))