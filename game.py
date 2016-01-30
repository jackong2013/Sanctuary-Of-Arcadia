from action import Action
from eventHandler import EventHandler
from player import Player

class Game(object):
	def __init__(self, playerIds):
		# objectiveIndex = int(math.floor(random.random() * OBJECTIVE_COUNT))
		# for playerId in playerIds:
		# 	self.players = Player(playerId, Objective(objectiveIndex))
		self.eventHandler = EventHandler()
		# self.logicHandler = logicHandler()

	def handleAction(self, playerId, action, options):
		if action is Action.TradeRequest:
			print "trade offer"
			#options contains targetPlayerIds, resourceOffer, resourceRequest
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

	def playerLeft(self, player_name):
		for player in self.players:
			if (player_name == player.get_name()):
				self.players.remove(player)
				break;



