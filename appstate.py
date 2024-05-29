from network import Host
import threading
class AppState:
    def __init__(self):
        self.user_name = "Icarus"
        self.host = Host()
        self.start_network()
    def start_network(self):
        self.network_thread = threading.Thread(target=self.host.start)
        self.network_thread.start()