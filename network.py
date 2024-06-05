import socket
import threading
from enum import Enum
from queue import Queue, Empty
class Host:
    def __init__(self, log_queue:Queue):
        self.host = "127.0.0.1"
        self.port = 9001
        self.log_queue = log_queue
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.log_queue.put("Started server")
    def start(self):
        self.log_queue.put("Listening for connections")
        while True:
            client_socket, addr = self.server.accept()
            self.clients.append(client_socket)
            self.log_queue.put(f"Connection from {addr} has been established")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
    def handle_client(self, client_socket:socket.socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.log_queue.put(message)
                self.broadcast(message, client_socket)
            except:
                self.log_queue.put(f"Connection from {client_socket.getpeername()} has been terminated")
                client_socket.close()
                self.clients.remove(client_socket)
                break

    def broadcast(self, message, client_socket = None):
        if client_socket is None:
            client_socket = self.server
        
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(str(message).encode('utf-8'))
                except:
                    self.log_queue.put(f"Connection from {client.getpeername()} has been terminated")
                    client.close()
                    self.clients.remove(client)
## Can only connect to local machine (localhost) for now, should run on seperate thread aswell
class Client:
    def __init__(self, log_queue:Queue):
        self.host = "127.0.0.1"
        self.port = 9001
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.log_queue = log_queue
    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                self.log_queue.put(message)
            except:
                self.client.close()
                break
    def send(self, message):
        self.client.send(str(message).encode('utf-8'))


class NetworkState(Enum):
    HOST = 1
    CLIENT = 2
