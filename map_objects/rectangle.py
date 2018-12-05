class Rect:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.x2 = x + width
		self.y2 = y + height
		
	def center(self):
		center_x = int((self.x + self.x2) / 2)
		center_y = int((self.y + self.y2) / 2)
		return (center_x, center_y)
		
	def intersect(self, other):
		#returns true if this rectangle intersects 'other' rect
		return (self.x <= other.x2 and self.x2 >= other.x and
				self.y <= other.y2 and self.y2 >= other.y)