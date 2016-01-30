import logicHandler as lgc

class Player(object):

	def __init__(self, name, objective):
		self.name = name
		self.objective = objective
		self.inventoryFlag = False
		self.resources = {
			lgc.WOOD: 3,
			lgc.IRON: 3,
			lgc.GOLD: 3,
			lgc.LUMBER: 0,
			lgc.MITHRIL: 0,
			lgc.TREASURE: 0
		}
		self.generators = {
			lgc.WOODMILL: 0,
			lgc.IRON_FORGE: 0,
			lgc.GOLD_MINE: 0,
			lgc.LUMBER_MILL: 0,
			lgc.MITHRIL_FORGE: 0,
			lgc.TREASURE_MINE: 0
		}

	# Accessor for the name
	def get_name(self):
		return self.name

	# Accessor for resources
	def get_resources(self):
		return self.resources

	# Accessor for second tier generator
	def get_generators(self):
		return self.generators

	# Accessor to get the number of a particular resource that this Person has
	def get_resource_count(self, resource):
		if resource in self.resources.keys():
			return self.resources[resource]
		else:
			return 'WRONG RESOURCE NAME!!! This game does not have ' + resource

	# Accessor to get the number of a particular generator that this Person has
	def get_generator_count(self, generator):
		if generator in self.generators.keys():
			return self.generators[generator]
		else:
			return 'WRONG GENERATOR NAME!!! This game does not have ' + generator

	# Mutator to update the number of a particular resource
	def update_resource(self, item, quantity):
		self.resources[item] += quantity
		return self.resources[item]
		# if item in self.resources.keys():
		# 	temp = self.resources[item] + quantity
		# 	if temp < 0:
		# 		return "YOU DO NOT HAVE ENOUGH " + item
		# 	else:
		# 		self.resources[item] = temp
		# 		self.inventoryFlag = False if self.inventory_vacant() else True
		# elif item in self.generators.keys():
		# 	temp = self.generators[item] + quantity
		# 	if temp < 0:
		# 		return "YOU DO NOT HAVE ENOUGH " + item
		# 	else:
		# 		self.generators[item] = temp
		# else:
		# 	return 'WRONG ITEM NAME!!! This game does not have ' + item

	# Mutator to update the number of a particular resource
	def update_generator(self, item, quantity):
		self.generators[item] += quantity
		return self.generators[item]

	# Method to check if there is space in the inventory
	def inventory_vacant(self):
		count = 0
		for res in self.resources.keys():
			if res in lgc.FIRST_TIER_RESOURCE:
				count += self.resources[res]
			if count > lgc.INVENTORY_CAP:
				return False
		return True

	# Method to check if the player has enough resources to build an item
	def ingredient_suffice(self, item):
		can_build = True
		for ingredient, qty in lgc.COST[item].items():
			if qty > self.get_resources()[ingredient]:
				can_build = False
				return can_build
		return can_build
		

	def build(self, item):
		if item in COST.keys():
			if self.ingredient_suffice(item) and item = self.objective:
				return "GAME OVER"
			elif self.ingredient_suffice(item):
				for ingredient, qty in COST[item].items():
					self.update_item(ingredient, -1*qty)
				self.update_item(item, 1)
			else:
				return "NOT ENOUGH INGREDIENT TO BUILD " + item
		else:
			return 'WRONG ITEM NAME!!! This game does not have ' + item

	def gather(self):
