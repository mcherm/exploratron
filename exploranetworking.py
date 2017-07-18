
import json
import copy
import select
from socket import *
from collections import defaultdict


# Max number of bytes WE choose to allow in a UDP packet.
UDP_MAX_SIZE = 4096

class Message:
    @classmethod
    def messageName(cls):
        className = cls.__name__
        assert className.endswith("Message")
        return className[:-7]
    def dataJSON(self):
        return copy.copy(self.__dict__)
    def toJSON(self):
        return {"message": self.messageName(), "data": self.dataJSON()}
    def __repr__(self):
        return f"Message<{str(self)}>"
    def __str__(self):
        return str(self.toJSON())
    def toBytes(self):
        byteStr = json.dumps(self.toJSON(), separators=(',',':')).encode('utf-8')
        if len(byteStr) > UDP_MAX_SIZE:
            raise Exception("Message too long for our UDP buffers.")
        return byteStr

        
class JoinServerMessage(Message):
    """A message sent when a client wants to sign on to a server."""
    def __init__(self, playerId):
        self.playerId = playerId

class WelcomeClientMessage(Message):
    """A message the servers sends to a client immediately after they join. It
    includes everything needed for a NewRoomMessage."""
    def __init__(self, width, height, grid):
        """Constructor. grid should be a 2-D array (list of lists) of 'cells', where
        a cell is EITHER a number (representing the single tileId in that location)
        OR a list of numbers (representing the stack of tiles in that location)."""
        self.width = width
        self.height = height
        self.grid = grid    

class NewRoomMessage(Message):
    """A message sent when a server wants a client to display a new room."""
    def __init__(self, width, height, grid):
        """Constructor. grid should be a 2-D array (list of lists) of 'cells', where
        a cell is EITHER a number (representing the single tileId in that location)
        OR a list of numbers (representing the stack of tiles in that location)."""
        self.width = width
        self.height = height
        self.grid = grid

class RefreshRoomMessage(Message):
    """A message sent when a server wants to refresh all the tiles in the
    current room."""
    def __init__(self, grid):
        """Constructor. grid should be a 2-D array (list of lists) of 'cells', where
        a cell is EITHER a number (representing the single tileId in that location)
        OR a list of numbers (representing the stack of tiles in that location)."""
        self.grid = grid

class UpdateRoomMessage(Message):
    """A message sent when a server wants to refresh just certain cells of the
    current room."""
    def __init__(self, cells):
        """Constructor. cells is a list of three-element lists [x,y,cell] where
        each 'cell' is either a number (representing the single tineId in that
        location) or a list of numbers (represent the stack of tiles in that location).
        Each cell provided fully replaces whatever was there before."""
        self.cells = cells

class KeyPressedMessage(Message):
    """A message sent when a client wants a server to know a key has been pressed."""
    def __init__(self, keyCode):
        self.keyCode = keyCode

class ClientShouldExitMessage(Message):
    """A message sent when the server is telling the client to quit playing."""

class ClientDisconnectingMessage(Message):
    """A message the client sends to the server when it is going to disconnect and
    no longer needs to receive updates."""


clientToServerMessages = [JoinServerMessage, KeyPressedMessage, ClientDisconnectingMessage]
serverToClientMessages = [WelcomeClientMessage, NewRoomMessage, RefreshRoomMessage,
                          UpdateRoomMessage, ClientShouldExitMessage]

_messageClass = {msg.messageName(): msg for msg in clientToServerMessages + serverToClientMessages}


def bytesToMessage(byteString):
    jsonMessage = json.loads(byteString.decode('utf-8'))
    messageType = jsonMessage["message"]
    return _messageClass[messageType](**jsonMessage["data"])


class ServersideClientConnection:
    """The server keeps instances of this class, each of which has information about
    a particular active client."""
    def __init__(self, serverSocket, address, joinServerMessage):
        assert isinstance(joinServerMessage, JoinServerMessage)
        self.serverSocket = serverSocket
        self.address = address
        self.playerId = joinServerMessage.playerId
    def send(self, message):
        assert isinstance(message, Message)
        print(f"sending to {self.address}: {message}")
        self.sendRaw(message.toBytes())
    def sendRaw(self, byteStr):
        """Like send(), but the caller converts to bytes and checks the length."""
        self.serverSocket.sendto(byteStr, self.address)
        


class ServersideClientConnections:
    """The server maintains an instance of this class, which keeps track of the clients
    that are currently connected."""
    def __init__(self):
        self.connectionsByAddr = {} # a map of address -> ServersideClientConnection
        self.connectionsByPlayer = defaultdict(list) # a map of "playerId" -> [ServersideClientConnections]
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)
        self.serverSocket.bind(('', 12000))
    def numConnections(self):
        return len(self.connectionsByAddr)
    def receiveMessages(self):
        """This should be called once per event loop. It will check to see if there are
        messages ready to read. The method will return a list of (Message, replyFunc)
        pairs (0 pairs if no messages that the server needs to respond to were received).
        The Message can be any clientToServerMessage and the replyFunc is a function
        taking a serverToClientMessage which will send it to the appropriate client."""
        result = []
        readyToReadSockets, (), () = select.select([self.serverSocket], [], [], 0)
        for socket in readyToReadSockets:
            # Read ONE message from the socket (FIXME: Should it read more if they are ready?)
            byteStr, address = socket.recvfrom(UDP_MAX_SIZE)
            message = bytesToMessage(byteStr)
            if isinstance(message, JoinServerMessage):
                clientConnection = ServersideClientConnection(self.serverSocket, address, message)
                self.connectionsByAddr[clientConnection.address] = clientConnection
                self.connectionsByPlayer[clientConnection.playerId].append(clientConnection)
                result.append( (message, clientConnection.send) )
            elif isinstance(message, ClientDisconnectingMessage):
                try:
                    clientConnection = self.connectionsByAddr.pop(address)
                    self.connectionsByPlayer.get(clientConnection.playerId).remove(clientConnection)
                except KeyError:
                    # Strangely, some client we don't know tried to disconnect. SHOULD WARN
                    pass
                result.append( (message, lambda x: None) )
            else:
                clientConnection = self.connectionsByAddr.get(address)
                print(f"Client {clientConnection} sent message {message}.")
                result.append( (message, clientConnection.send) )
        return result
    def sendMessageToAll(self, message):
        for clientConnection in self.connectionsByAddr.values():
            clientConnection.sendRaw(message.toBytes())
    def sendMessageToPlayer(self, playerId, message):
        """Sends a message to all connections for a given playerId."""
        for clientConnection in self.connectionsByPlayer.get(playerId):
            clientConnection.sendRaw(message.toBytes())
    def numClients(self, playerId):
        """Given a playerId, returns the number of currently connected clients
        following that player."""
        return len(self.connectionsByPlayer.get(playerId))
        
        
    

##sampleBytes = b'{"message":"NewRoom","data":{"width":4,"height":3,"imageIds":[[2,2,2,2],[2,3,3,2],[2,3,24,2],[2,2,5,2]]}}'
##
##msg1 = NewRoomMessage( 4, 5, [[7,7,7,7],[7,0,0,7],[7,0,[0,12],7],[7,0,0,7],[7,7,8,7]] )
##msg2 = KeyPressedMessage( keyCode=115 )
##print(sampleBytes)
##print(msg1.toBytes())

