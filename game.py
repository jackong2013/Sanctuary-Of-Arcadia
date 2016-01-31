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
		self.jsonResponse = {}

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

		self.jsonResponse = None

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
				makeTradeTemplateJson(self.currentTrade)
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
				self.makeUpdateTemplateJson()
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
				self.makeUpdateTemplateJson()
				return True
			else:
				return False
		elif action is Action.Build or action is Action.UpgradeResourceGenerator:
			print "Build or upgrade resouce generator"
			#options contains generatorName
			if self.logicHandler.build(player, options["generator"]):
				self.affectedPlayers.append(player)
				self.makeUpdateTemplateJson()
				return True
			else:
				return False
		elif action is Action.Gather:
			print "gather"
			multipliers = self.eventHandler.getGeneratorMultipliers()
			if self.logicHandler.gather(player, multipliers):
				self.affectedPlayers.append(player)
				self.makeUpdateTemplateJson()
				return True
			else:
				return False
		elif action is Action.Destroy:
			#options contains targetPlayerName , buildingName
			print "destroy"
			targetPlayer = self.getPlayerWithName(options["to"])
			if self.logicHandler.destroy(player, targetPlayer, options["generator"]):
				self.affectedPlayers.append(player)
				self.affectedPlayers.append(targetPlayer)
				self.makeUpdateTemplateJson()
				return True
			else:
				return False  
		elif action is Action.UpgradeResource:
			print "upgrade resource"
			#options contains resourceType
			if self.logicHandler.upgrade_resource(player, options["resource"]):
				self.affectedPlayers.append(player)
				self.makeUpdateTemplateJson()
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

	def getAffectedPlayersSummaries(self):
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

	def increaseTurns(self):
		self.turns += 1

	def getCurrentTurnPlayerName(self):
		return self.players[self.getTurns() % len(self.players)].get_name()

	def makeUpdateTemplateJson(self):
		json = {}
		json['action'] = "Update"
		json['update_res'] = self.getAffectedPlayersSummaries() 
		self.jsonResponse = json

	def makeTradeTemplateJson(self, trade):
		json = {}
		json['action'] = "TradeRequest"
		json['from'] = trade.get_initiator()
		json['to'] = trade.get_target_players_name()
		json['want'] = trade.get_resources_request()
		json['offer'] = trade.get_resources_offer()
		json['tid'] = trade.get_id()
		self.jsonResponse = json

	def getJsonResponse(self):
		return self.jsonResponse

