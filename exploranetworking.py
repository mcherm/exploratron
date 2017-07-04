
import json

# Max number of bytes WE choose to allow in a UDP packet.
UDP_MAX_SIZE = 4096

class Message:
    def __init__(self, messageName):
        self.messageName = messageName
    def dataJSON(self):
        return {}
    def toJSON(self):
        return {"message": self.messageName, "data": self.dataJSON()}
    def __repr__(self):
        return f"Message<{str(self)}>"
    def __str__(self):
        return str(self.toJSON())
    def toBytes(self):
        return json.dumps(self.toJSON(), separators=(',',':')).encode('utf-8')

        
class JoinServerMessage(Message):
    """A message sent when a client wants to sign on to a server."""
    def __init__(self):
        super().__init__("JoinServer")

class WelcomeClientMessage(Message):
    """A message the servers sends to a client immediately after they join."""
    def __init__(self):
        super().__init__("WelcomeClient")

class NewRoomMessage(Message):
    """A message sent when a server wants a client to display a new room."""
    def __init__(self, width, height, grid):
        """Constructor. grid should be a 2-D array (list of lists) of 'cells', where
        a cell is EITHER a number (representing the single tileId in that location)
        OR a list of numbers (representing the stack of tiles in that location)."""
        super().__init__("NewRoom")
        self.width = width
        self.height = height
        self.grid = grid
    def dataJSON(self):
        return {
            "width": self.width,
            "height": self.height,
            "grid": self.grid
        }


class KeyPressedMessage(Message):
    """A message sent when a client wants a server to know a key has been pressed."""
    def __init__(self, keyCode):
        super().__init__("KeyPressed")
        self.keyCode = keyCode
    def dataJSON(self):
        return {
            "keyCode": self.keyCode
        }

class ClientShouldExitMessage(Message):
    """A message sent when the server is telling the client to quit playing."""
    def __init__(self):
        super().__init__("ClientShouldExit")


_messageClass = {
    "JoinServer": JoinServerMessage,
    "WelcomeClient": WelcomeClientMessage,
    "NewRoom": NewRoomMessage,
    "KeyPressed": KeyPressedMessage,
    "ClientShouldExit": ClientShouldExitMessage,
}

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

