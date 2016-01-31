from enum import Enum

class Action(Enum):
	Build = 1
	Gather = 2
	TradeRequest = 3
	TradeAccept = 4
	Destroy = 5
	UpgradeResource = 6
	UpgradeResourceGenerator = 7
	TradeWithBank = 8