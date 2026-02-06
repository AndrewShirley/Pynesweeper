from typing import Callable

from textual import on
from textual.message import Message
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


	Iterate over ALL blocks, regardless of Row and Column with:
	for block in BoardObj:
		print(block.X, block.Y)
'''
class Board(Static):
	'''
		A Class to represent an entire PlayBoard's Blocks
	'''

	DEFAULT_CSS = '''
		Board {
			width: auto;
			height: auto;
			border-top: heavy #C0C0C0;
			border-right: heavy #B0B0B0;
			border-bottom: heavy #808080;
			border-left: heavy white;
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
		self.PlayerDied		: bool								= False			# Has the Played Died?
		self.Create_Blocks_Matrix()												# Create a new self.Blocks List and Generate Random Blocks 
		self.Set_Adjacent_Bombs_Counts()										# Sets all the square's Adjacent_Bomb_Count attribute

	def __iter__(self):
		return BoardIterator(self)
	
	class BoardStatus(Message):
		'''			A Message to Pass on Board Status Updates		'''
		BombCount					: int		= 0
		RemainingBlockCount			: int		= 0
		PlayerDied					: bool		= False


	
	def Create_Blocks_Matrix(self):
		'''		Creates the 2X2 Blocks Matrix, setting each Block to a Random Block, using Player Level Weights		'''
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
		BombList:set[Block.Block] = self.Query_Blocks(AroundBlock=block, FilterFunc=lambda B: type(B) == Block.Block_Bomb)
		return len(BombList)

	def Reveal_Adjacent_Blocks(self, block:Block.Block, Exclude:list[Block.Block] = [], Travel:bool=False, DisableBlocks:bool=True):
		'''
			Reveals the Blocks Adjacent to the one supplied.
			Args:
				Exclude					: A List of Types to exclude, ie: [Block_Bomb]		
				Travel					: Visit outside of immediate adjacent Blocks when their Adjacent Bomb Count is ZERO
		'''
		BlockList: set[Block.Block] = self.Query_Blocks(AroundBlock=block, Travel = Travel)
		BlockList.add(block)
		for B in BlockList:
			if not type(B) in Exclude:
				B.Uncovered = True
				if DisableBlocks: B.disabled = True

	def Reveal_All(self):
		for block in self:
			block.Uncovered = True


	def Query_Blocks(self, AroundBlock:Block.Block, FilterFunc:Callable | None = None, Travel:bool=True) -> set[Block.Block]:
		'''
			Query for Blocks around a given Block, optionally searching along paths of blocks that have 0 adjacent bombs
			Args:
				NoBombs						True = Return No Blocks that are Bombs
				AroundBlock					The Block to search around. If No Block is provided (None) then
											the block at (0,0) is used as the starting point
				Travel						True = Also Visit distance relatives (ie: blocks attached to blocks attached to....)
				MaxLevels					The Maximum number of Child-Levels to search.
				 							1 = Only blocks immediately surrounding the AroundBlock are searched
			Returns:
				A New Set with the Resultant Blocks, including the ones passed in with AddToSet
		'''
		MaxLevels		: int = 99 if Travel else 1

		return self._Query_Blocks(FilterFunc=FilterFunc, AroundBlock=AroundBlock, MaxLevels=MaxLevels)


	def _Query_Blocks(self, AroundBlock:Block.Block, FilterFunc:Callable | None = None, MaxLevels:int = 1, AddToSet:set[Block.Block] | None = None) -> set[Block.Block]:


		# If no AroundBlock was provided, get the first block from Coords (0,0)
		BaseBlock:Block.Block = self.Get_Block(X=0, Y=0) if AroundBlock is None else AroundBlock

		BlockSet		: set = set() if AddToSet is None else AddToSet		# Ensure we have a set to work with

		StartRow		: int = max(BaseBlock.Y - 1, 0)
		EndRow			: int = min(self.Height - 1, BaseBlock.Y + 1)
		StartCol		: int = max(BaseBlock.X - 1, 0)
		EndCol			: int = min(self.Width - 1, BaseBlock.X + 1)

		for Y in range(StartRow, EndRow + 1):								# range() function stops at .stop-1
			for X in range(StartCol, EndCol + 1):
				if X == BaseBlock.X and Y == BaseBlock.Y: continue			# Skip the Block we're inquiring about
				block:Block.Block = self.Get_Block(X=X, Y=Y)
				if block in BlockSet: continue								# If the Block is already in the result set, ignore it

				if FilterFunc!= None and not FilterFunc(block):				# If A Filter Function was supplied, call it. Returns False = Filter it out
					continue

				BlockSet.add(block)

				# Prevent Recursion overruns
				if MaxLevels > 1 and block.Adjacent_Bomb_Count == 0 and not type(block) == Block.Block_Bomb:
					BlockSet = self._Query_Blocks(
						FilterFunc=FilterFunc,
						AroundBlock=block,
						MaxLevels=MaxLevels-1,
						AddToSet=BlockSet
					)

		return BlockSet

	def Set_Adjacent_Bombs_Counts(self):
		'''			Sets the Adjacent Bombs Counts on each Tile in the Board		'''
		for block in self:
			BombCount	: int		= self.Calculate_Adjacent_Bombs(block = block)
			block.Adjacent_Bomb_Count = BombCount


	def Get_Bombs_Remaining(self) -> int:
		return len([B for B in self if not B.Marked and type(B) == Block.Block_Bomb])


	def Get_Uncovered_SafeBlocks_Remaining(self) -> int:
		return len([B for B in self if not B.Uncovered and not type(B) == Block.Block_Bomb])

	def on_click(self, Event):
		'''			Called when the Played Clicks a Block		'''
		if Event.control.Uncovered: return											# Don't Process Blocks that are uncovered

		match Event.button:
			case 1:																	# Left Mouse Button
				Event.control.Uncovered = True
				Event.control.disabled = True										# Disable the Block to change its Visual Style
				match type(Event.control):
					case Block.Block_Bomb:
						self.PlayerDied = True
					case _:															# Default Behaviour for Non-Bombs
						if Event.control.Adjacent_Bomb_Count == 0:					# Clicked on a Tile with NO Bombs. Auto Reveal All Attached through Zeros
							self.Reveal_Adjacent_Blocks(block=Event.control, Exclude=[Block.Block_Bomb], Travel=True, DisableBlocks=True)							# type: ignore

			case _:																	# Any Mouse Button but the Left One
				Marked:bool = not Event.control.Marked
				if Marked:
					Event.control.add_class("Marked")
				else:
					Event.control.remove_class("Marked")

				Event.control.Marked = Marked

		self.Raise_BoardStatus()


	def Raise_BoardStatus(self):
		'''			Raises a "Board Status" Message			'''
		BS:Board.BoardStatus = Board.BoardStatus()
		BS.PlayerDied				= self.PlayerDied
		BS.BombCount				= self.Get_Bombs_Remaining()
		BS.RemainingBlockCount		= self.Get_Uncovered_SafeBlocks_Remaining()
		self.post_message(message=BS)

	def DisableBoard(self):
		self.disabled = True



class BoardIterator:
    '''
        Iterator class for traversing a Board's 2D blocks matrix.
        Iterates column-by-column across each row, then moves to the next row.
    '''
    
    def __init__(self, board: 'Board'):
        self.Board = board
        self.RowIndex = 0
        self.ColumnIndex = 0
    
    def __iter__(self):
        return self
    
    def __next__(self) -> Block.Block:
        '''
            Returns the next Block in the 2D matrix.
            Traverses column-by-column across each row, then moves to the next row.
            Raises StopIteration when all blocks have been returned.
        '''
        # Check if we've reached the end of the matrix
        if self.RowIndex >= self.Board.Height:
            raise StopIteration
        
        # Get the current block
        block = self.Board.Get_Block(X=self.ColumnIndex, Y=self.RowIndex)
        
        # Move to the next position
        self.ColumnIndex += 1
        if self.ColumnIndex >= self.Board.Width:
            self.ColumnIndex = 0
            self.RowIndex += 1


       
        return block
	
