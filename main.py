from textual.app import App

from ui import MainMenuScreen
from appstate import AppState

class TerminalChat(App):
    async def on_mount(self) -> None:
        self.state = AppState()
        await self.push_screen(MainMenuScreen())

if __name__ == "__main__":
    #app = TerminalChat()
    #app.run()
    asd = AppState()