class Fighter:
	def __init__(self, hp, defense, power):
		self.max_hp = hp
		self.hp = hp
		self.defense = defense
		self.power = power
	
	def take_damage(self, amount):
		results = []
		
		self.hp -= amount
		
		if self.hp <= 0:
			results.append({'dead' : self.owner})
		
		return results
		
	def attack(self, other):
		results = []
	
		damage = self.power - other.fighter.defense
		
		if damage > 0:
			results.append({'message': "{0} attacks {1} for {2} hit points.".format(self.owner.name.capitalize(), other.name, str(damage))})
		
			results.extend(other.fighter.take_damage(damage))
		else:
			results.append({'message':"{0} attacks {1} but does no damage.".format(self.owner.name.capitalize(), other.name)})
		
		return results