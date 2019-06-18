import socket
import threading
import sys
import time
from random import randint

class Server:
    connections = []
    peers = []

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(('0.0.0.0', 10000))
        sock.listen(1)

        print("Server running")

        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()

            self.connections.append(c)
            self.peers.append(a[0])

            print(str(a[0]) + ':' + str(a[1]), "connected")
            self.sendPeers()

            iThread = threading.Thread(target=self.sendMsg, args=(c,))
            iThread.daemon = True
            iThread.start()

    def sendMsg(self, connection):
        while True:
            connection.send(bytes(input(""), 'utf-8'))

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            sender = bytes(str(a[0]) + ':' + str(a[1]) + " says: ", "utf-8")

            print(data)

            for connection in self.connections:
                if connection != c:
                    connection.send(sender + data)

            if not data:
                print(str(a[0]) + ":" + str(a[1]), "disconnected")
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break

    def sendPeers(self):
        p = ",".join(self.peers)

        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, "utf-8"))


class Client:
    def __init__(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.connect((address, 10000))
        print("Connected to server")

        iThread = threading.Thread(target=self.sendMsg, args=(sock,))
        iThread.daemon = True
        iThread.start()

        while True:
            data = sock.recv(1024)
            if not data:
                break

            if data[0:1] == b'\x11':
                self.updatePeers(data[1:])
            else:
                print(str(data, 'utf-8'))

    def sendMsg(self, sock):
        while True:
            sock.send(bytes(input(), 'utf-8'))

    def updatePeers(self, peerData):
        p2p.peers = str(peerData, "utf-8").split(",")

class p2p:
     # this list holds all the peers connected to the server.
     # initialized to 127.0.0.1 so the first node will start as a server
     peers = ['192.248.9.138']


while True:
    try:
        print("Trying to connect...")

        time.sleep(randint(1, 5))

        for peer in p2p.peers:
            try:
                client = Client(peer)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass

            try:
                server = Server()
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print("Couldnt start the server")

    except KeyboardInterrupt:
        sys.exit(0)







