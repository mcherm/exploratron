
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
        self.sendRaw(message.toBytes())
    def sendRaw(self, byteStr):
        """Like send(), but the caller converts to bytes and checks the length."""
        self.serverSocket.sendto(byteStr, self.address)
        
        

lastLocation = (2,2)

def makeRandomGrid():
    grid1 = [[7,7,7,7],[7,0,0,7],[7,0,[0,12],7],[7,0,0,7],[7,7,8,7]]
    grid2 = [[7,8,7,7],[7,0,0,7],[7,0,[0,12],7],[7,0,0,7],[7,7,7,7]]
    return random.choice([grid1, grid2])

def makeRandomUpdate():
    global lastLocation
    locations = [(1,1), (2,1), (1,2), (2,2)]
    newLocation = lastLocation
    while newLocation == lastLocation:
        newLocation = random.choice(locations)
    result = [
        [lastLocation[0], lastLocation[1], 0],
        [newLocation[0], newLocation[1], [0,12]],
    ]
    lastLocation = newLocation
    return result


def messageServer():
    print(f'Test Server')
    global lastLocation
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
                print(f"WelcomeClientMessage to just 1 client")
                clientConnection.send(WelcomeClientMessage( 4, 5, makeRandomGrid() ))
            elif isinstance(message, KeyPressedMessage):
                clientConnection = clientConnections.get(address)
                print(f"Client {clientConnection} sent key press {message.keyCode}.")
            elif isinstance(message, ClientDisconnectingMessage):
                clientConnections.pop(address) # Remove this client from the list we send to
            else:
                raise Exception(f"Message type not supported for message {message}.")
        if random.randrange(2000000) < 1:
            print(f"New Room to {len(clientConnections)} clients")
            lastLocation = (2,2)
            msg = NewRoomMessage( 4, 5, makeRandomGrid() )
            for clientConnection in clientConnections.values():
                clientConnection.sendRaw(msg.toBytes())
        if random.randrange(1000000) < 1:
            print(f"Refresh Room to {len(clientConnections)} clients")
            lastLocation = (2,2)
            msg = RefreshRoomMessage( makeRandomGrid() )
            for clientConnection in clientConnections.values():
                clientConnection.sendRaw(msg.toBytes())
        if random.randrange(100000) < 1:
            print(f"Update Room to {len(clientConnections)} clients")
            msg = UpdateRoomMessage( makeRandomUpdate() )
            for clientConnection in clientConnections.values():
                clientConnection.sendRaw(msg.toBytes())
            
            
        


messageServer()

