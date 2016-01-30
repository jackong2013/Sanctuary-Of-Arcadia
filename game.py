from action import Action
from eventHandler import EventHandler
from player import Player
from objective import Objective
import random
import math

class Game(object):
	OBJECTIVE_COUNT = len(list(Objective))
	OBJECTIVE_REQUIREMENTS = {
		Objective.GrandSanctuary : [5, 2, 2]
		Objective.PhoenixsForge : [2, 5, 2]
		Objective.BankOfSmaug : [2, 2, 5]
		Objective.PegasusCruiser : [3, 3, 3] 
	}

	def __init__(self, playerIds):
		objectiveIndex = int(math.floor(random.random() * OBJECTIVE_COUNT))
		for playerId in playerIds:
			self.players = Player(playerId, Objective(objectiveIndex))
		self.eventHandler = EventHandler()
		# self.logicHandler = logicHandler()

	#options is a dictionary contains playerId for all actions
	def handleAction(self, action, options):
		if action is Action.trade:
			print "trade"
			#options contains targetPlayerIds, resourceOffer, resourceRequest
		elif action is Action.build:
			print "build"
			#options contains buildingType
		elif action is Action.gather:
			print "gather"
		elif action is Action.destroy:
			print "destroy"
			#options contains targetPlayerIds with size of one, buildingType  
		elif action is Action.upgradeResource:
			print "upgrade resource"
			#options contains resourceType
		elif action is Action.upgradeResourceGenerator:
			print "upgrade resource generator"
			#options contains resourceGeneratorType
		else: 
			print("error action")



