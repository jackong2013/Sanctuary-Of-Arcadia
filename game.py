from action import Action
from eventHandler import EventHandler
from player import Player

class Game(object):
	def __init__(self, playerNames):
		for playerName in playerNames:
			objective = logicHandler.get_random_objective()
			self.players = Player(playerName, objective)
		self.eventHandler = EventHandler()
		self.logicHandler = logicHandler()

	def handleAction(self, playerName, action, options):
		self.affectedPlayers = []
		player = self.getPlayerWithName(playerName)
		if player == None:
			return False

		if action is Action.TradeRequest:
			print "trade offer"
			#options contains targetPlayerNames, resourceOffer, resourceRequest
			if logicHandler.ingredient_suffice_to_trade(player, options["resourcesOffer"]):
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
			if logicHandler.accept_trade(player, options["resourcesOffer"], options["resourcesRequest"]):
				self.affectedPlayers.append(player) #player who accept the trade
				acceptedPlayer = self.getPlayerWithName(options["targetPlayerName"])
				self.affectedPlayers.append(acceptedPlayer)
				return True
			else:
				return False
		elif action is Action.Build or action is Action.UpgradeResourceGenerator:
			print "Build or upgrade resouce generator"
			#options contains generatorName
			if logicHandler.build(player, options["generatorName"]):
				self.affectedPlayers.append(player)
				return True
			else:
				return False
		elif action is Action.Gather:
			print "gather"
			multipliers = self.eventHandler.getGeneratorMultipliers()
			if logicHandler.gather(player, multipliers):
				self.affectedPlayers.append(player)
				return True
			else:
				return False
		elif action is Action.Destroy:
			print "destroy"
			targetPlayer = self.getPlayerWithName(options["targetPlayerName"])
			if logicHandler.destroy(player, targetPlayer, options["generatorName"]):
				self.affectedPlayers.append(player)
				self.affectedPlayers.append(targetPlayer)
				return True
			else:
				return False
			#options contains targetPlayerNames with size of one, buildingType  
		elif action is Action.UpgradeResource:
			print "upgrade resource"
			#options contains resourceType
			if logicHandler.UpgradeResource(player, options["resourceName"]):
				return True
			else: 
				return False
		else: 
			print("error action")
			return False

	def updateEventAndGetUpcomingEvents(self):
		self.eventHandler.randomUpcomingEvent()
		let currentEvents = self.eventHandler.getCurrentEvents()

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
		playerSummaries = []
		for player in self.affectedPlayers:
			playerSummary = {}
			resources = player.get_resources()
			for res, count in resources.items()
				playerSummary[res.name] = count
			for generator, count in generator.items()
				playerSummary[generator.name] = count 
			playerSummaries.append(playerSummary)
		return playerSummaries



