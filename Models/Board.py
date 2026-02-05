from textual import on
from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal
import random

from Models import Block

'''
	Blocks are Stored in a 2X2 List:
	Row
		0	Block_Col1		Block_Col2		Block_Col3		Block.....
		1	Block_Col1		Block_Col2		Block_Col3		Block.....
		2	Block_Col1		Block_Col2		Block_Col3		Block.....
		.
		.
		.
'''
class Board(Static):
	'''
		A Class to represent an entire PlayBoard's Blocks
	'''

	DEFAULT_CSS = '''
		Board {
			width: auto;
			height: auto;
			border: heavy #404040;			
		}

	.BlockRow {
		width:auto;
		height: auto;
	}
	'''

	def __init__(self, Width:int = 30, Height:int = 20, Weights:list[int] = [10,1]):
		super().__init__()
		self.Width          : int                       		= Width
		self.Height         : int                       		= Height
		self.Blocks         : list[list[Block.Block]]							# Use Create_Blocks_Matrix to create the 2X2 Matrix
		self.Weights		: list[int]							= Weights		# A List of Weights when randomly choosing Block Types.

		self.Create_Blocks_Matrix()												# Create a new self.Blocks List and Generate Random Blocks 
		self.Set_Adjacent_Bombs_Counts()										# Sets all the square's Adjacent_Bomb_Count attribute

	def Create_Blocks_Matrix(self):
		'''		Creates the 2X2 Blocks Matrix, setting each Block to None		'''
		self.Blocks = []
		for Y in range(self.Height):
			self.Blocks.append([])												# Make a new Row
			for X in range(self.Width):
				B:Block.Block = self.Get_Random_Block()
				B.X = X
				B.Y = Y
				self.Blocks[Y].append(B)	# Make all the Columns in the new Row

	def Get_Block(self, X:int, Y:int) -> Block.Block:
		return self.Blocks[Y][X]


	def Set_Block(self, X:int, Y:int, Block:Block.Block):
		self.Blocks[Y][X] = Block


	def Get_Random_Block(self) -> Block.Block:
		'''			Generates a Random Block using self.Weights			'''
		BlockStyle: Block.BlockTypes = random.choices(list(Block.BlockTypes), self.Weights)[0]
		match BlockStyle:
			case Block.BlockTypes.Bomb:
				return Block.Block_Bomb(classes="Block")
			case Block.BlockTypes.Safe:
				return Block.Block_Safe(classes="Block")
			
		raise ValueError(f"Random Block Chosen, But is not a known Block")

	def compose(self):
		for Y in range(self.Height):
			with Horizontal(classes="BlockRow"):
				for X in range(self.Width):
					yield self.Get_Block(X=X, Y=Y)

	def Calculate_Adjacent_Bombs(self, block:Block.Block) -> int:
		'''		Calculates the Number of Bombs that the given Block is attached to		'''
		Bombs_Counter: int = 0
		#BombList:list[Block.Block] = self.Get_Adjacent_Blocks(block=block, AddThisBlock=False)
		BombList:set[Block.Block] = self.Query_Blocks(AroundBlock=block)
		
		for B in BombList:
			Bombs_Counter += 1 if type(B) is Block.Block_Bomb else 0

		return Bombs_Counter

	def Reveal_Adjacent_Blocks(self, block:Block.Block, Exclude:list[Block.Block] = []):
		'''
			Reveals the Blocks Adjacent to the one supplied.
			Args:
				Exclude					: A List of Types to exclude, ie: [Block_Bomb]		
		'''

		#BlockList: list[Block.Block] = self.Get_Adjacent_Blocks(block = block, AddThisBlock=True)
		BlockList: set[Block.Block] = self.Query_Blocks(AroundBlock=block)
		BlockList.add(block)

		for B in BlockList:
			if not type(B) in Exclude:
				B.Uncovered = True


	def Query_Blocks(self, NoBombs:bool = False, AroundBlock:Block.Block | None = None, MaxLevels:int = 1) -> set[Block.Block]:
		'''
			Query for Blocks around a given Block, optionally searching neighbours
			Args:
				NoBombs						True = Return No Blocks that are Bombs
				AroundBlock					The Block to search around. If No Block is provided (None) then
											the block at (0,0) is used as the starting point
				MaxLevels					The Maximum number of Child-Levels to search.
				 							1 = Only blocks immediately surrounding the AroundBlock are searched
			Returns:
				A New Set with the Resultant Blocks, including the ones passed in with AddToSet
		'''
		return self._Query_Blocks(NoBombs=NoBombs, AroundBlock=AroundBlock, MaxLevels=MaxLevels)


	def _Query_Blocks(self, NoBombs:bool = False,OnlyZeros:bool = False,  AroundBlock:Block.Block | None = None, MaxLevels:int = 1, AddToSet:set[Block.Block] | None = None) -> set[Block.Block]:
		# If no AroundBlock was provided, get the first block from Coords (0,0)
		BaseBlock:Block.Block = self.Get_Block(X=0, Y=0) if AroundBlock is None else AroundBlock
		Seed			: bool = AddToSet is None							# True means this is the first time into the function before any recursion

		BlockSet		: set = set() if AddToSet is None else AddToSet		# Ensure we have a set to work with
		#VisitBlocks		: set = set()										# A Set of Child Blocks to visit if MaxLevels > 1

		StartRow		: int = max(BaseBlock.Y - 1, 0)
		EndRow			: int = min(self.Height - 1, BaseBlock.Y + 1)
		StartCol		: int = max(BaseBlock.X - 1, 0)
		EndCol			: int = min(self.Width - 1, BaseBlock.X + 1)

		for Y in range(StartRow, EndRow + 1):								# range() function stops at .stop-1
			for X in range(StartCol, EndCol + 1):
				if X == BaseBlock.X and Y == BaseBlock.Y: continue			# Skip the Block we're inquiring about
				#Coords.append((X,Y))
				block:Block.Block = self.Get_Block(X=X, Y=Y)

				# Apply Filters
				if NoBombs and type(block) == Block.Block_Bomb:
					continue

				if OnlyZeros and block.Adjacent_Bomb_Count != 0:
					continue

				# If the Block hasn't been added to the set yet, add it and optionally visit its neighbours
				if not block in BlockSet:								# If the Block hasn't been added yet...
					BlockSet.add(block)									# Add it, then Visit its Descendants

					# Prevent Recursion overruns
					if MaxLevels > 1:
						BlockSet = self._Query_Blocks(
							NoBombs=NoBombs,
							OnlyZeros=OnlyZeros,
							AroundBlock=block,
							MaxLevels=MaxLevels-1,
							AddToSet=BlockSet
						)

		return BlockSet

	def Set_Adjacent_Bombs_Counts(self):
		'''			Sets the Adjacent Bombs Counts on each Tile in the Board		'''
		Counts:list = []
		for Row in self.Blocks:
			for block in Row:
				BombCount	: int		= self.Calculate_Adjacent_Bombs(block = block)
				Counts.append(BombCount)
				block.Adjacent_Bomb_Count = BombCount

		#self.notify(f"Counts={Counts}")

	@on(Block.Block.Click)
	def Handle_Click(self, Event: Block.Block.Click):
		#Event.Control.Uncovered = True
		#self.Reveal_Adjacent_Blocks(Block_X=Event.Control.X, Block_Y=Event.Control.Y)
		#self.notify(f"{Event.Control.Adjacent_Bomb_Count}")
		self.Reveal_Adjacent_Blocks(block=Event.Control) #, Exclude=[Block.Block_Bomb])

		match type(Event.Control):
			case Block.Block_Bomb:
				self.notify("YOU BLEW UP!!!!")



