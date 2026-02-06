from textual.widgets import Static
from textual.reactive import reactive
from enum import Enum


Happy:list[str] = [
r'''|~~\\   /|\  ||~~/~~\|  |  ||~~|~~|~~\|~~|~~\
|__/ \ / | \ ||--'--.|  |  ||--|--|__/|--|__/
|     |  |  \||__\__/ \/ \/ |__|__|   |__|  \ ''',

r'''|__/ \ / | \ ||--'--.|  |  ||--|--|__/|--|__/
|     |  |  \||__\__/ \/ \/ |__|__|   |__|  \

''',

r'''|     |  |  \||__\__/ \/ \/ |__|__|   |__|  \

''',

'''
''',

r'''

|~~\\   /|\  ||~~/~~\|  |  ||~~|~~|~~\|~~|~~\ ''',

r'''
|~~\\   /|\  ||~~/~~\|  |  ||~~|~~|~~\|~~|~~\
|__/ \ / | \ ||--'--.|  |  ||--|--|__/|--|__/''',

r'''|~~\\   /|\  ||~~/~~\|  |  ||~~|~~|~~\|~~|~~\
|__/ \ / | \ ||--'--.|  |  ||--|--|__/|--|__/
|     |  |  \||__\__/ \/ \/ |__|__|   |__|  \ ''',

r'''|~~\\   /|\  ||~~/~~\|  |  ||~~|~~|~~\|~~|~~\
|__/ \ / | \ ||--'--.|  |  ||--|--|__/|--|__/
|     |  |  \||__\__/ \/ \/ |__|__|   |__|  \ ''',




]







class Face(Static):
	class FaceTypes(Enum):
		Happy               = 1
		Sad                 = 2
		Angry               = 3

	Faces:dict = {
		FaceTypes.Happy		: Happy,
		FaceTypes.Sad		: ["Oh No!!!! :(", "Try Again!!"],
		FaceTypes.Angry		: "GRRRRRRR!!!!!!!!!!!"
	}

	FaceStyle           : reactive[FaceTypes]   = reactive(FaceTypes.Happy)           	# This changes the displayed Face Style
	FrameNumber         : reactive[int]			= reactive(0)							# Which Frame Number in the Animation to Display

	def watch_FaceStyle(self, NewValue:int):											# If the Face Style Changes, Reset the FrameNumber to 0
		self.FrameNumber = 0


	def on_mount(self) -> None:
		self.IntervalTimer = self.set_interval(.8, self.Update_Frame)

	def Update_Frame(self):
		NewFrameNumber:int = self.FrameNumber + 1
		if NewFrameNumber >= self.Get_Frame_Count():
			NewFrameNumber = 0

		self.FrameNumber = NewFrameNumber

	def Get_Frame_Count(self) -> int:
		Val = self.Faces[self.FaceStyle]
		if type(Val) == str: return 1
		return len(Val)

	def Get_Frame_str(self) -> str:
		Val = self.Faces[self.FaceStyle]
		if type(Val) == str: return Val
		#if self.FrameNumber >= len(Val): return ""										

		return Val[self.FrameNumber]
		





	def render(self):
		return self.Get_Frame_str()


