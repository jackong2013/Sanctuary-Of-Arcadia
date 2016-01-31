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
		player = getCurrentPlayer(playerName)
		if player == None:
			return False

		if action is Action.TradeRequest:
			print "trade offer"
			#options contains targetPlayerIds, resourceOffer, resourceRequest
			if logicHandler.ingredient_suffice_to_trade(player, options["resourcesOffer"]):
				self.affectedPlayers = [playerName, options["targetPlayerNames"]]
				return True
		if action is Action.TradeAccept:
			print "Trade accept"
			#options contains tradeId
		elif action is Action.Build:
			print "Build"
			#options contains buildingType
		elif action is Action.Gather:
			print "gather"
		elif action is Action.Destroy:
			print "destroy"
			#options contains targetPlayerIds with size of one, buildingType  
		elif action is Action.UpgradeResource:
			print "upgrade resource"
			#options contains resourceType
		elif action is Action.UpgradeResourceGenerator:
			print "upgrade resource generator"
			#options contains resourceGeneratorType
		else: 
			print("error action")

	def getCurrentPlayer(self, name):
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



