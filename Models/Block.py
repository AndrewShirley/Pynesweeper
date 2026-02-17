from textual import on
from enum import Enum
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Static
from textual.message import Message

class BlockCharacterTypes(Enum):
	Covered					= 1						# Blocks that are still UnRevealed
	Uncovered				= 2						# Blocks that are Revealed
	Marked					= 3

class BlockTypes(Enum):
	Safe					= 1						# This Block is a BOMB
	Bomb					= 2						# This Block is SAFE

class Block(Static):
	'''
		The Base-Block Class for Blocks that appear on the board
		Events:
			Click						The User Clicked the Block
	'''

	DEFAULT_CSS = '''
		Block { 
			width:  5;
			height: 3;
        	text-align: center;		
			background: #E0E0E0;
			color: black;
			border-top: solid #C0C0C0;
			border-right: solid #B0B0B0;
			border-bottom: solid #808080;
			border-left: solid white;
		}

		Block.Marked {
			background: orange;
		}

	'''

	def __init__(self, *args,  CoveredChr:str = "?", UncoveredChr: str = "!", **kwargs) -> None:
		#self._Uncovered					: bool		= False
		self.CoveredCharacter			: str				= CoveredChr				# "?" = Calculate Number based on number of adjacent bombs
		self.UnCoveredCharacter			: str				= UncoveredChr
		self.MarkedCharacter			: str				= r"\?"						# \? = ?, the "\" is an escape chr
		self.Adjacent_Bomb_Count		: int				= 0							# Number of Adjacent Bombs
		self.X							: int				= -1						# X Location of the Block
		self.Y							: int				= -1						# Y Location of the Block
		super().__init__(" ", *args, **kwargs)


	Uncovered							: reactive[bool]	= reactive(False)						# True when this Tile has been revealed
	Marked								: reactive[bool]	= reactive(False)						# True when the Player Marks this tile as a bomb




	def Get_Character(self, Which: BlockCharacterTypes) -> str:
		'''		Returns the Character to Represent this Block		'''
		match Which:
			case BlockCharacterTypes.Covered:
				return self.CoveredCharacter
			case BlockCharacterTypes.Uncovered:
				return self.UnCoveredCharacter
			case BlockCharacterTypes.Marked:
				return self.MarkedCharacter
			
		return "X"

	def Get_Current_Character(self) -> str:
		'''
			Returns the Current Character for the Block
			Rules:	If self.Marked, return self.MarkedCharacter
					Otherwise, return self.CoveredCharacter or self.UncoveredCharacter, dependent on self.Uncovered
			
		'''

		# Decide Which Character to Show on the Screen.
		# Priority Order, Highest to Lowest:    Uncovered, Marked, Covered
		# Which:BlockCharacterTypes = BlockCharacterTypes.Covered
		# if self.Marked: Which = BlockCharacterTypes.Marked
		# elif self.Uncovered: Which = BlockCharacterTypes.Uncovered

		'''
			Marked		Uncovered		Char
			0			0				Covered						[0][0]
			0			1				Uncovered					[0][1]
			1			0				Marked						[1][0]
			1			1				Uncovered					[1][1]


			[[Covered, Uncovered], [Marked, Uncovered]]

		'''
		TruthTable:list[list] = [[BlockCharacterTypes.Covered, BlockCharacterTypes.Uncovered], [BlockCharacterTypes.Marked, BlockCharacterTypes.Uncovered]]
		Which: BlockCharacterTypes = TruthTable[int(self.Marked)][int(self.Uncovered)]

		Chr: str = self.Get_Character(Which=Which)

		if Chr == "?":
			return str(self.Adjacent_Bomb_Count)

		if Chr == r"\?":
			return "?"
		
		return Chr

	def render(self):
		CurrentChr: str = self.Get_Current_Character()
		if CurrentChr == "0": CurrentChr = " "
		return CurrentChr


class Block_Bomb(Block):
	DEFAULT_CSS = '''
		Block_Bomb {
        	text-align: center;
        	content-align: center middle;
		}
	'''
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, CoveredChr = " ", UncoveredChr = "§", **kwargs)



class Block_Safe(Block):
	DEFAULT_CSS = '''
		Block_Safe {
        	text-align: center;		
        	content-align: center middle;
		}

		Block_Safe:disabled {
			background: #B0B0B0 ;
		}
	

	'''
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, CoveredChr = " ", UncoveredChr = "?", **kwargs)

