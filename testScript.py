from eventHandler import EventHandler
from logicHandler import LogicHandler
from game import Game
from items import *
from player import Player
from event import Event
from action import Action

def printPlayerSummary():
	for player in game.affectedPlayers:
		print "*" + player.get_name() + "*"
		for res, count in player.get_resources().items():
			print res.name + " " + str(count)
		for gen, count in player.get_generators().items():
			print gen.name + " " + str(count)
		print "\n"

game = Game(["ccs", "saihou", "jack"]) 
print "TEST #1", game.handleAction("ccs", Action.Build, {"generatorName": "Woodmill"})
print "TEST #2", game.handleAction("ccs", Action.Gather, {}) # 14 12 13 
printPlayerSummary()
print "TEST #3", game.handleAction("ccs", Action.Build, {"generatorName": "Woodmill"}) 
printPlayerSummary()
print "TEST #4", game.handleAction("ccs", Action.UpgradeResource, {"resourceName": "Lumber"}) 
printPlayerSummary()
print "TEST #5", game.handleAction("ccs", Action.UpgradeResourceGenerator, {"generatorName": "LumberMill"}) 
printPlayerSummary()
print "Test #6", game.handleAction("ccs", Action.Destroy, {"generatorName": "GoldMine", "targetPlayerName": "jack"}) 
printPlayerSummary()
print "Test #7 update event and upcoming event"
game.updateEventAndGetUpcomingEvents()
game.updateEventAndGetUpcomingEvents()
game.updateEventAndGetUpcomingEvents()
game.updateEventAndGetUpcomingEvents()
game.updateEventAndGetUpcomingEvents()
print "Test #8", game.handleAction("ccs", Action.TradeWithBank, {"resourcesOffer": {}, "resourcesRequest": {}}}) 


# event = EventHandler()
# logic = LogicHandler()
# logic.destroy(sai, jack, SecondGenerator.LumberMill)
# logic.destroy(jack, sai, FirstGenerator.GoldMine)


# logic.upgrade_resource(jack, SecondResource.Lumber)
# logic.build(player, SecondGenerator.LumberMill)
# logic.build(player, SecondGenerator.TreasureMine)
# logic.build(player, FirstGenerator.GoldMine)

# logic.collect(player)


# event.changeMultiplierAccordingToEvent([Event.AngryTreeImps])
# event.changeMultiplierAccordingToEvent([Event.ArmsBan])
# event.changeMultiplierAccordingToEvent([Event.MinersStrike])
# event.changeMultiplierAccordingToEvent([Event.HappyTreeImps])
# event.changeMultiplierAccordingToEvent([Event.ArmsRace])
# event.changeMultiplierAccordingToEvent([Event.ShovelItUp])
# event.changeMultiplierAccordingToEvent([Event.BlackSwan])
# event.changeMultiplierAccordingToEvent([Event.GoodHarvest])
# event.changeMultiplierAccordingToEvent([Event.SharingIsCaring])
# event.changeMultiplierAccordingToEvent([Event.BankRupt])
# event.changeMultiplierAccordingToEvent([Event.DwarvesDay])
# event.changeMultiplierAccordingToEvent([Event.AngryTreeImps, Event.HappyTreeImps])
# event.changeMultiplierAccordingToEvent([Event.ArmsBan, Event.ArmsRace])
# event.changeMultiplierAccordingToEvent([Event.ShovelItUp, Event.MinersStrike])
# event.changeMultiplierAccordingToEvent([Event.BlackSwan, Event.HappyTreeImps])
# event.changeMultiplierAccordingToEvent([Event.BlackSwan, Event.ArmsRace])
# event.changeMultiplierAccordingToEvent([Event.ShovelItUp, Event.BlackSwan])
# event.changeMultiplierAccordingToEvent([Event.BlackSwan, Event.GoodHarvest])
# event.changeMultiplierAccordingToEvent([Event.AngryTreeImps, Event.GoodHarvest])
# event.changeMultiplierAccordingToEvent([Event.ArmsBan, Event.GoodHarvest])
# event.changeMultiplierAccordingToEvent([Event.MinersStrike, Event.GoodHarvest])
# event.changeMultiplierAccordingToEvent([Event.BankRupt, Event.DwarvesDay])
