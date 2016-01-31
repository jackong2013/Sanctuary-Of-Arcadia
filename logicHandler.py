from items import FirstResource, SecondResource, FirstGenerator, SecondGenerator
from objective import Objective
import random
import math

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
	isAcceptingTrade = False
		
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

	def gather(self, player, multipliers):
		generators = player.get_generators()
		for generator, qty in generators.items():
			resource = LogicHandler.GENERATOR_CAPACITY[generator]['resource']
			capacity = LogicHandler.GENERATOR_CAPACITY[generator]['capacity']
			multiplier = 1 if generator not in multipliers.keys() else multipliers[generator]
			income = qty * multiplier * capacity
			player.update_resource(resource, income)
		return True

	def upgrade_resource(self, player, target):
		targetResource = self.get_resource_with_name(target)
		if not targetResource: 
			return False

		if self.ingredient_suffice(player, targetResource):
			player.update_resource(targetResource, 1)
			for res, cost in LogicHandler.COST[targetResource].items():
				player.update_resource(res, -1 * cost)
			return True
		else:
			return False

	def build(self, player, target):
		targetGenerator = self.get_generator_with_name(target)
		if not targetGenerator:
			return False

		if self.ingredient_suffice(player, targetGenerator):
			player.update_generator(targetGenerator, 1)
			for res, cost in LogicHandler.COST[targetGenerator].items():
				if res in list(FirstGenerator):
					player.update_generator(res, -1 * cost)
				else:
					player.update_resource(res, -1 * cost)
			return True
		else:
			return False

	def destroy(self, initiator, victim, target):
		#caculate cost for target
		targetGenerator = self.get_generator_with_name(target)
		if not targetGenerator:
			return False
			
		if self.ingredient_suffice(initiator, targetGenerator):
			victim.update_generator(targetGenerator, -1)
			for res, cost in LogicHandler.COST[targetGenerator].items():
				if res in list(FirstGenerator):
					initiator.update_generator(res, -1 * cost)
				else:
					initiator.update_resource(res, -1 * cost)
			return True
		else:
			return False

	def get_resource_with_name(self, name):
		for res in list(FirstResource) + list(SecondResource):
			if res.name.lower() == name.lower():
				return res
		print "resource enum with name " + name + " not found"
		return None

	def get_generator_with_name(self, name):
		for generator in list(FirstGenerator) + list(SecondGenerator):
			if generator.name.lower() == name.lower():
				return generator
		print "generator enum with name " + name + " not found"
		return None

	#trade has 3 kinds
	# 1 Open Trade
	# 2 1-1 Trade
	# 3 1-n Trade
	def ingredient_suffice_to_trade(self, player, resourcesOffer):
		#make sure initiator has enough resources to offer
		playerResources = player.get_resources()
		playerGenerators = player.get_generators()
		for res, count in resourcesOffer.items(): # res is string, dictionary in enum
			targetResource = self.get_resource_with_name(res)
			if targetResource in list(FirstResource) + list(SecondResource) and count > playerResources[targetResource] or \
				targetResource in list(FirstGenerator) + list(SecondGenerator) and count > playerGenerators[targetResource]:
				return False
		return True

	def accept_trade(self, initiator, resourcesOffer, resourcesRequest, acceptedPlayer):
		if LogicHandler.isAcceptingTrade: 
			return False
		LogicHandler.isAcceptingTrade = True
		acceptedPlayerResources = acceptedPlayer.get_resources()
		acceptedPlayerGenerators = acceptedPlayer.get_generators()
		for res, count in resourcesRequest.items():
			targetResource = self.get_resource_with_name(res)
			#make sure accepted player has enough resources to accept
			if targetResource in list(FirstResource) + list(SecondResource) and count > acceptedPlayerResources[targetResource] or \
				targetResource in list(FirstGenerator) + list(SecondGenerator) and count > acceptedPlayerGenerators[targetResource]:
				LogicHandler.isAcceptingTrade = False
				return False

			#update accepted player resources/generators
			if targetResource in list(FirstResource) + list(SecondResource):
				acceptedPlayer.update_resource(targetResource, -count)
			else:
				acceptedPlayer.update_generator(targetResource, -count)

		#update initiator resources/generators
		for res, count in resourcesOffer.items():
			targetResource = self.get_resource_with_name(res)
			if targetResource in list(FirstResource) + list(SecondResource):
				initiator.update_resource(targetResource, -count)
			else:
				initiator.update_generator(targetResource, -count)
		LogicHandler.isAcceptingTrade = False
		return True

	def get_random_objective(self):
		randomObjectiveCount = len(list(Objective))
		randomIndex = int(math.floor(random.random() * randomObjectiveCount))
		return randomIndex




