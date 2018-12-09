import libtcodpy as libtcod

class Stairs:
	'''
	Stairs between two levels of a dungeon
	'''
	
	def __init__(self, floor):
		self.floor = floor
		self.owner=None

