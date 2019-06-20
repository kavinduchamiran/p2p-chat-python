import socket
import threading
import sys
import time
from random import randint
import ctypes

# Both the classes are implemented in the same file so the first one to run main.py will
# become the server and the others will automatically be client(s)

# When a server crashes, immediately one of the clients will become the server and other
# clients will connect to that new server

class Server:
    connections = []    # keep the connections
    peers = []          # keep the peer ips

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(('0.0.0.0', 10000))     # binding to local network card, port 10000
        sock.listen(1)

        print("Server running")

        c, a = None, None

        while not c and not a:
            print('Waiting for Bob to connect')
            # there are 2 main methods on Server class
            # handler() to listen to clients' messages
            # sendMsg() to listen to own messages

            # main thread will be listning to client connection requests
            c, a = sock.accept()

        print('Bob connected')
        self.handler(c, a)

    def handler(self, c, a):
        alice = ctypes.cdll.LoadLibrary('./ObliviousTransfer/ot.so')

        # overwrite default return type to char
        alice.GetPublicParams.restype = ctypes.c_char_p
        alice.GetBlinedKey.restype = ctypes.c_char_p
        alice.GetSharedTuple.restype = ctypes.c_char_p
        alice.GetBValue.restype = ctypes.c_char_p
        alice.GetEValue.restype = ctypes.c_char_p
        alice.GetAValue.restype = ctypes.c_char_p
        alice.GetBlinedR.restype = ctypes.c_char_p

        # Initiate the protocol
        alice.InitOT(0)

        # get the security parameter
        securityParam = alice.GetSecurityParam()

        # Get the security params from initiater(Alice)
        p = alice.GetPublicParams(0)
        g0 = alice.GetPublicParams(1)
        g1 = alice.GetPublicParams(2)
        g2 = alice.GetPublicParams(3)

        # Send & set the security params to Bob (p,g0,g1,g2 - only server to client)
        self.sendMsg(c, p)
        self.sendMsg(c, g0)
        self.sendMsg(c, g1)
        self.sendMsg(c, g2)











    def sendMsg(self, connection, msg=None):
        # encode user input to utf-8, convert it to a bitstream and send over the network
        if connection and msg:
            connection.send(bytes(msg, 'utf-8'))

    def receive(self, c, a):
        while True:
            # listen to clients' data streams

            data = c.recv(1024)
            sender = bytes(str(a[0]) + ':' + str(a[1]) + " says: ", "utf-8")

            if not data:
                # when there is no data, that means client has been disconnected
                # print(str(a[0]) + ":" + str(a[1]), "disconnected")
                # c.close()
                break

        return str(data, 'utf-8')

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
        p2p.status = 'client'

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

    def sendMsg(self, sock, msg=None):
        while True and msg:
            sock.send(bytes(msg, 'utf-8'))

    def updatePeers(self, peerData):
        p2p.peers = str(peerData, "utf-8").split(",")

class p2p:
     # this list holds all the peers connected to the server.
     # set this to other node's ip address
     peers = ['127.0.0.1']
     status = ''


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







