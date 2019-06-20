from chat import p2p, Client, Server
import time
import sys
from random import randint

# while True:
#     try:
#         print("Trying to connect...")
#
#         # to avoid race conditions on who becomes the server
#         time.sleep(randint(1, 5))
#
#         for peer in p2p.peers:
#             try:
#                 client = Client(peer)
#             except KeyboardInterrupt:
#                 sys.exit(0)
#             except:
#                 pass
#
#             try:
#                 server = Server()
#             except KeyboardInterrupt:
#                 sys.exit(0)
#             except:
#                 print("Couldnt start the server")
#
#     except KeyboardInterrupt:
#         sys.exit(0)

for peer in p2p.peers:
    print(22223333)
    try:
        client = Client(peer)
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        pass

    print(55555)

    try:
        server = Server()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print("Couldnt start the server")

    print(66666)

print(111111)