import libtcodpy as libtcod

from game_messages import Message
from entity import Entity
from components.fighter import Fighter

def heal(*args, **kwargs):
	#Heal function to be assigned to items
	#Breakdown: arg[0] should be entity being healed
	#kwargs['amount'] should be amount to heal bytearray
	
	entity = args[0]
	amount = kwargs.get('amount')
	
	results = []
	
	if entity.fighter.hp == entity.fighter.max_hp:
		results.append({
			'consumed': False,
			'message': Message('You are already at full health', libtcod.yellow)
		})
	else:
		entity.fighter.heal(amount)
		results.append({
			'consumed': True,
			'message': Message('Your wounds start to feel better', libtcod.green)
		})
		
	return results