import hashlib

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
        return "{:7s} hears {:9s} [{:10s}] on {:10.1f}Hz using {:5s} {:3.0f}WPM and {:5s} UTC :: {}".format(self.spotter, self.callsign, self.message, self.frequency, self.mode + ",", self.decibels, self.time, self.toHash())
    
    def toEncode(self) -> str:
        return f"{self.spotter}{self.callsign}{self.message}{int(self.frequency * 10)}{self.mode}{self.decibels}{self.time.replace(':', '')}"
    
    def toHash(self) -> str:
        return hashlib.sha256(self.toEncode().encode()).hexdigest()
    
    
    def toDict(self) -> dict:
        return {
            "spotter": self.spotter,
            "callsign": self.callsign,
            "frequency": self.frequency,
            "mode": self.mode,
            "decibels": self.decibels,
            "speed": self.speed,
            "message": self.message,
            "time":self.time
        }
