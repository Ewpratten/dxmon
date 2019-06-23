from Spot import Spot

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

