from action import Action

class Game(object):
	def __init__(self, players):
		self.players = players
		# self.eventHandler = eventHandler()
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



