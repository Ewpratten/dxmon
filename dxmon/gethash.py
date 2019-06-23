import socket
import hashlib
import sys

# RBN client


class Client:
    server: str = "telnet.reversebeacon.net"
    port: int = 7000

    def connect(self, call: str):
        # Open socket and connect
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.server, self.port))

        # Idle loop while waiting for data
        while not self.__sock.recv(128):
            continue
        # print("Authenticating")

        # Send auth message
        self.__sock.send(f"{call}\n\r\n\r".encode())

    def getMSG(self) -> bytes:
        # Read 128 bytes
        data = self.__sock.recv(256)

        return data

    def disconnect(self):
        self.__sock.close()

# Container for a spot


class Spot:
    spotter: str
    callsign: str
    frequency: float
    mode: str
    decibels: int
    speed: int
    message: str
    time: int

    def __str__(self) -> str:
        return "{:7s} hears {:9s} [{:10s}] on {:10.1f}Hz using {:6s} {:3.0f}WPM and {:5s} UTC :: {}".format(self.spotter, self.callsign, self.message, self.frequency, self.mode + ",", self.decibels, self.time, self.toHash())

    def toEncode(self) -> str:
        return f"{self.spotter}{self.callsign}{self.message}{int(self.frequency * 10)}{self.mode}{self.decibels}{self.time.replace(':', '')}"

    def toHash(self, type: int) -> str:
        content: str = self.toEncode().encode()

        if type == 1:
            return hashlib.sha1(content).hexdigest()
        if type == 256:
            return hashlib.sha256(content).hexdigest()
        if type == 512:
            return hashlib.sha512(content).hexdigest()

    def toDict(self) -> dict:
        return {
            "spotter": self.spotter,
            "callsign": self.callsign,
            "frequency": self.frequency,
            "mode": self.mode,
            "decibels": self.decibels,
            "speed": self.speed,
            "message": self.message,
            "time": self.time
        }

# Spot parser


class Parser:

    def parse(self, data: bytes) -> Spot:

        data = " ".join(data.decode().strip().split()).split(" ")

        # check for bad data or useless headers
        if not data or data[0] == "Local":
            return None

        if not len(data) == 12:
            return None

        # Create a new Spot to return
        output = Spot()

        # Parse message
        output.callsign = data[2][:-3]
        output.frequency = float(int(data[3].replace(".", "")) / 10)
        output.spotter = data[4].split("/")[0]
        output.mode = data[5]
        output.decibels = int(data[6])
        output.speed = int(data[8])
        output.message = data[10]
        output.time = data[11][:-3] + ":" + data[11][-3:-1]

        return output


# Do args stuff
if not len(sys.argv) == 3:
    print("Usage: rfhash <callsign> <hash type (1, 256, or 512)>")
    exit(1)

callsign: str = sys.argv[1]
hashtype: int = int(sys.argv[2])

# Connect to the server
client: Client = Client()
client.connect(callsign)

# Create the parser
parser: Parser = Parser()

while True:
    spot: Spot = parser.parse(client.getMSG())

    if not spot:
        continue

    print(spot.toHash(hashtype))
    break
client.disconnect()
