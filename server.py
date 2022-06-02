import socket
import threading
import sys

server = "192.168.50.167"
port = 7778
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server,port))
except socket.error as e:
    print('hi')
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

clients = []

def handle(client):
    if len(clients) > 1:
        print("2 players are connected")
        # send("start")
        clients[0].send(str.encode("X:O"))
        clients[1].send(str.encode("O:X"))
    while True:
        try:
            data = client.recv(2048).decode("utf-8")
            print("data = ", data)
            if not data:
                break
            else:
                if client == clients[0]:
                    print("player2")
                    clients[1].send(str.encode(data))
                else:
                    print("player1")
                    clients[0].send(str.encode(data))

        except:
            print("Something went wrong")

    print("Lost connection")
    index = clients.index(client)
    clients.remove(client)
    client.close()

def receive():
    while True:
        if len(clients) < 3:
            client, address = s.accept()
            print("connected")
            clients.append(client)
            thread = threading.Thread(target = handle, args = (client,))
            thread.start()

receive()