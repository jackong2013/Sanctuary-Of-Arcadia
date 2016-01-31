import time
class Trade(object):
	def __init__(self, initiator, resourcesOffer, resourcesRequest, targetPlayers):
		self.initiator = initiator
		self.resourcesOffer = resourcesOffer
		self.resourcesRequest = resourcesRequest
		self.id = time.time()
		self.playersResponded = {}
		for player in targetPlayers:
			self.playersResponded[player.get_name()] = False
		self.isTradeOver = False

	def get_id(self):
		return self.id

	def get_initiator(self):
		return self.initiator

	def get_resources_offer(self):
		return self.resourcesOffer

	def get_resources_request(self):
		return self.resourcesRequest

	def get_target_players_responded(self):
		return self.playersResponded

	def get_target_players_name(self):
		return self.playersResponded.keys()

	def get_is_trade_over(self): # true if all players responded or one of the player accepted the offer
		return self.isTradeOver

	def set_is_trade_over(self, isOver):
		self.isTradeOver = isOver

	def set_player_responded(self, playerName):
		if playerName in self.playersResponded.keys():
			self.playersResponded[playerName] = True
			if False not in self.playersResponded.values():
				set_is_trade_over(True)
			return True
		else:
			print "player name not in list"
			return False


