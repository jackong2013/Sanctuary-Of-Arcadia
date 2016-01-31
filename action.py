from enum import Enum

class Action(Enum):
	Build = 1
	Gather = 2
	TradeRequest = 3
	TradeAccept = 4
	TradeDeny = 5
	TradeWithBank = 6
	Destroy = 7
	UpgradeResource = 8
	UpgradeResourceGenerator = 9
	