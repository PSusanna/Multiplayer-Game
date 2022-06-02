import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.50.167"
        self.port = 7778
        self.addr = (self.server, self.port)

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode("utf-8")

    def disconnect(self):
        self.client.close()

    def send(self, data):
        self.client.send(str.encode(data))

    def receive(self):
        return self.client.recv(2048).decode("utf-8")
