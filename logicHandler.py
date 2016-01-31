from items import FirstResource, SecondResource, FirstGenerator, SecondGenerator
from objective import Objective

class LogicHandler(object):
	INVENTORY_CAP = 10
	GENERATOR_CAPACITY = { 
		FirstGenerator.Woodmill: {
			'resource': FirstResource.Wood,
			'capacity': 1 
		},
		FirstGenerator.IronForge: {
			'resource': FirstResource.Iron,
			'capacity': 1 
		}, 
		FirstGenerator.GoldMine: {
			'resource': FirstResource.Gold,
			'capacity': 1 
		}, 
		SecondGenerator.LumberMill: {
			'resource': FirstResource.Wood,
			'capacity': 3
		}, 
		SecondGenerator.MithrilForge: {
			'resource': FirstResource.Iron,
			'capacity': 3
		}, 
		SecondGenerator.TreasureMine: {
			'resource': FirstResource.Gold,
			'capacity': 3
		}
	}

	COST = {
		SecondResource.Lumber: { FirstResource.Wood: 2 },
		SecondResource.Mithril: { FirstResource.Iron: 2 },
		SecondResource.Treasure: { FirstResource.Gold: 2 },
		FirstGenerator.Woodmill: { 
			FirstResource.Wood: 3, 
			FirstResource.Iron: 1, 
			FirstResource.Gold: 1 
		},
		FirstGenerator.IronForge: { 
			FirstResource.Wood: 1, 
			FirstResource.Iron: 3, 
			FirstResource.Gold: 1 
		},
		FirstGenerator.GoldMine: { 
			FirstResource.Wood: 1, 
			FirstResource.Iron: 1, 
			FirstResource.Gold: 3 
		},
		SecondGenerator.LumberMill: { 
			FirstGenerator.Woodmill: 1, 
			SecondResource.Lumber: 1, 
			FirstResource.Iron: 1, 
			FirstResource.Gold: 1
		},
		SecondGenerator.MithrilForge: { 
			FirstGenerator.IronForge: 1, 
			SecondResource.Mithril: 1, 
			FirstResource.Wood: 1, 
			FirstResource.Gold: 1
		},
		SecondGenerator.TreasureMine: { 
			FirstGenerator.GoldMine: 1, 
			SecondResource.Treasure: 1, 
			FirstResource.Wood: 1, 
			FirstResource.Iron: 1
		},
		Objective.GrandSanctuary: { 
			SecondResource.Lumber: 5, 
			SecondResource.Treasure: 2, 
			SecondResource.Mithril: 2
		},
		Objective.PhoenixsForge: { 
			SecondResource.Lumber: 2, 
			SecondResource.Treasure: 2, 
			SecondResource.Mithril: 5
		},
		Objective.BankOfSmaug: { 
			SecondResource.Lumber: 2, 
			SecondResource.Treasure: 5, 
			SecondResource.Mithril: 2
		},
		Objective.PegasusCruiser: { 
			SecondResource.Lumber: 3, 
			SecondResource.Treasure: 3, 
			SecondResource.Mithril: 3
		}
	}
		
	def __init__(self):
		self.nothing = None

	# Check if a user have vacancy in inventory
	def inventory_vacant(self, player):
		count = 0
		resources = player.get_resources()
		for res in list(FirstResource):
			count += resources[res]
			if count > LogicHandler.INVENTORY_CAP:
				return False
		return True

	# Check if the player has enough resources to build an item
	def ingredient_suffice(self, player, item):
		can_build = True
		resources = player.get_resources()
		generators = player.get_generators()
		for ingredient, cost in LogicHandler.COST[item].items():
			if ingredient in list(FirstGenerator):
				if cost > generators[ingredient]:
					can_build = False
					return can_build
			else:
				if cost > resources[ingredient]:
					can_build = False
					return can_build
		return can_build

	def collect(self, player, multipliers):
		generators = player.get_generators()
		for generator, qty in generators.items():
			resource = LogicHandler.GENERATOR_CAPACITY[generator]['resource']
			capacity = LogicHandler.GENERATOR_CAPACITY[generator]['capacity']
			multiplier = 1 if generator not in multipliers.keys() else multipliers[generator]
			income = qty * multiplier * capacity
			player.update_resource(resource, income)

	def upgrade_resource(self, player, target):
		if self.ingredient_suffice(player, target):
			player.update_resource(target, 1)
			for res, cost in LogicHandler.COST[target].items():
				player.update_resource(res, -1 * cost)
			return True
		else:
			return False

	def build(self, player, target):
		if self.ingredient_suffice(player, target):
			player.update_generator(target, 1)
			for res, cost in LogicHandler.COST[target].items():
				if res in list(FirstGenerator):
					player.update_generator(res, -1 * cost)
				else:
					player.update_resource(res, -1 * cost)
			return True
		else:
			return False

	def destroy(self, initiator, victim, target):
		#caculate cost for target
		if self.ingredient_suffice(initiator, target):
			victim.update_generator(target, -1)
			for res, cost in LogicHandler.COST[target].items():
				if res in list(FirstGenerator):
					initiator.update_generator(res, -1 * cost)
				else:
					initiator.update_resource(res, -1 * cost)
