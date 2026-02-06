'''
	A Module to hold Common Definitions
'''
from enum import Enum

class PlayerLevels(Enum):
	Beginner			= 1
	Intermediate		= 2
	Expert				= 3
	BaaaHaaa			= 4

PlayerLevelWeights: dict[PlayerLevels, list[int]]	= {				# Safe Squares to Bomb Sqaures Ratio
	PlayerLevels.Beginner			: [20,1],
	PlayerLevels.Intermediate		: [10,1],
	PlayerLevels.Expert				: [3,1],
	PlayerLevels.BaaaHaaa			: [0,1]
}


Default_Player_Level		: PlayerLevels			= PlayerLevels.Intermediate


