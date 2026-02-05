from textual.widgets import Static
from textual.reactive import reactive
from enum import Enum

class Face(Static):
	class FaceTypes(Enum):
		Happy               = 1
		Sad                 = 2
		Angry               = 3

	Faces:dict = {
		FaceTypes.Happy: "HAPPY HAPPY\nJOY JOY"
	}

	FaceStyle           : reactive[FaceTypes]   = reactive(FaceTypes.Happy)           	# This changes the displayed Face Style
	FrameNumber         : reactive[int]			= reactive(0)							# Which Frame Number in the Animation to Display


	def on_mount(self) -> None:
		self.set_interval(1, self.Update_Frame)


	def Update_Frame(self):
		NewFrameNumber:int = self.FrameNumber + 1
		if NewFrameNumber > 2: NewFrameNumber = 0

		self.FrameNumber = NewFrameNumber



	def render(self):
		return ["HELLO","THERE","WHATSUP??"][self.FrameNumber]


		return self.Faces[self.FaceStyle]


