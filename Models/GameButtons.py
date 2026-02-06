from textual import on
from textual.widgets import Static, Button, RadioButton, RadioSet, Input, Label
from Models.Definitions import PlayerLevels
from textual.message import Message
from textual.validation import Number


#from textual.containers import Horizontal

class GameButtons(Static):

	DEFAULT_CSS = '''
		GameButtons {
			layout: horizontal;
		}

		GameButtons RadioSet {
			layout: horizontal;
		}

		
		#Input_Width {
			width: 12;
		}

		#Input_Height {
			width: 12;
		}


		#BoardSizeContainer {
			layout: horizontal;
			width: auto;
		}

	'''

	class NewGame(Message):
		'''			Message Raised when a new Game has been Chosen by the player		'''
		Level		: PlayerLevels
		Width		: int
		Height		: int
		

	def Raise_NewGame(self, Level:PlayerLevels, Width:int, Height:int):
		Msg			: GameButtons.NewGame		= GameButtons.NewGame()
		Msg.Level								= Level
		Msg.Width								= Width
		Msg.Height								= Height
		self.post_message(Msg)


	def compose(self):
		self.RadioSet_PlayerLevels	: RadioSet = RadioSet()
		self.Input_Width			: Input = Input(
			"10",
			id="Input_Width",
			type="integer",
			valid_empty=False, 
			validators=[
				Number(minimum=10, maximum=200),
			],			
		)
		self.Input_Height			: Input = Input(
			"10",
			id="Input_Height",
			type="integer",
			valid_empty=False, 			
			validators=[
				Number(minimum=10, maximum=200),
			],			

		)

		yield Button("END GAME", id="Button_EndGame")


		with Static(id="BoardSizeContainer"):
			yield Label("Board:")

			yield self.Input_Width
			yield Label("X")
			yield self.Input_Height

		yield Button("NEW GAME", id="Button_NewGame")

		with self.RadioSet_PlayerLevels:
			for Level in PlayerLevels:
				yield RadioButton(Level.name, id=Level.name)


	def InputFormIsValid(self) -> bool:
		Valid_Width		: bool			= self.Input_Width.validate(self.Input_Width.value).is_valid
		Valid_Height	: bool			= self.Input_Height.validate(self.Input_Height.value).is_valid
		Valid_Level		: bool			= self.RadioSet_PlayerLevels.pressed_index >= 0

		return Valid_Width and Valid_Height and Valid_Level

	@on(Button.Pressed, "#Button_NewGame")
	def Handle_NewButton_Pressed(self, Event: Button.Pressed):
		Event.stop()
		if not self.InputFormIsValid():
			self.notify("Please Input Width and Height from 10-200 and Selected a Player Level")
			return

		Width			: int			= int(self.Input_Width.value)
		Height			: int			= int(self.Input_Height.value)
		Level			: PlayerLevels	= PlayerLevels[self.RadioSet_PlayerLevels.pressed_button.id]


		self.Raise_NewGame(Level=Level, Width=Width, Height=Height)


	def Set_InputForm(self, Level: PlayerLevels, Width: int, Height:int):
		self.Input_Width.value = str(Width)
		self.Input_Height.value = str(Height)
		self.RadioSet_PlayerLevels.value = Level.name

		self.query_one(f"#{Level.name}").value = True