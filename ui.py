from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Vertical
from textual.widgets import Header, Footer, Static, ListView,Label,ListItem, Input, Rule
from textual.binding import Binding
from textual.screen import Screen
from textual.reactive import reactive
from textual import on
from network import NetworkState
from queue import Empty
from message import MessageType, SystemMessage, UserMessage
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
        Binding("Enter", "send_message", "Send message")
    ]
    def action_send_message(self) -> None:
        pass
        
    def compose(self):
        yield Header()
        yield self.menu
        yield Footer()


class ChatMenu(Static):
    def __init__(self, ):
        super().__init__()
    def compose(self):
        yield Input()
        yield ListView()
    async def on_mount(self):
        self.app.state.start_network()
        self.set_interval(1/60, self.check_message_queue)

    def check_message_queue(self):
        try:
            message = self.app.state.log_queue.get_nowait()
            self.add_peer_message(message)
        except Empty:
            pass
    @on(Input.Submitted)
    def input_submitted(self, event:Input.Submitted):
        self.add_message(event.value)
        if self.app.state.network_state == NetworkState.HOST:
            self.app.state.host.broadcast(UserMessage(event.value, self.app.state.user_name))
        elif self.app.state.network_state == NetworkState.CLIENT:
            self.app.state.client.send(UserMessage(event.value, self.app.state.user_name))
        self.query_one(Input).value = ""
    def add_message(self, message:str):
        self.query_one(ListView).append(ListItem(Label(self.parent.parent.state.user_name + ': ' +message)))
    def add_peer_message(self, message:str):
        self.query_one(ListView).append(ListItem(Label(message)))
    def add_sys_message(self, message:str):
        self.query_one(ListView).append(ListItem(Label('[System]: ' +message)))

class MainMenu(Static):
    BINDINGS = [
        Binding("key-up", "cursor_up", "Move cursor up"),
        Binding("key-down", "cursor_down", "Move cursor down"),
        Binding("space", "enter", "Select currect")
    ]
    def action_enter(self) -> None:
        match self.menulist.index:
            case 0:
                self.app.state.network_state = NetworkState.HOST
                self.app.push_screen(ChatScreen())
            case 1:
                self.app.state.network_state = NetworkState.CLIENT
                self.app.push_screen(ChatScreen())
            case 2:
                print("Three")

    def compose(self) -> ComposeResult:
        self.menulist = ListView(
            ListItem(Label("Host chat")),
            ListItem(Label("Join chat"))
        )
        yield self.menulist
