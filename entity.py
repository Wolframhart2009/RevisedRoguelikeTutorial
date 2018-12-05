class Entity:
	"""
	A generic object that represents an interactable players, items, enemies, etc
	"""
	
	def __init__(self, x, y, char, color):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		
	def move(self, dx, dy):
		#Moves the entity from x, y by dx, dy
		self.x += dx
		self.y += dy