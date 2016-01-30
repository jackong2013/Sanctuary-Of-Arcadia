from enum import Enum

class FirstResource(Enum):
	Wood = 0
	Iron = 1
	Gold = 2

class SecondResource(Enum):
	Lumber = 0
	Mithril = 1
	Treasure = 2

class FirstGenerator(Enum):
	Woodmill = 0
	IronForge = 1
	GoldMine = 2

class SecondGenerator(Enum):
	LumberMill = 0
	MithrilForge = 1
	TreasureMine = 2