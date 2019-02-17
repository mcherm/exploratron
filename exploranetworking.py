
import json
import copy
import select
from socket import socket, AF_INET, SOCK_DGRAM
from collections import defaultdict


# Max number of bytes WE choose to allow in a UDP packet.
UDP_MAX_SIZE = 4096


# ===== Some type definitions that are designed to be implemented in JSON to cary data =====

class CellData:
    """In JSON, a CellData is EITHER a number (representing the single tileId in that
    location) OR a list of numbers (representing the stack of tiles in that
    location)."""
    def __init__(self, tileIds):
        """Initialize a cell from a tuple of tileIds."""
        assert isinstance(tileIds, tuple)
        self._tileIds = tileIds

    def __eq__(self, other):
        return isinstance(other, CellData) and  self._tileIds == other._tileIds

    def __hash__(self):
        return hash(self._tileIds)

    @classmethod
    def fromJSON(cls, json):
        """Initialize a cell from the corresponding JSON."""
        if isinstance(json, int):
            return cls(tileIds=(json,))
        elif isinstance(json, list):
            return cls(tileIds=tuple(json))
        else:
            raise TypeError("CellData must be an integer or list of integers.")

    def toJSON(self):
        """Return this Cell in JSON format."""
        if len(self._tileIds) == 1:
            return self._tileIds[0]
        else:
            return list(self._tileIds)

    def tileIds(self):
        """Returns an iterable of the items in this cell."""
        for x in self._tileIds:
            yield x


class GridData:
    """A GridData represents the contents of a room. In JSON, a grid is a 2-D array
    (list of lists) of (the JSON representation of) cells."""
    def __init__(self, width, height, allCells):
        """Initialize a grid from width, height, and allCells."""
        self.width = width
        self.height = height
        self._allCells = allCells

    @classmethod
    def fromJSON(cls, json):
        """Initialize a grid from the corresponding JSON."""
        allCells = [] # array of all cells, indexed by [x + (y * width)]
        assert isinstance(json, list)
        height = len(json)
        assert height > 0   # otherwise width would be undefined
        width = len(json[0])
        for row in json:
            assert isinstance(row, list)
            assert len(row) == width
            allCells.extend(CellData.fromJSON(x) for x in row)
        return cls(width, height, allCells)

    def toJSON(self):
        """Return this Grid in JSON format."""
        return [[self.cellAt(x,y).toJSON() for x in range(self.width)] for y in range(self.height)]

    def cellAt(self, x, y):
        """Returns the CellData at the specified x,y location (which must be valid for this GridData)."""
        assert 0 <= x < self.width
        assert 0 <= y <= self.height
        return self._allCells[x + self.width * y]

    def _setCellAt(self, x, y, cellData):
        """Use only by GridChanges; this makes it mutable. Update one cell, replacing the contents."""
        assert 0 <= x < self.width
        assert 0 <= y <= self.height
        self._allCells[x + self.width * y] = cellData


class GridDataChange:
    """This represents a set of changes that can be applied to an existing grid.
    In JSON, it is a list of three-element lists [x,y,cell] where x and y should
    be within the range of the grid it is to be applied to and cell is (the JSON
    representation of) a cell."""
    def __init__(self, changes):
        """Initialize a GridChange a list of (x,y,CellData) tuples."""
        self._changes = changes

    @classmethod
    def fromJSON(cls, json):
        """Initialize a GridChange from the corresponding JSON."""
        assert isinstance(json, list)
        return cls(changes=[(x, y, CellData.fromJSON(cellJSON)) for x, y, cellJSON in json])

    def toJSON(self):
        """Return this GridChange in JSON format."""
        return [[x, y, cellData.toJSON()] for x, y, cellData in self._changes]

    def changes(self):
        """Returns an iterator of (x, y, CellData) tuples."""
        return iter(self._changes)

    def applyToGrid(self, gridData):
        """When invoked, modifies the given grid by applying these changes. Will
        give an error if that doesn't work."""
        assert isinstance(gridData, GridData)
        for x, y, cellData in self.changes():
            gridData._setCellAt(x, y, cellData)


