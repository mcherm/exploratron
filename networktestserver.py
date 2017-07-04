
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
                print(f"Client sent JoinServerMessage: {message}.")
                clientConnection = ClientConnection(serverSocket, address, message)
                clientConnections[address] = clientConnection
                clientConnection.send(WelcomeClientMessage())
            elif isinstance(message, KeyPressedMessage):
                clientConnection = clientConnections.get(address)
                print(f"Client {clientConnection} sent key press {message.keyCode}.")
            else:
                raise Exception(f"Message type {message} not supported.")
        


messageServer()

