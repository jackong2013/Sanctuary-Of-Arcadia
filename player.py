from items import FirstResource, SecondResource, FirstGenerator, SecondGenerator

class Player(object):

	def __init__(self, name, objective):
		self.name = name
		self.objective = objective
		self.inventoryFlag = False
		self.resources = {
			FirstResource.WOOD: 3,
			FirstResource.IRON: 3,
			FirstResource.GOLD: 3,
			SecondResource.LUMBER: 0,
			SecondResource.MITHRIL: 0,
			SecondResource.TREASURE: 0
		}
		self.generators = {
			FirstGenerator.WOODMILL: 0,
			FirstGenerator.IRON_FORGE: 0,
			FirstGenerator.GOLD_MINE: 0,
			SecondGenerator.LUMBER_MILL: 0,
			SecondGenerator.MITHRIL_FORGE: 0,
			SecondGenerator.TREASURE_MINE: 0
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

	# Mutator to update the number of a particular resource
	def update_generator(self, item, quantity):
		self.generators[item] += quantity
		return self.generators[item]
