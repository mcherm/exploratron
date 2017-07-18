
import random
from exploranetworking import *


# FIXME: Remove this
##class ClientConnection:
##    def __init__(self, serverSocket, address, joinServerMessage):
##        assert isinstance(joinServerMessage, JoinServerMessage)
##        self.serverSocket = serverSocket
##        self.address = address
##    def send(self, message):
##        assert isinstance(message, Message)
##        print(f"sending to {self.address}: {message}")
##        self.sendRaw(message.toBytes())
##    def sendRaw(self, byteStr):
##        """Like send(), but the caller converts to bytes and checks the length."""
##        self.serverSocket.sendto(byteStr, self.address)
        
        

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

    clients = ServersideClientConnections()

    while True:
        for message, replyFunc in clients.receiveMessages():
            if isinstance(message, JoinServerMessage):
                print(f"Got JoinServerMessage to join client {message.playerId}.")
                print(f"WelcomeClientMessage to just 1 client")
                replyFunc( WelcomeClientMessage( 4, 5, makeRandomGrid() ) )
            elif isinstance(message, KeyPressedMessage):
                pass
            elif isinstance(message, ClientDisconnectingMessage):
                pass
            else:
                raise Exception(f"Message type not supported for message {message}.")
            
        if random.randrange(2000000) < 1:
            print(f"New Room to {clients.numConnections()} clients")
            lastLocation = (2,2)
            msg = NewRoomMessage( 4, 5, makeRandomGrid() )
            clients.sendMessageToAll(msg)
        if random.randrange(1000000) < 1:
            print(f"Refresh Room to {clients.numConnections()} clients")
            lastLocation = (2,2)
            msg = RefreshRoomMessage( makeRandomGrid() )
            clients.sendMessageToAll(msg)
        if random.randrange(100000) < 1:
            print(f"Update Room to {clients.numConnections()} clients")
            msg = UpdateRoomMessage( makeRandomUpdate() )
            clients.sendMessageToAll(msg)
            


messageServer()