# ===== The messages themselves =====


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
    @classmethod
    def fromDataJSON(cls, dataJSON):
        return cls(**dataJSON)


        
class JoinServerMessage(Message):
    """A message sent when a client wants to sign on to a server."""
    def __init__(self, playerId):
        self.playerId = playerId

class WelcomeClientMessage(Message):
    """A message the servers sends to a client immediately after they join. It
    includes everything needed for a NewRoomMessage."""
    def __init__(self, gridData):
        """Constructor. Accepts a GridData."""
        assert isinstance(gridData, GridData)
        self.gridData = gridData
    def dataJSON(self):
        return self.gridData.toJSON()
    @classmethod
    def fromDataJSON(cls, dataJSON):
        return cls(gridData=GridData.fromJSON(dataJSON))

class NewRoomMessage(Message):
    """A message sent when a server wants a client to display a new room."""
    def __init__(self, gridData):
        """Constructor. Accepts a GridData."""
        assert isinstance(gridData, GridData)
        self.gridData = gridData
    def dataJSON(self):
        return self.gridData.toJSON()
    @classmethod
    def fromDataJSON(cls, dataJSON):
        return cls(gridData=GridData.fromJSON(dataJSON))

class RefreshRoomMessage(Message):
    """A message sent when a server wants to refresh all the tiles in the
    current room."""
    def __init__(self, gridData):
        """Constructor. Accepts a GridData."""
        assert isinstance(gridData, GridData)
        self.gridData = gridData
    def dataJSON(self):
        return self.gridData.toJSON()
    @classmethod
    def fromDataJSON(cls, dataJSON):
        return cls(gridData=GridData.fromJSON(dataJSON))


class UpdateRoomMessage(Message):
    """A message sent when a server wants to refresh just certain cells of the
    current room."""
    def __init__(self, gridDataChange):
        """Constructor. Accepts a GridDataChange."""
        assert isinstance(gridDataChange, GridDataChange)
        self.gridDataChange = gridDataChange
    def dataJSON(self):
        return self.gridDataChange.toJSON()
    @classmethod
    def fromDataJSON(cls, dataJSON):
        return cls(gridDataChange=GridDataChange.fromJSON(dataJSON))

class PlaySoundsMessage(Message):
    """A message sent by the server to instruct the client to begin playing some
    sounds."""
    def __init__(self, soundIds):
        """Constructor. soundIds is a list of sound ids."""
        self.soundIds = soundIds

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
                          UpdateRoomMessage, PlaySoundsMessage, ClientShouldExitMessage]

_messageClass = {msg.messageName(): msg for msg in clientToServerMessages + serverToClientMessages}


def bytesToMessage(byteString):
    jsonMessage = json.loads(byteString.decode('utf-8'))
    messageType = jsonMessage["message"]
    return _messageClass[messageType].fromDataJSON(jsonMessage["data"])


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
        messages ready to read. The method will return a list of (Message, clientConnection)
        pairs (0 pairs if no messages that the server needs to respond to were received).
        The Message can be any clientToServerMessage and the clientConnection is the
        connection to that client."""
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
                result.append( (message, clientConnection) )
            elif isinstance(message, ClientDisconnectingMessage):
                try:
                    clientConnection = self.connectionsByAddr.pop(address)
                    self.connectionsByPlayer.get(clientConnection.playerId).remove(clientConnection)
                    result.append( (message, clientConnection) )
                except KeyError:
                    # Strangely, some client we don't know tried to disconnect.
                    # FIXME: Should probably log this or something.
                    pass
            else:
                clientConnection = self.connectionsByAddr.get(address)
                print(f"Client {clientConnection} sent message {message}.")
                result.append( (message, clientConnection) )
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

