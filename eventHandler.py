import random
import math
from event import Event

class EventHandler(object):
	MAX_COUNT_DOWN_ROUNDS_FOR_EVENT = 3 # in n rounds the event happens, next round, 2nd round, 3rd round .. nth round might happen
	NUMBER_OF_EVENTS = 11
	ANGRY_TREE_IMP_MULTIPLIER = 0
	ARMS_BAN_MULTIPLIER = 0
	MINERS_STRIKE_MULTIPLIER = 0
	HAPPY_TREE_IMP_MULTIPLIER = 2
	ARMS_RACE_MULTIPLIER = 2
	SHOVEL_IT_UP_MULTIPLIER = 2
	BLACK_SWAN_MULTIPLIER = 0
	GOOD_HARVEST_MULTIPLIER = 2
	BANK_RUPT_MULTIPLIER = 0
	DWARVES_DAY_MULTIPLIER = 1

	def __init__(self):
		self.happenInRounds = [-1] * EventHandler.NUMBER_OF_EVENTS
		self.woodmillMultiplier = 1
		self.ironForgeMultiplier = 1
		self.goldMineMultiplier = 1
		self.bankMultiplier = 0.5

	def setFirstTierMultiplier(self, multiplier):
		self.setWoodmillMultiplier(multiplier)
		self.setIronForgetMultiplier(multiplier)
		self.setGoldMineMultiplier(multiplier)

	def setWoodmillMultiplier(self, multiplier):
		self.woodmillMultiplier = multiplier

	def setIronForgetMultiplier(self, multiplier):
		self.ironForgeMultiplier = multiplier

	def setGoldMineMultiplier(self, multiplier):
		self.goldMineMultiplier = multiplier

	def setBankMultiplier(self, multiplier):
		self.bankMultiplier = multiplier

	def getWoodmillMultiplier(self):
		return self.woodmillMultiplier

	def getIronForgetMultiplier(self):
		return self.ironForgeMultiplier

	def getGoldMineMultiplier(self):
		return self.goldMineMultiplier

	def getBankMultiplier(self):
		return self.bankMultiplier

	def randomUpcomingEvent(self):
		for i in range(0, EventHandler.NUMBER_OF_EVENTS):
			self.happenInRounds[i] = self.happenInRounds[i] - 1 if self.happenInRounds[i] >= 0 else self.happenInRounds[i]
		randomIndex = int(math.floor(random.random() * EventHandler.NUMBER_OF_EVENTS))

		countDownRounds = int(math.ceil(random.random() * EventHandler.MAX_COUNT_DOWN_ROUNDS_FOR_EVENT))
		print "count down rounds " + str(countDownRounds)
		self.happenInRounds[randomIndex] = countDownRounds
		print self.happenInRounds

	def getCurrentEvents(self):
		currentEvents = []
		for i in range(0, EventHandler.NUMBER_OF_EVENTS):
			if self.happenInRounds[i] == 0:
				currentEvents.append(Event(i))
		
		self.changeMultiplierAccordingToEvent(currentEvents)
		return currentEvents

	def changeMultiplierAccordingToEvent(self, events):
		self.resetMultiplier()
		for event in events:
			if event is Event.AngryTreeImps:
				print "angry tree imps"
				self.setWoodmillMultiplier(EventHandler.ANGRY_TREE_IMP_MULTIPLIER)
			elif event is Event.ArmsBan:
				print "arms ban"
				self.setIronForgetMultiplier(EventHandler.ARMS_BAN_MULTIPLIER)
			elif event is Event.MinersStrike:
				print "miners strike"
				self.setGoldMineMultiplier(EventHandler.MINERS_STRIKE_MULTIPLIER)
			elif event is Event.HappyTreeImps:
				print "happy tree imps"
				# stop by angry tree imps and black swan
				if Event.AngryTreeImps in events or Event.BlackSwan in events:
					print "angry tree imps or black swan happens too"
					continue
				self.setWoodmillMultiplier(EventHandler.HAPPY_TREE_IMP_MULTIPLIER)
			elif event is Event.ArmsRace:
				print "ArmsRace"	
				# stop by arms ban and black swan
				if Event.ArmsBan in events or Event.BlackSwan in events:
					print "arms ban or black swan happens too"
					continue
				self.setIronForgetMultiplier(EventHandler.ARMS_RACE_MULTIPLIER)
			elif event is Event.ShovelItUp:
				print "ShovelItUp"	
				#stop by miners strike and black swan
				if Event.MinersStrike in events or Event.BlackSwan in events:
					print "miners strike or black swan happens too"
					continue
				self.setGoldMineMultiplier(EventHandler.SHOVEL_IT_UP_MULTIPLIER)
			elif event is Event.BlackSwan:
				print "BlackSwan"	
				self.setFirstTierMultiplier(EventHandler.BLACK_SWAN_MULTIPLIER)
			elif event is Event.GoodHarvest:
				print "GoodHarvest"	
				#stop by black swan
				if Event.BlackSwan in events:
					print "swan happens too"
					continue

				self.setFirstTierMultiplier(EventHandler.GOOD_HARVEST_MULTIPLIER)

				if Event.AngryTreeImps in events: 
					self.setWoodmillMultiplier(EventHandler.ANGRY_TREE_IMP_MULTIPLIER)
				if Event.ArmsBan in events: 
					self.setIronForgetMultiplier(EventHandler.ARMS_BAN_MULTIPLIER)
				if Event.MinersStrike in events: 
					self.setGoldMineMultiplier(EventHandler.MINERS_STRIKE_MULTIPLIER)
			elif event is Event.BankRupt:
				print "BankRupt"	
				self.setBankMultiplier(EventHandler.BANK_RUPT_MULTIPLIER)
			elif event is Event.DwarvesDay:
				print "DwarvesDay"	
				#stop by bank rupt
				if Event.BankRupt in events:
					print "bank rupt happens too"
					continue
				self.setBankMultiplier(EventHandler.DWARVES_DAY_MULTIPLIER)
			else:
				print "error event"
		print str(self.woodmillMultiplier) + " " \
			+ str(self.ironForgeMultiplier) + " " \
			+ str(self.goldMineMultiplier) + " " \
			+ str(self.bankMultiplier) + "\n"
	
	def resetMultiplier(self):
		self.setFirstTierMultiplier(1)
		self.setBankMultiplier(0.5)




