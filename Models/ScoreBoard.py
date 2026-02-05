from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Static, Digits
from textual.containers import Horizontal
from Models import Face
from time import time

class ScoreBoard(Static):
	DEFAULT_CSS = '''
		ScoreBoard {
			height: 7;
    		layout: grid;
			grid-size: 3 1;
			grid-columns: 1fr 1fr 1fr;
		}

		Face {
			width: auto;
		}

		#BombsLeft {
			width: auto;
		}

		#Face {
			width: auto;
		}

		#ElapsedTime {
			width: auto;
		}

		#Container_BombsLeft {
			height: 100%;
			width: 1fr;
			border: round $border;
			align: center middle;
			border-title-align: center;
			border-title-color: $text-secondary;
		}

		#Container_StatusFace {
			height: 100%;
			width: 1fr;
			border: round $border;
			align: center middle;
			border-title-align: center;
		}

		#Container_ElapsedTime {
			height: 100%;
			width: 1fr;
			border: round $border;
			align: center middle;
			border-title-align: center;
			border-title-color: $text-secondary;
		}

	'''

	StartTime         : reactive[float]			= reactive(time())			# Game Start Time

	def on_mount(self) -> None:
		self.set_interval(1, self.Update_Time)

	def Update_Time(self):
		'''
			Update the Timer Widger with the current elapsed seconds since game start
			This function is called by Textual every second. The Timer is set in .on_mount
		'''
		ElapsedSeconds:int  =  int(time() - self.StartTime)
		self.Set_Timer(Value=ElapsedSeconds)

	def Set_Timer(self, Value:int):
		'''
			Sets the Value displayed in the "Seconds" Panel
		'''
		self.Panel_Timer.update(f"{Value:03}")

	def Set_Bombs(self, Value: int):
		'''
			Sets the Value displayed in the "Bombs" panel
		'''
		self.Panel_BombsCount.update(f"{Value:03}")


	def compose(self):
		with Static(id="Container_BombsLeft") as S:
			S.border_title = "Bombs"
			self.Panel_BombsCount:Digits = Digits("999", id="BombsLeft")
			yield self.Panel_BombsCount

		with Static(id="Container_StatusFace") as S:
			yield Face.Face()
			#yield Static(":)", id="Face")

		with Static(id="Container_ElapsedTime") as S:
			S.border_title = "Seconds"
			self.Panel_Timer:Digits = Digits("000", id="ElapsedTime")
			yield self.Panel_Timer
	
	def Reset_Timer(self, Value:int = 0):
		'''
			Resets and Redraws the Timer with an optional value (defaults to 0)
			Args:
				Value			int		(Optional)		Value to set the timer to (0=Default)
		'''
		self.StartTime = time()

