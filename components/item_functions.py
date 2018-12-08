import libtcodpy as libtcod

from game_messages import Message
from entity import Entity
from components.fighter import Fighter
from components.ai import ConfusedMonster

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
	
def cast_lightning(*args, **kwargs):
	#Lighning function to be assigned to items
	#args[0] = caster
	#kwargs['entities'] list of entities around
	#kwargs['fov_map'] what caster is able to see
	#kwargs['damage'] amount of damage to do
	#kwargs['maximum_range'] max range to shoot at
	
	caster = args[0]
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	damage = kwargs.get('damage')
	maximum_range = kwargs.get('maximum_range')
	
	results = []
	
	closest_distance = maximum_range + 1
	
	target = None
	for entity in entities:
		if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
			distance = caster.distance_to(entity)
			
			if distance < closest_distance:
				target = entity
				closest_distance = distance
	if target:
		results.append({
			'consumed': True,
			'target': target,
			'message': Message('a lightning bolt strikes the {0} with a thunderous bang! The damage is {1}'.format(target.name, damage), libtcod.white)
		})
		results.extend(target.fighter.take_damage(damage))
	else:
		results.append({
			'consumed': False,
			'target': None,
			'message': Message('No enemy in range!', libtcod.red)
		})
	
	return results
	
def cast_fireball(*args, **kwargs):
	#Fireball function to be assigned to items
	#args[0] = caster
	#kwargs['entities'] list of entities around
	#kwargs['fov_map'] what caster is able to see
	#kwargs['damage'] amount of damage to do
	#kwargs['radius'] the area to from the targeted square to effect
	#kwargs['target_x'] targeted square's x to effect
	#kwargs['target_y'] targeted square's y to effect
	
	caster = args[0]
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	damage = kwargs.get('damage')
	radius = kwargs.get('radius')
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')
	
	results = []
		
	if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
		results.append({
			'consumed': False,
			'message': Message('You cannot target a tile you cannot see')
		})
		return results
	
	results.append({
		'consumed': True,
		'message': Message('The fireball explodes, burning everything within {0} tiles'.format(radius), libtcod.orange)
	})
	
	target = None
	for entity in entities:
		if entity.fighter and entity.distance(target_x, target_y) <= radius:
			results.append({
				'message': Message('The {0} gets burned for {1} hit points'.format(entity.name, damage), libtcod.orange)
			})
			results.extend(entity.fighter.take_damage(damage))
		
	return results
	
def cast_confusion(*args, **kwargs):
	#Fireball function to be assigned to items
	#args[0] = caster
	#kwargs['entities'] list of entities around
	#kwargs['fov_map'] what caster is able to seet
	#kwargs['target_x'] targeted square's x to effect
	#kwargs['target_y'] targeted square's y to effect
	
	caster = args[0]
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')
	
	results = []
		
	if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
		results.append({
			'consumed': False,
			'message': Message('You cannot target a tile you cannot see')
		})
		return results
	
	target = None
	for entity in entities:
		if entity.ai and entity.x == target_x and entity.y == target_y:
			confused_ai = ConfusedMonster(entity.ai, 10)
			confused_ai.owner = entity
			
			entity.ai = confused_ai
			
			results.append({
				'consumed': True,
				'message': Message('The eyes of the {0} look vacant and they begin to stumble around'.format(entity.name), libtcod.light_green)
			})
			
			break
	else:
		results.append({
			'consumed': False,
			'message': Message('There is no targetable enemy on that tile'.format(entity.name, damage), libtcod.yellow)
		})
		
	return results
	