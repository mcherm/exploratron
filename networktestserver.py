
import random
from socket import *
import select
from exploranetworking import *



class ClientConnection:
    def __init__(self, serverSocket, address, joinServerMessage):
        assert isinstance(joinServerMessage, JoinServerMessage)
        self.serverSocket = serverSocket
        self.address = address
    def send(self, message):
        assert isinstance(message, Message)
        print(f"sending to {self.address}: {message}")
        self.serverSocket.sendto(message.toBytes(), self.address)
        



def messageServer():
    print(f'Test Server')
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', 12000))

    # map of address -> ClientConnection
    clientConnections = {}

    while True:
        readyToReadSockets, (), () = select.select([serverSocket], [], [], 0)
        if readyToReadSockets:
            byteStr, address = readyToReadSockets[0].recvfrom(UDP_MAX_SIZE)
            message = bytesToMessage(byteStr)
            if isinstance(message, JoinServerMessage):
                clientConnection = ClientConnection(serverSocket, address, message)
                clientConnections[address] = clientConnection
                clientConnection.send(WelcomeClientMessage())
            else:
                raise Exception(f"Message type {message} not supported.")
        


messageServer()


"""

Some thoughts on message design.

I want a way to pass a room display. I can assign an integer (2 byte) to each image.

Oh, wait... what I should REALLY do is to make it work first, THEN make it efficient.

How about a JSON structure:


blank line is "end of item".

{
    "message": "NewRoom",
    "data": {
        "height": 3,
        "width": 4,
        "imageIds": [
            [2, 2, 2, 2],
            [2, 3, 3, 2],
            [2, 3, 24, 2],
            [2, 2, 5, 2]
        ]
    }
}
"""
