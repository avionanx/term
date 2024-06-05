from textual.app import App

from ui import MainMenuScreen

class TerminalChat(App):
    CSS_PATH = "css.tcss"
    def __init__(self, state):
        super().__init__()
        self.state = state
    async def on_mount(self) -> None:
        await self.push_screen(MainMenuScreen())