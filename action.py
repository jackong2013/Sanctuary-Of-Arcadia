from enum import Enum

class Action(Enum):
	build = 1
	gather = 2
	trade = 3
	destroy = 4
	upgradeResource = 5
	upgradeResourceGenerator = 6