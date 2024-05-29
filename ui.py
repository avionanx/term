from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer, Static, ListView,Label,ListItem
from textual.binding import Binding
from textual.screen import Screen
from textual.reactive import reactive
class MainMenuScreen(Screen):
    def compose(self):
        yield Header()
        yield MainMenu()
        yield Footer()

class ChatScreen(Screen):
    def __init__(self):
        super().__init__()
        self.menu = ChatMenu()
    BINDINGS = [
        Binding("e", "exit_chat", "Exit chat")
    ]
    def action_exit_chat(self) -> None:
        self.menu.add_message("Exiting chat")
    def compose(self):
        yield Header()
        yield self.menu
        yield Footer()


class ChatMenu(Static):
    def __init__(self):
        super().__init__()
    def compose(self):
        yield ListView()
    def add_message(self, message:str):
        self.query_one(ListView).append(ListItem(Label(message)))

class MainMenu(Static):
    BINDINGS = [
        Binding("key-up", "cursor_up", "Move cursor up"),
        Binding("key-down", "cursor_down", "Move cursor down"),
        Binding("space", "enter", "Select currect")
    ]
    def action_enter(self) -> None:
        match self.menulist.index:
            case 0:
                self.app.push_screen(ChatScreen())
            case 1:
                print("Two")
            case 2:
                print("Three")

    def compose(self) -> ComposeResult:
        self.menulist = ListView(
            ListItem(Label("Host chat")),
            ListItem(Label("Join chat"))
        )
        yield self.menulist
