import socket

class Client:
    server: str = "telnet.reversebeacon.net"
    port: int = 7000
    
    def connect(self):
        # Open socket and connect
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.server, self.port))

        # Idle loop while waiting for data
        while not self.__sock.recv(128):
            continue
        # print("Authenticating")
            
        # Send auth message
        self.__sock.send("dxm0n\n\r\n\r".encode())
    
    def getMSG(self) -> bytes:
        # Read 128 bytes
        data = self.__sock.recv(256)

        return data
    
    def disconnect(self):
        self.__sock.close()