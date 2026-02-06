from enum import Enum
from pydantic import BaseModel

from textual import on
from textual.reactive import reactive
from textual.widgets import Static, Button
from textual.containers import VerticalScroll


from Models import ScoreBoard
from Models import GameButtons
from Models import Block
from Models import Board
from Models.Definitions import PlayerLevels, PlayerLevelWeights, Default_Player_Level


class Game(Static):
	BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

	DEFAULT_CSS = '''
		Game {
			width: auto;
			height: auto;
			background: $panel;
			border-top: solid #C0C0C0;
			border-right: solid #B0B0B0;
			border-bottom: solid #808080;
			border-left: solid white;
		}

		#PlayerLevelChoice {

		}
	'''
	class Game_Config(BaseModel):								# Making a Pydantic Model
		'''
			A class to configure a new game
		'''
		Width							: int					= 10
		Height							: int					= 10
		Player_Level					: PlayerLevels			= Default_Player_Level


	def __init__(self, *args, GameConfig:"Game.Game_Config | None" = None ,**kwargs):
		super().__init__(*args, **kwargs)
		self.Config						: Game.Game_Config		= Game.Game_Config() if GameConfig == None else GameConfig		# type: ignore
		self.Board						: Board.Board			= self.Make_Board(GameConfig = self.Config)

	def watch_PlayerLevel(self, old_message: str, new_message: str) -> None:
		self.update()

	def Get_CurrentPlayerLevel_Weights(self) -> list[int]:
		return PlayerLevelWeights[self.Config.Player_Level]

	def Make_Board(self, GameConfig:"Game.Game_Config") -> Board.Board:
		'''			Returns a new Board Object with the supplied GameConfig applied			'''

		board:Board.Board=Board.Board(
			Weights = self.Get_CurrentPlayerLevel_Weights(),
			Width=GameConfig.Width,
			Height=GameConfig.Height
		)

		#self.notify(f"Made Board with Weigrhts: {self.Get_CurrentPlayerLevel_Weights()}")
		
		return board


	def compose(self):
		self.ScoreBoard 	: ScoreBoard.ScoreBoard		= ScoreBoard.ScoreBoard()
		self.GameButtons	: GameButtons.GameButtons 	= GameButtons.GameButtons()
		self.BoardContainer	: VerticalScroll			= VerticalScroll(id="BoardContainer")

		yield self.GameButtons

		yield self.ScoreBoard

		with self.BoardContainer:
			yield self.Board

	def on_mount(self):
		self.Sync_HelperComponenets()		
		#self.Update_Bombs_Remaining()

	def Update_Bombs_Remaining(self) -> int:
		'''		Updates the Scoreboard to show the latest Bomb-Remaining count and returns the Bomb Remaining Count		'''
		BombCount:int = self.Board.Get_Bombs_Remaining()
		self.ScoreBoard.Set_Bombs(Value=BombCount)
		return BombCount


	def End_Game(self, PlayerDied:bool = True):
		'''			Ends the Game			'''
		FaceStyle: str = "Happy" if not PlayerDied else "Sad"

		self.ScoreBoard.Set_FaceStyle(FaceStyle=FaceStyle)
		self.ScoreBoard.EndGame(PlayerDied=PlayerDied)
		self.Board.Reveal_All()

	def RestartGame(self):
		'''			Starts a new Game, using self.Config and Mounts it into the Game Container		'''
		self.loading = True
		self.Board.remove()

		self.Board = self.Make_Board(GameConfig=self.Config)
		self.BoardContainer.mount(self.Board)
		self.Sync_HelperComponenets()
		self.loading = False

	def Sync_HelperComponenets(self):
		'''			Syncs the Scoreboard and Game Buttons with self.Config			'''
		self.GameButtons.Set_InputForm(Level=self.Config.Player_Level, Width=self.Config.Width, Height=self.Config.Height)
		self.ScoreBoard.Restart()
		self.Update_Bombs_Remaining()


	@on(Board.Board.BoardStatus)
	def Handle_BoardStatus_Update(self, Event:Board.Board.BoardStatus):
		'''			Called by the Board when Block Count has changed or the player has died			'''
		self.ScoreBoard.Set_Bombs(Event.BombCount)
		if Event.PlayerDied:
			self.End_Game(PlayerDied=True)

		elif Event.RemainingBlockCount < 1 or Event.BombCount < 1:
			self.End_Game(PlayerDied=False)

	@on(Button.Pressed, "#Button_EndGame")
	def Handle_EndGame_Button(self, Event: Button.Pressed):
		self.End_Game()


	# @on(Button.Pressed, "#Button_NewGame")
	# def Handle_NewGame_Button(self, Event: Button.Pressed):
	# 	self.notify(f"NEW GAME BUTTON PRESSED  {Event.control.id}")
	# 	self.RestartGame()


	@on(GameButtons.GameButtons.NewGame)
	def Handle_NewGame(self, Event: GameButtons.GameButtons.NewGame):
		self.Config.Player_Level		= Event.Level
		self.Config.Width				= Event.Width
		self.Config.Height				= Event.Height
		self.RestartGame()

	