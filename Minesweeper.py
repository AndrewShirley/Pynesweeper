
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button

from Help.Help import ShowHelp
from Models import Game


class MinesweeperApp(App):
	BINDINGS = [
		("d",  "toggle_dark", "Toggle dark mode"),
		("f1", "show_help", "Help")
	]

	DEFAULT_CSS = '''
		#BoardContainer {
			width: 100%;
			height: auto;
			align: center middle;
		}
	'''
	def compose(self) -> ComposeResult:
		yield Header()

		yield Game.Game()

		yield Footer()

	def action_toggle_dark(self) -> None:
		self.theme = (
			"textual-dark" if self.theme == "textual-light" else "textual-light"
		)

	def action_show_help(self) -> None:
		ShowHelp(self)

if __name__ == "__main__":
	app = MinesweeperApp()
	app.run()