from action import Action
from eventHandler import EventHandler
from logicHandler import LogicHandler
from player import Player

class Game(object):

	def __init__(self, playerNames):
		self.logicHandler = LogicHandler()
		self.eventHandler = EventHandler()
		self.players = []

		for playerName in playerNames:
			objective = self.logicHandler.get_random_objective()
			self.players.append(Player(playerName, objective))

	def handleAction(self, playerName, action, options):
		self.affectedPlayers = []
		player = self.getPlayerWithName(playerName)
		if player == None:
			return False

		if action is Action.TradeRequest:
			print "trade offer"

			#options contains targetPlayerNames, resourceOffer, resourceRequest
			if self.logicHandler.ingredient_suffice_to_trade(player, options["resourcesOffer"]):
				self.affectedPlayers.append(player)
				for playerName in options["targetPlayerNames"]:
					targetPlayer = self.getPlayerWithName(playerName)
					self.affectedPlayers.append(targetPlayer)
				return True
			else:
				return False
		if action is Action.TradeAccept:
			print "Trade accept"
			#options contains tradeId
			if self.logicHandler.accept_trade(player, options["resourcesOffer"], options["resourcesRequest"]):
				self.affectedPlayers.append(player) #player who accept the trade
				acceptedPlayer = self.getPlayerWithName(options["targetPlayerName"])
				self.affectedPlayers.append(acceptedPlayer)
				return True
			else:
				return False
		elif action is Action.Build or action is Action.UpgradeResourceGenerator:
			print "Build or upgrade resouce generator"
			#options contains generatorName
			if self.logicHandler.build(player, options["generatorName"]):
				self.affectedPlayers.append(player)
				return True
			else:
				return False
		elif action is Action.Gather:
			print "gather"
			multipliers = self.eventHandler.getGeneratorMultipliers()
			if self.logicHandler.gather(player, multipliers):
				self.affectedPlayers.append(player)
				return True
			else:
				return False
		elif action is Action.Destroy:
			#options contains targetPlayerName , buildingName
			print "destroy"
			targetPlayer = self.getPlayerWithName(options["targetPlayerName"])
			if self.logicHandler.destroy(player, targetPlayer, options["generatorName"]):
				self.affectedPlayers.append(player)
				self.affectedPlayers.append(targetPlayer)
				return True
			else:
				return False  
		elif action is Action.UpgradeResource:
			print "upgrade resource"
			#options contains resourceType
			if self.logicHandler.upgrade_resource(player, options["resourceName"]):
				self.affectedPlayers.append(player)
				return True
			else: 
				return False
		elif action is Action.TradeWithBank:
			print "trade with bank"
			#options contains resourcesOffer
			bankMultiplier = self.eventHandler.getBankMultiplier()
			if self.logicHandler.trade_with_bank(player, options["resourcesOffer"], options["resourcesRequest"], bankMultiplier):
				self.affectedPlayers.append(player)
				return True
			else:
				return False
		else: 
			print("error action")
			return False

	def updateEventAndGetUpcomingEvents(self):
		self.eventHandler.randomUpcomingEvent()
		currentEvents = self.eventHandler.getUpcomingEvents()


	def getPlayerWithName(self, name):
		for player in self.players:
			if player.get_name() == name:
				return player
		print "player not found"
		return None

	def playerLeft(self, player_name):
		for player in self.players:
			if (player_name == player.get_name()):
				self.players.remove(player)
				break;

	def getPlayersSummaries(self):
		playerSummary = {}
		for player in self.affectedPlayers:
			playerSummary = {}
			resources = player.get_resources()
			for res, count in resources.items():
				playerSummary[res.name] = count
			generator = player.get_generators()
			for generator, count in generator.items():
				playerSummary[generator.name] = count 
			playerSummary[player.get_name()] = playerSummary
		return playerSummary

	def getAllPlayersSummaries(self):
		allPlayerSummaries = {}
		for player in self.players:
			playerSummary = {}
			resources = player.get_resources()
			for res, count in resources.items():
				playerSummary[res.name] = count
			generator = player.get_generators()
			for generator, count in generator.items():
				playerSummary[generator.name] = count 
			allPlayerSummaries[player.get_name()] = playerSummary
		return allPlayerSummaries

	def getGeneratorsAndBankMultipliers(self):
		multipliers = {}
		for key, mutliplier in self.eventHandler.getGeneratorMultipliers.items():
			mutliplier[key.name] = multipliers
		multipliers["bank"] = self.eventHandler.getBankMultiplier()
		return multipliers
