
import json
import copy
import select
from socket import socket, AF_INET, SOCK_DGRAM
from collections import defaultdict
from clientdata import GridData, GridDataChange, VisibleData, InventoryData


# Max number of bytes WE choose to allow in a UDP packet.
UDP_MAX_SIZE = 4096


class Message:
    """An abstract parent for all of the message types."""
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

class UpdateVisibleDataMessage(Message):
    """A message sent by the server to update the properties of the currently-displayed
    player."""
    def __init__(self, visibleData):
        assert isinstance(visibleData, VisibleData)
        self.visibleData = visibleData
    def dataJSON(self):
        return self.visibleData.toJSON()
    @classmethod
    def fromDataJSON(cls, dataJSON):
        return cls(visibleData=VisibleData.fromJSON(dataJSON))

class KeyPressedMessage(Message):
    """A message sent when a client wants a server to know a key has been pressed."""
    def __init__(self, keyCode):
        self.keyCode = keyCode

class RequestInventoryMessage(Message):
    """A message a client sends to request the inventory of the current player."""

class InventoryMessage(Message):
    """A message the server sends on request to provide the current inventory of a player."""
    def __init__(self, inventoryData):
        self.inventoryData = inventoryData
    def dataJSON(self):
        return self.inventoryData.toJSON()
    @classmethod
    def fromDataJSON(cls, dataJSON):
        return cls(inventoryData=InventoryData.fromJSON(dataJSON))

class DropItemMessage(Message):
    """A message the client sends to have the current player drop an item."""
    def __init__(self, itemUniqueId):
        self.itemUniqueId = itemUniqueId

class EquipMessage(Message):
    """A message the client sends to have the current player wield a weapon or wand in their inventory.
    None can be used for the uniqueId which will un-wield an item. Attempting to wield an item not
    found in the inventory or an item of the wron type will have no affect."""
    def __init__(self, equipmentTypeCode, itemUniqueId):
        self.equipmentTypeCode = equipmentTypeCode
        self.itemUniqueId = itemUniqueId

class InfoTextMessage(Message):
    """A message the server sends to the client to queue up a text message to be displayed."""
    def __init__(self, text):
        self.text = text

# FIXME: Wouldn't it be a better design if this contained a LIST of text messages?
class ConsoleTextMessage(Message):
    """A message the server sends to the client to append a new text message onto the console."""
    def __init__(self, text):
        self.text = text

class ClientShouldExitMessage(Message):
    """A message sent when the server is telling the client to quit playing."""

class ClientDisconnectingMessage(Message):
    """A message the client sends to the server when it is going to disconnect and
    no longer needs to receive updates."""


clientToServerMessages = [JoinServerMessage, KeyPressedMessage, RequestInventoryMessage, DropItemMessage,
                          EquipMessage, ClientDisconnectingMessage]
serverToClientMessages = [WelcomeClientMessage, NewRoomMessage, RefreshRoomMessage,
                          UpdateRoomMessage, PlaySoundsMessage, UpdateVisibleDataMessage, InventoryMessage,
                          InfoTextMessage, ConsoleTextMessage, ClientShouldExitMessage]

_messageClass = {msg.messageName(): msg for msg in clientToServerMessages + serverToClientMessages}


def bytesToMessage(byteString):
    jsonMessage = json.loads(byteString.decode('utf-8'))
    messageType = jsonMessage["message"]
    return _messageClass[messageType].fromDataJSON(jsonMessage["data"])


class ClientsideConnection:
    """Each client keeps one instance of this class, which has information about the
    connection."""
    def __init__(self, serverAddress, playerId):
        self.serverAddress = serverAddress
        self.playerId = playerId
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.settimeout(1)
        self.clientSocket.sendto(JoinServerMessage(playerId).toBytes(), serverAddress)
    def send(self, message):
        assert isinstance(message, Message)
        print(f"sending to {self.serverAddress}: {message}")
        self.clientSocket.sendto(message.toBytes(), self.serverAddress)
    def receiveOneMessage(self):
        """This should be called at least once per event loop. It will check to see if there
        are messages ready to read. The method will return None if no messages are ready to
        be received, if one or more messages are available to be read it will return one
        Message."""
        readyToReadSockets, (), () = select.select([self.clientSocket], [], [], 0)
        if readyToReadSockets:
            byteStr, address = readyToReadSockets[0].recvfrom(UDP_MAX_SIZE)
            print(f"Server sent: {byteStr}.")
            message = bytesToMessage(byteStr)
            return message
        else:
            return None


class ServersideClientConnection:
    """The server keeps instances of this class, each of which has information about
    a particular active client."""
    def __init__(self, serverSocket, address, joinServerMessage):
        assert isinstance(joinServerMessage, JoinServerMessage)
        self.serverSocket = serverSocket
        self.address = address
        self.playerId = joinServerMessage.playerId
        self.visibleData = None # Either None, or the last VisibleData sent to this client.
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
        self.connectionsByPlayer = defaultdict(list) # a map of "playerId" -> [ServersideClientConnection]
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
            clientConnection.send(message)
    def sendMessageToPlayer(self, playerId, message):
        """Sends a message to all connections for a given playerId."""
        for clientConnection in self.connectionsByPlayer.get(playerId):
            clientConnection.send(message)
    def numClients(self, playerId):
        """Given a playerId, returns the number of currently connected clients
        following that player."""
        return len(self.connectionsByPlayer.get(playerId))
