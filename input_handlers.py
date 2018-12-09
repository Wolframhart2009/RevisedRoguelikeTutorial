import libtcodpy as libtcod

from game_states import GameStates

def handle_keys(key, game_state):
	if game_state == GameStates.PLAYERS_TURN:
		return handle_player_turn_keys(key)
	elif game_state == GameStates.PLAYER_DEAD:
		return handle_player_dead_keys(key)
	elif game_state == GameStates.TARGETING:
		return handle_targeting_keys(key)
	elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
		return handle_show_inventory_keys(key)
	else:
		return {}

def handle_player_turn_keys(key):
	key_char = chr(key.c)

	#Movement Key handlers
	if key.vk == libtcod.KEY_UP or key_char == 'k':
		return {'move': (0, -1)}
	elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
		return {'move': (0, 1)}
	elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
		return {'move': (-1, 0)}
	elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
		return {'move': (1, 0)}
	elif key_char == 'y':
		return {'move': (-1, -1)}
	elif key_char == 'u':
		return {'move': (1, -1)}
	elif key_char == 'b':
		return {'move': (-1, 1)}
	elif key_char == 'n':
		return {'move': (1, 1)}

	#Interaction handlers
	if key_char == 'g':
		return {'pickup': True}
	elif key_char == 'i':
		return {'show_inventory': True}
	elif key_char == 'd':
		return {'show_drop_inventory': True}
	
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		#Alt + Enter triggers fullscreen mode
		return {'fullscreen': True} 
	
	elif key.vk == libtcod.KEY_ESCAPE:
		#Exit game or current menu
		return {'exit': True}
	
	#No Input from keys 
	return {}

def handle_player_dead_keys(key):
	key_char = chr(key.c)

	#Interaction handlers
	if key_char == 'i':
		return {'show_inventory': True}
	
	#Option handlers
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		#Alt + Enter triggers fullscreen mode
		return {'fullscreen': True} 
	elif key.vk == libtcod.KEY_ESCAPE:
		#Exit game or current menu
		return {'exit': True}
		
	return {}
	
def handle_targeting_keys(key):
	if key.vk == libtcod.KEY_ESCAPE:
		#Exit game or current menu
		return {'exit': True}
	
	return {}
		
def handle_show_inventory_keys(key):
	index = key.c - ord('a')
	
	#Selected inventory index in inv list
	if index >= 0:
		return {'inventory_index': index}
		
	#Option handlers
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		#Alt + Enter triggers fullscreen mode
		return {'fullscreen': True} 
	elif key.vk == libtcod.KEY_ESCAPE:
		#Exit game or current menu
		return {'exit': True}
		
	return {}

def handle_main_menu(key):
	key_char = chr(key.c)
	
	#Main menu options
	if key_char == 'a':
		return{'new_game': True}
	elif key_char == 'b':
		return{'load_game': True}
	elif key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
		return{'exit': True}
		
	return {}

def handle_mouse(mouse):
	(x, y) = (mouse.cx, mouse.cy)
	
	if mouse.lbutton_pressed:
		return {'left_click': (x, y)}
	elif mouse.rbutton_pressed:
		return {'right_click': (x, y)}
	
	return {}