'''
	A Widget to display Help for Pynesweeper
'''


from textual.screen import Screen
from textual.containers import Container
from textual.widgets import Static, Button

HelpText:str = '''
 ____                                                           __     ___   ___  
|  _ \ _   _ _ __   ___  _____      _____  ___ _ __   ___ _ __  \ \   / / | / _ \ 
| |_) | | | | '_ \ / _ \/ __\ \ /\ / / _ \/ _ \ '_ \ / _ \ '__|  \ \ / /| || | | |
|  __/| |_| | | | |  __/\__ \\ V  V  /  __/  __/ |_) |  __/ |      \ V / | || |_| |
|_|    \__, |_| |_|\___||___/ \_/\_/ \___|\___| .__/ \___|_|       \_/  |_(_)___/ 
       |___/                                  |_|                                 


[u b $accent]Pynesweeper V1.0 by Andrew Shirley - 2026[/]
Written in Python for the Windows and Linux Bash Terminals.

[u b $accent]Game Play:[/]
The Game of Pynesweeper contists of a 2-dimensional board consisting of many tiles, each tile being one of two types:
	- Safe Tiles
	- Mines (bombs)

Initially, each tile is hidden with no mention of which type of tile it is. Your job, should you choose it, is to uncover each tile, exposing the safe tiles and the bombs.

To do this, you click tiles to reveal them.

[u b $accent]Rules:[/]
Clicking a "Safe" tile will reveal the number of bombs the tile is directly next to.
When that is 0, a blank tile is shown.
When clicking a tile with 0 bombs attached, all connected safe tiles surrounding the clicked tile and its attached neighbours is displayed

Clicking a "Bomb" tile will explode the tile, ending the game.

To Win the game, you need to uncover all of the safe tiles or mark all of the bomb tiles.

[u b $accent]Controls:[/]
Right-Click				Mark / UnMark a Tile as a Bomb. The tile changes colour to show a Marked bomb
Left-Click				Uncover a Tile.
					If the Tile is NOT a bomb, it will be uncovered.

'''

class Help(Container):
	DEFAULT_CSS = '''
		Help {
			height: auto;
		}

	'''

	def compose(self):
		yield Static(HelpText)


class Help_Modal(Screen):
	def compose(self):
		yield Help()
		yield Button("OK", id="ok_button", variant="primary")


	def on_button_pressed(self, event: Button.Pressed) -> None:
		#if event.button.id == "ok_button":
		self.app.pop_screen()

def ShowHelp(App):
	Modal: Help_Modal = Help_Modal()
	App.push_screen(Modal)