class Tile:
	"""
	A tile on a map. It may or may not be blocked from movement or sight
	"""
	
	def __init__(self, blocked, block_sight=None):
		self.blocked = blocked
		
		# By default if tile is blocked it also blocks sight
		if block_sight is None:
			self.block_sight = blocked
		else:
			self.block_sight = block_sight