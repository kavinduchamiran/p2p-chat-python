from flask import Flask
import sys
app = Flask(__name__)

from chat import Client, Server, p2p

print("Trying to connect...")

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


@app.route("/")
def hello():
    return