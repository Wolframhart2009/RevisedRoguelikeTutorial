from map_objects.tile import Tile

class GameMap:
	"""
	A container for the tiles that are part of the current map screen
	"""
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.tiles = self.init_tiles()
		
	def init_tiles(self):
		tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
		
		tiles[30][22].blocked = True
		tiles[30][22].block_sight = True
		tiles[31][22].blocked = True
		tiles[31][22].block_sight = True
		tiles[32][22].blocked = True
		tiles[32][22].block_sight = True
		
		return tiles
		
	def is_blocked(self, x, y):
		if self.tiles[x][y].blocked:
			return True
		
		return False