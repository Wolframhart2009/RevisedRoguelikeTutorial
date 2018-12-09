import libtcodpy as libtcod

def menu(con, header, options, width, screen_width, screen_height):
	if len(options) > 26: raise ValueError('Cannot have a manu with more than 26 options')
	
	#calculate total height for header (after autowrap) and one line per option
	header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
	height = header_height + len(options)
	
	#Create an offscreen console that represents the menu's window
	window = libtcod.console_new(width, height)
	
	#print the header with autowrap
	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
	
	#print all of the options
	y = header_height
	letter_index = ord('a')
	for option_text in options:
		text = '(' + chr(letter_index) + ') ' + option_text
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
		y += 1
		letter_index += 1
		
	#Blit the contents of the 'window' together to the root console
	x = int(screen_width / 2  - width /2)
	y = int(screen_height / 2  - height /2)
	
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, .7)

def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
	options = []
	#Show a menu with item in the inventory as an option
	if(len(player.inventory.items) == 0):
		options = ['Inventory is empty']
	else:
		options = []
		
		for item in player.inventory.items:
			if player.equipment.main_hand == item:
				options.append('{0} (on main hand)'.format(item.name))
			elif player.equipment.off_hand == item:
				options.append('{0} (on off hand)'.format(item.name))
			else:
				options.append(item.name)
		
	menu(con, header, options, inventory_width, screen_width, screen_height)
	
def main_menu(con, background_image, screen_width, screen_height):
	libtcod.image_blit_2x(background_image, 0, 0, 0)

	libtcod.console_set_default_foreground(0, libtcod.light_yellow)
	libtcod.console_print_ex(0, int(screen_width/2), int(screen_height/2) - 4, libtcod.BKGND_NONE, libtcod.CENTER, 'TOMB OF THE ANCIENT KINGS')
	libtcod.console_print_ex(0, int(screen_width/2), int(screen_height - 2) , libtcod.BKGND_NONE, libtcod.CENTER, 'By Graeme Copeland')
	
	menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)
	
def message_box(con, header, width, screen_width, screen_height):
	menu(con, header, [], width, screen_width, screen_height)
	
def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
	options = [
	'Constitution (+20 Hp, from {0})'.format(player.fighter.max_hp),
	'Strength (+1 Attack, from {0})'.format(player.fighter.power),
	'Agility (+1 Defense, from {0})'.format(player.fighter.defense)
	]
	
	menu(con, header, options, menu_width, screen_width, screen_height)
	
def character_screen(player, characten_screen_width, characten_screen_height, screen_width, screen_height):
	window = libtcod.console_new(characten_screen_width, characten_screen_height)
	
	libtcod.console_set_default_foreground(window, libtcod.white)
	
	libtcod.console_print_rect_ex(window, 0, 1, characten_screen_width, characten_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Character Information')
	libtcod.console_print_rect_ex(window, 0, 2, characten_screen_width, characten_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Level {0}'.format(player.level.current_level))
	libtcod.console_print_rect_ex(window, 0, 3, characten_screen_width, characten_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Experience {0}'.format(player.level.current_xp))
	libtcod.console_print_rect_ex(window, 0, 4, characten_screen_width, characten_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Experience to level {0}'.format(player.level.experience_to_next_level))
	libtcod.console_print_rect_ex(window, 0, 6, characten_screen_width, characten_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Maximum Hp {0}'.format(player.fighter.max_hp))
	libtcod.console_print_rect_ex(window, 0, 7, characten_screen_width, characten_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Attack {0}'.format(player.fighter.power))
	libtcod.console_print_rect_ex(window, 0, 8, characten_screen_width, characten_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Defense {0}'.format(player.fighter.defense))
	
	x = screen_width // 2 - characten_screen_width // 2
	y = screen_height // 2 - characten_screen_height // 2
	libtcod.console_blit(window, 0, 0, characten_screen_width, characten_screen_height, 0, x, y, 1.0, .7)
	