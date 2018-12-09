import libtcodpy as libtcod
from random import randint

from entity import Entity
from render_functions import RenderOrder
from game_messages import Message
from components.fighter import Fighter
from components.ai import BasicMonster
from components.item import Item
from components.item_functions import heal, cast_lightning, cast_fireball, cast_confusion
from components.stairs import Stairs
from map_objects.tile import Tile
from map_objects.rectangle import Rect

class GameMap:
	"""
	A container for the tiles that are part of the current map screen
	"""
	def __init__(self, width, height, dungeon_level=1):
		self.width = width
		self.height = height
		self.tiles = self.init_tiles()
		
		self.dungeon_level = dungeon_level
		
	def init_tiles(self):
		tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
		
		return tiles
		
	def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room):
		#Creates up to 'max_rooms' and connects them all together
		
		rooms = []
		num_rooms = 0
		
		center_of_last_room_x = None
		center_of_last_room_y = None
		
		for r in range(max_rooms):
			#random width and height
			w = randint(room_min_size, room_max_size)
			h = randint(room_min_size, room_max_size)
			#random position with map boundaries
			x = randint(0, map_width - w - 1)
			y = randint(0, map_height - h - 1)
	
			#Make our rooms Rect objects to handle them better
			new_room = Rect(x, y, w, h)
						
			#Make sure our new room does not intersect with our other rooms
			for other_room in rooms:
				if new_room.intersect(other_room):
					break
			else:
				#We did not intersect so we can create our room
				
				#first carve it out from our tile map
				self.create_room(new_room)
				
				#then get its center coords
				(new_x, new_y) = new_room.center()
				
				center_of_last_room_x = new_x
				center_of_last_room_y = new_y
				
				if num_rooms == 0:
					player.x = new_x
					player.y = new_y
				else:
					#All rooms besides first need to connect to 
					#the last created room
				
					#get previous rooms center coords
					(prev_x, prev_y) = rooms[num_rooms - 1].center()
					
					if randint(0, 1) == 1:
						self.create_h_tunnel(prev_x, new_x, prev_y)
						self.create_v_tunnel(prev_y, new_y, new_x)
					else:
						self.create_v_tunnel(prev_y, new_y, prev_x)
						self.create_h_tunnel(prev_x, new_x, new_y)
						
				self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)
				rooms.append(new_room)
				num_rooms += 1
		
		stairs_component = Stairs(self.dungeon_level + 1)
		down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs', render_order=RenderOrder.STAIRS, stairs=stairs_component)
		entities.append(down_stairs)
			
	def create_room(self, room):
		#Go through the tiles in the rectangle and make them passable
		for x in range(room.x + 1, room.x2):
			for y in range(room.y + 1, room.y2):
				self.tiles[x][y].blocked = False
				self.tiles[x][y].block_sight = False
		
	def create_h_tunnel(self, x1, x2, y):
		for x in range(min(x1, x2), max(x1, x2) + 1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False
	
	def create_v_tunnel(self, y1, y2, x):
		for y in range(min(y1, y2), max(y1, y2) + 1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False
			
	def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
		#Get a random number of monsters
		number_of_monsters = randint(0, max_monsters_per_room)
		
		#Get a random number of items to place
		number_of_items = randint(0, max_items_per_room)
		
		#Place our random monsters
		for i in range(number_of_monsters):
			#Choose location in room
			x = randint(room.x + 1, room.x2 - 1)
			y = randint(room.y + 1, room.y2 - 1)
	
			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				if randint(0, 100) < 80:
					fighter_component = Fighter(hp=10, defense=0, power=5, xp=35)
					ai_component = BasicMonster()
				
					monster = Entity(x, y, 'o', libtcod.desaturated_green, "Orc", blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai= ai_component)
				else:
					fighter_component = Fighter(hp=16, defense=1, power=4, xp=100)
					ai_component = BasicMonster()
				
					monster = Entity(x, y, 'T', libtcod.darker_green, "Troll", blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
					
				entities.append(monster)
				
		for i in range(number_of_items):
			x = randint(room.x + 1, room.x2 - 1)
			y = randint(room.y + 1, room.y2 - 1)
			
			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				item = None
			
				item_chance = randint(0, 100)
				if item_chance < 70:
					item_component = Item(use_function=heal, amount=4)
					item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM, item=item_component)
				elif item_chance < 80:
					item_component = Item(use_function=cast_fireball, radius=3, damage=12, targeting=True, targeting_message=Message("Left-Click a target tile for the fireball or right-click to cancel", libtcod.light_cyan))
					item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM, item=item_component)
				elif item_chance < 90:
					item_component = Item(use_function=cast_confusion, radius=3, damage=12, targeting=True, targeting_message=Message("Left-Click an enemy to confuse it right-click to cancel", libtcod.light_cyan))
					item = Entity(x, y, '#', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM, item=item_component)
				else:
					item_component = Item(use_function=cast_lightning, maximum_range=5, damage=20)
					item = Entity(x, y, '#', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM, item=item_component)
				
				entities.append(item)
	
	def next_floor(self, player, message_log, constants):
		self.dungeon_level += 1
		entities = [player]
		
		self.tiles = self.init_tiles()
		self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities, constants['max_monsters_per_room'], constants['max_items_per_room'])
		
		player.fighter.heal(player.fighter.max_hp // 2)
		
		message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))
		
		return entities
			
	def is_blocked(self, x, y):
		if self.tiles[x][y].blocked:
			return True
		
		return False