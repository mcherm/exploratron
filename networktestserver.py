
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
        byteStr = message.toBytes()
        if len(byteStr) > UDP_MAX_SIZE:
            raise Exception("Message too long for our UDP buffers.")
        self.sendRaw(byteStr)
    def sendRaw(self, byteStr):
        """Like send(), but the caller converts to bytes and checks the length."""
        self.serverSocket.sendto(byteStr, self.address)
        
        



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
                print(f"Client sent JoinServerMessage: {message}.")
                clientConnection = ClientConnection(serverSocket, address, message)
                clientConnections[address] = clientConnection
                clientConnection.send(WelcomeClientMessage())
            elif isinstance(message, KeyPressedMessage):
                clientConnection = clientConnections.get(address)
                print(f"Client {clientConnection} sent key press {message.keyCode}.")
            else:
                raise Exception(f"Message type {message} not supported.")
        if random.randrange(100000) < 1:
            print("New Display Change")
            msg = NewRoomMessage( 4, 3, [[2,2,2,2],[2,3,3,2],[2,3,24,2],[2,2,5,2]] )
            byteStr = msg.toBytes()
            if len(byteStr) > UDP_MAX_SIZE:
                raise Exception("Message too long for our UDP buffers.")
            for clientConnection in clientConnections.values():
                clientConnection.sendRaw(byteStr)
        


messageServer()

