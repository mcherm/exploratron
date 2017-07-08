
import json
import copy

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

class KeyPressedMessage(Message):
    """A message sent when a client wants a server to know a key has been pressed."""
    def __init__(self, keyCode):
        self.keyCode = keyCode

class ClientShouldExitMessage(Message):
    """A message sent when the server is telling the client to quit playing."""


messages = [JoinServerMessage, WelcomeClientMessage, NewRoomMessage, RefreshRoomMessage,
            KeyPressedMessage, ClientShouldExitMessage]

_messageClass = {msg.messageName(): msg for msg in messages}


def bytesToMessage(byteString):
    jsonMessage = json.loads(byteString.decode('utf-8'))
    messageType = jsonMessage["message"]
    return _messageClass[messageType](**jsonMessage["data"])



##sampleBytes = b'{"message":"NewRoom","data":{"width":4,"height":3,"imageIds":[[2,2,2,2],[2,3,3,2],[2,3,24,2],[2,2,5,2]]}}'
##
##msg1 = NewRoomMessage( 4, 5, [[7,7,7,7],[7,0,0,7],[7,0,[0,12],7],[7,0,0,7],[7,7,8,7]] )
##msg2 = KeyPressedMessage( keyCode=115 )
##print(sampleBytes)
##print(msg1.toBytes())

