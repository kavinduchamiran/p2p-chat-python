import socket
import threading
import sys
import time
from random import randint

# Both the classes are implemented in the same file so the first one to run main.py will
# become the server and the others will automatically be client(s)

# When a server crashes, immediately one of the clients will become the server and other
# clients will connect to that new server automatically

class Server:
    connections = []    # keep the connections
    peers = []          # keep the peer ips

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(('0.0.0.0', 10000))     # binding to local network card, port 10000
        sock.listen(1)

        print("Server running")

        while True:
            # there are 2 main methods on Server class
            # handler() to listen to clients' messages
            # sendMsg() to listen to own messages

            # main thread will be listning to client connection requests
            c, a = sock.accept()

            # cThread will be running handler()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()

            self.connections.append(c)
            self.peers.append(a[0])

            print(str(a[0]) + ':' + str(a[1]), "connected")
            self.sendPeers()

            # iThread will be running sendMsg()
            iThread = threading.Thread(target=self.sendMsg, args=(c,))
            iThread.daemon = True
            iThread.start()

    def sendMsg(self, connection):
        # encode user input to utf-8, convert it to a bitstream and send over the network
        while True:
            connection.send(bytes(input(""), 'utf-8'))

    def handler(self, c, a):
        while True:
            # listen to clients' data streams

            data = c.recv(1024)
            sender = bytes(str(a[0]) + ':' + str(a[1]) + " says: ", "utf-8")

            print(str(a[0]) + ':' + str(a[1]) + " says: ", str(data, 'utf-8'))

            for connection in self.connections:
                # iterate through all active sessions
                if connection != c:
                    # no need to send to the same client who sent the message
                    connection.send(sender + data)

            if not data:
                # when there is no data, that means client has been disconnected
                print(str(a[0]) + ":" + str(a[1]), "disconnected")
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break

    def sendPeers(self):
        # update the peer list in every client so they know who their neighbours are
        p = ",".join(self.peers)

        for connection in self.connections:
            # add a special \x11 to distinguish normal messages vs. peer list
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
     # set this to other node's ip address
     peers = ['192.168.43.147']


while True:
    try:
        print("Trying to connect...")

        # to avoid race conditions on who becomes the server
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







