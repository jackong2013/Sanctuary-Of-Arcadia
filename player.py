INVENTORY_CAP = 10
WOOD = 'wood'
IRON = 'iron'
GOLD = 'gold'
LUMBER = 'lumber'
MITHRIL = 'mithril'
TREASURE = 'treasure'
WOODMILL = 'woodmill'
IRON_FORGE = 'ironForge'
GOLD_MINE = 'goldMine'
LUMBER_MILL = 'lumberMill'
MITHRIL_FORGE = 'mithrilForge'
TREASURE_MINE = 'treasureMine'
GRAND_SANCTUARY = 'grandSanctuary'
PHOENIX_FORGE = 'phoenixForge'
BANK_SMAUG = 'bankSmaug'
PEGASUS_CRUISER = 'pegasusCruiser'
FIRST_TIER_RESOURCE = [WOOD, IRON, GOLD]
SECOND_TIER_RESOURCE = [LUMBER, MITHRIL, TREASURE]
FIRST_TIER_GENERATOR = { WOODMILL: 1, IRON_FORGE: 1, GOLD_MINE: 1 }
SECOND_TIER_GENERATOR = { LUMBER_MILL: 3, MITHRIL_FORGE: 3, TREASURE_MINE: 3}
COST = {
	LUMBER: { WOOD: 2 },
	MITHRIL: { IRON: 2 },
	TREASURE: {	GOLD: 2 },
	WOODMILL: { WOOD: 3, IRON: 1, GOLD: 1 },
	IRON_FORGE: { WOOD: 1, IRON: 3, GOLD: 1 },
	GOLD_MINE: { WOOD: 1, IRON: 1, GOLD: 3 },
	LUMBER_MILL: { WOODMILL: 1, LUMBER: 1, IRON: 1, GOLD: 1},
	MITHRIL_FORGE: { IRON_FORGE: 1, MITHRIL: 1, WOOD: 1, GOLD: 1},
	TREASURE_MINE: { GOLD_MINE: 1, TREASURE: 1, WOOD: 1, IRON: 1},
	GRAND_SANCTUARY: { LUMBER: 5, TREASURE: 2, MITHRIL: 2},
	PHOENIX_FORGE: { LUMBER: 2, TREASURE: 2, MITHRIL: 5},
	BANK_SMAUG: { LUMBER: 2, TREASURE: 5, MITHRIL: 2},
	PEGASUS_CRUISER: { LUMBER: 3, TREASURE: 3, MITHRIL: 3}
}

class Player(object):

	def __init__(self, name, objective):
		self.name = name
		self.objective = objective
		self.inventoryFlag = False
		self.resources = {
			WOOD: 3,
			IRON: 3,
			GOLD: 3,
			LUMBER: 0,
			MITHRIL: 0,
			TREASURE: 0
		}
		self.generators = {
			WOODMILL: 0,
			IRON_FORGE: 0,
			GOLD_MINE: 0,
			LUMBER_MILL: 0,
			MITHRIL_FORGE: 0,
			TREASURE_MINE: 0
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

	# Accessor to check if there is space in the inventory
	def inventory_vacant(self):
		count = 0
		for res in self.resources.keys():
			if res in FIRST_TIER_RESOURCE:
				count += self.resources[res]
			if count > INVENTORY_CAP:
				return False
		return True

	# Mutator to update the number of a particular resource
	def update_resource(self, resource, quantity):
		if resource in self.resources.keys():
			temp = self.resources[resource] + quantity
			if temp < 0:
				return "YOU DO NOT HAVE ENOUGH " + resource
			else:
				self.resources[resource] = temp
				self.inventoryFlag = False if self.inventory_vacant() else True
		else:
			return 'WRONG RESOURCE NAME!!! This game does not have ' + resource

	def build(self):
		pass


