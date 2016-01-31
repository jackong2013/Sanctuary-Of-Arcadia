from items import FirstResource, SecondResource, FirstGenerator, SecondGenerator

class Player(object):

	def __init__(self, name, objective):
		self.name = name
		self.objective = objective
		self.inventoryFlag = False
		self.resources = {
			FirstResource.Wood: 10,
			FirstResource.Iron: 10,
			FirstResource.Gold: 10,
			SecondResource.Lumber: 2,
			SecondResource.Mithril: 2,
			SecondResource.Treasure: 2
		}
		self.generators = {
			FirstGenerator.Woodmill: 1,
			FirstGenerator.IronForge: 2,
			FirstGenerator.GoldMine: 3,
			SecondGenerator.LumberMill: 1,
			SecondGenerator.MithrilForge: 0,
			SecondGenerator.TreasureMine: 0
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
