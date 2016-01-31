from action import Action
from eventHandler import EventHandler
from logicHandler import LogicHandler
from player import Player
from trade import Trade

class Game(object):
	def __init__(self, playerNames):
		self.logicHandler = LogicHandler()
		self.eventHandler = EventHandler()
		self.players = []
		self.turns = 0

		for playerName in playerNames:
			objective = self.logicHandler.get_random_objective()
			self.players.append(Player(playerName, objective))

	def handleAction(self, playerName, action, options):
		if self.getCurrentTurnPlayerName() != playerName:
			return False

		self.affectedPlayers = []
		player = self.getPlayerWithName(playerName)
		if player == None:
			return False

		if action is Action.TradeRequest:
			print "trade offer"
			#options contains targetPlayerNames, resourceOffer, resourceRequest
			targetPlayerNames = options["targetPlayerNames"]
			resourcesOffer = options["resourcesOffer"]
			resourcesRequest = options["resourcesRequest"]

			if not targetPlayerNames or not resourcesOffer or not resourcesRequest:
				return False

			targetPlayers = []
			for name in targetPlayerNames:
				targetPlayer = self.getPlayerWithName(name)
				targetPlayers.append(targetPlayer)

			if self.logicHandler.ingredient_suffice_to_trade(player, resourcesOffer):
				self.currentTrade = Trade(player, resourcesOffer, resourcesRequest, targetPlayers)
				self.affectedPlayers.append(player)
				for playerName in targetPlayerNames:
					targetPlayer = self.getPlayerWithName(playerName)
					self.affectedPlayers.append(targetPlayer)
				return True
			else:
				return False
		if action is Action.TradeAccept:
			print "Trade accept"
			#options contains tradeId
			tradeId = options["tradeId"]
			if not self.isTradeValidWithIdAndName(tradeId, player.get_name()):
				return False 
			if self.logicHandler.accept_trade(player, self.currentTrade):
				self.currentTrade.set_player_responded(player.get_name())
				self.affectedPlayers.append(player) #player who accept the trade
				self.affectedPlayers.append(self.currentTrade.get_initiator())
				return True
			else:
				return False
		elif action is Action.TradeDeny:
			print "trade deny"
			#options contains tradeId
			tradeId = options["tradeId"]
			if not self.isTradeValidWithIdAndName(tradeId, player.get_name()):
				return False 

			self.currentTrade.set_player_responded(player.get_name())
			return True
		elif action is Action.TradeWithBank:
			print "trade with bank"
			#options contains resourcesOffer, resourcesRequest
			bankMultiplier = self.eventHandler.getBankMultiplier()
			if self.logicHandler.trade_with_bank(player, options["resourcesOffer"], options["resourcesRequest"], bankMultiplier):
				self.affectedPlayers.append(player)
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
		else: 
			print("error action")
			return False

	def isTradeValidWithIdAndName(self, tradeId, playerName):
		if not tradeId or tradeId != self.currentTrade.get_id() or \
			playerName not in self.currentTrade.get_target_players_name():
			return False

		if self.currentTrade.get_is_trade_over():
			print("trade is over")
			return False

		return True


	def updateEventAndGetUpcomingEvents(self):
		self.eventHandler.randomUpcomingEvent()
		currentEvents = self.eventHandler.getUpcomingEvents()
		self.turns += 1


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
			for gen, count in generator.items():
				playerSummary[gen.name] = count 
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
			for gen, count in generator.items():
				playerSummary[gen.name] = count 
			allPlayerSummaries[player.get_name()] = playerSummary
		return allPlayerSummaries

	def getGeneratorsAndBankMultipliers(self):
		multipliers = {}
		for key, mutliplier in self.eventHandler.getGeneratorMultipliers.items():
			mutliplier[key.name] = multipliers
		multipliers["bank"] = self.eventHandler.getBankMultiplier()
		return multipliers

	def getTradeId(self):
		return self.currentTrade.get_id()

	def getIsTradeOver(self):
		return self.currentTrade.get_is_trade_over()

	def getTurns(self):
		return self.turns

	def getCurrentTurnPlayerName(self):
		return self.players[self.getTurns() % len(self.players)].get_name()