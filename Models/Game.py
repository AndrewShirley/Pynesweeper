from textual import on
from textual.reactive import reactive
from textual.widgets import Static, RadioSet, RadioButton

from Models import Block
from Models import Board
from enum import Enum

class PlayerLevels(Enum):
		Beginner			= 1
		Intermediate		= 2
		Expert				= 3
		BaaaHaaa			= 4



class Game(Static):
	BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

	DEFAULT_CSS = '''
		Game {
			width: auto;
			height: auto;
/*			border: solid purple; */
		}

		#PlayerLevelChoice {

		}
	'''
	PlayerLevel				= reactive(PlayerLevels.Beginner)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.Board						: Board.Board
		#self.PlayerLevel				: PlayerLevels	= PlayerLevels.Beginner

	def watch_PlayerLevel(self, old_message: str, new_message: str) -> None:
		self.update()

	PlayerLevelWeights: dict[PlayerLevels, list[int]]	= {				# Safe Squares to Bomb Sqaures Ratio
		PlayerLevels.Beginner			: [20,1],
		PlayerLevels.Intermediate		: [10,1],
		PlayerLevels.Expert				: [5,1],
		PlayerLevels.BaaaHaaa			: [0,1]
	}

	def Get_CurrentPlayerLevel_Weights(self) -> list[int]:
		return self.PlayerLevelWeights[self.PlayerLevel]

	def compose(self):
		Width			: int		= 30
		Height			: int		= 20
		self.Board = Board.Board(Weights = self.Get_CurrentPlayerLevel_Weights(), Width=Width, Height=Height)
		yield self.Board


	@on(RadioSet.Changed, "#PlayerLevelChoice")
	def Handle_PlayerLevel_Changed(self, Event: RadioSet.Changed):
		self.PlayerLevel = PlayerLevels[Event.pressed.id]						# type: ignore
		self.update()

