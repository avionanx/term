from network import Host, Client, NetworkState
import threading
from terminal import TerminalChat
from queue import Queue, Empty
class AppState:
    def __init__(self):
        self.user_name = "Icarus"
        self.app = TerminalChat(self)
        self.network_state: NetworkState
        self.log_queue = Queue()
    def start_network(self):
        if self.network_state == NetworkState.HOST:
            self.host = Host(self.log_queue)
            self.network_thread = threading.Thread(target=self.host.start)
            self.network_thread.start()
        elif self.network_state == NetworkState.CLIENT:
            self.client = Client(self.log_queue)
            self.network_thread = threading.Thread(target=self.client.start)
            self.network_thread.start()
    def run(self):
        self.app.run()

