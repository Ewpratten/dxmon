from Client import Client
from Parser import Parser

# Connect to the server
client = Client()
client.connect()

# Create the parser
parser = Parser()

# Catch CTRL+C
try:
    while True:
        
        spot = parser.parse(client.getMSG())

        if not spot:
            continue

        print(spot)
except (e):
    print(e)
    print("SigTERM detected. Closing connection")
    client.disconnect()