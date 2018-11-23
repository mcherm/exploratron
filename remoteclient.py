#
# This is a client that connects to a certain character.
#

import pygame
from exploranetworking import *
from events import pygameKeyToKeyCode, KeyCode
import select
import images
from display import PygameDisplay


class MockThing:
    def __init__(self, tileId):
        self.tileId = tileId

class MockCell:
    def __init__(self, tileData):
        if isinstance(tileData, int):
            self.things = [MockThing(tileData)]
        elif isinstance(tileData, list):
            self.things = [MockThing(tileId) for tileId in tileData]
        else:
            raise Exception("tileData must be an int or a list of ints.")

class MockRoom:
    def __init__(self, message):
        assert isinstance(message, (WelcomeClientMessage, NewRoomMessage))
        self.width = message.width
        self.height = message.height
        self.grid = [ [MockCell(tileData) for tileData in row] for row in message.grid]
    def refreshRoom(self, message):
        assert isinstance(message, RefreshRoomMessage)
        self.grid =  [ [MockCell(tileData) for tileData in row] for row in message.grid]
    def updateRoom(self, message):
        assert isinstance(message, UpdateRoomMessage)
        for x, y, tileData in message.cells:
            self.grid[y][x] = MockCell(tileData)
    def cellAt(self, x, y):
        return self.grid[y][x]


#------ TEST CODE ------
def test():
    msg1 = NewRoomMessage( 4, 5, [[7,7,7,7],[7,0,0,7],[7,0,[0,12],7],[7,0,0,7],[7,7,8,7]] )
    mockRoom = MockRoom(msg1)
    imageLibrary = images.ImageLibrary()
    display = PygameDisplay()
    display.show(mockRoom, imageLibrary)
#-----------------------
    
SERVER_ADDRESS = ("127.0.0.1", 12000)
PLAYER_ID = "0"

class RemoteClient():
    def __init__(self, playerId):
        print(f'Test Client')
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.settimeout(1)

        self.clientSocket.sendto(JoinServerMessage(playerId).toBytes(), SERVER_ADDRESS)
    def mainLoop(self):
        currentRoom = None
        display = None
        imageLibrary = None
        shouldExit = False
        while not shouldExit:
            # --- Look for local events ---
            if display is not None:
                for pygameEvent in display.getEvents():
                    if pygameEvent.type == pygame.QUIT:
                        shouldExit = True
                    elif pygameEvent.type == pygame.KEYDOWN:
                        keyCode = pygameKeyToKeyCode.get(pygameEvent.key)
                        if keyCode is not None:
                            if keyCode == KeyCode.MOVE_UI_UP:
                                display.uiState.moveUINorth()
                            elif keyCode == KeyCode.MOVE_UI_DOWN:
                                display.uiState.moveUISouth()
                            elif keyCode == KeyCode.MOVE_UI_LEFT:
                                display.uiState.moveUIWest()
                            elif keyCode == KeyCode.MOVE_UI_RIGHT:
                                display.uiState.moveUIEast()
                            elif keyCode == KeyCode.TOGGLE_INVENTORY:
                                display.uiState.toggleInventory()
                            else:
                                message = KeyPressedMessage(keyCode)
                                self.clientSocket.sendto(message.toBytes(), SERVER_ADDRESS)
                    else:
                        raise Exception(f"pygame event type {pygameEvent.type} not supported")

            # --- Read from socket ---
            readyToReadSockets, (), () = select.select([self.clientSocket], [], [], 0)
            if readyToReadSockets:
                byteStr, address = readyToReadSockets[0].recvfrom(UDP_MAX_SIZE)
                message = bytesToMessage(byteStr)
                if isinstance(message, WelcomeClientMessage):
                    print(f"Server sent WelcomeClientMessage.")
                    currentRoom = MockRoom(message)
                    if display is None:
                        display = PygameDisplay()
                        defaultRegion = images.Region()
                        imageLibrary = defaultRegion.imageLibrary
                        soundLibrary = defaultRegion.soundLibrary
                    display.uiState.newRoom(currentRoom)
                elif isinstance(message, NewRoomMessage):
                    print(f"Server sent NewRoomMessage.")
                    currentRoom = MockRoom(message)
                    display.uiState.newRoom(currentRoom)
                elif isinstance(message, RefreshRoomMessage):
                    print(f"Server sent RefreshRoomMessage.")
                    currentRoom.refreshRoom(message)
                elif isinstance(message, UpdateRoomMessage):
                    print(f"Server sent UpdateRoomMessage.")
                    currentRoom.updateRoom(message)
                elif isinstance(message, PlaySoundsMessage):
                    print(f"Server sent PlaySoundsMessage.")
                    display.playSounds(message.soundIds, soundLibrary)
                elif isinstance(message, ClientShouldExitMessage):
                    print(f"Server sent ClientShouldExitMessage: {message}.")
                    shouldExit = True
                else:
                    raise Exception(f"Message type {message} not supported.")
                
            # --- Display ---
            if currentRoom is not None:
                display.show(currentRoom, imageLibrary)

    def exit(self):
        """This should be called after the main loop exits. It will inform the server
        that we are exiting. Use a try-finally to try very hard to make sure it is
        called.""" # FIXME: Make it compatible with the new 'with' statement
        self.clientSocket.sendto(ClientDisconnectingMessage().toBytes(), SERVER_ADDRESS)
        

def testDisplay():
    msg = NewRoomMessage( 4, 5, [[7,7,7,7],[7,0,0,7],[7,0,[0,12],7],[7,0,0,7],[7,7,8,7]] )
    room = MockRoom(msg)
    
    display = PygameDisplay()
    imageLibrary = images.ImageLibrary()
    display.show(room, imageLibrary)
    timeToQuit = False
    while not timeToQuit:
        events = display.getEvents()
        for event in events:
            if event.type == pygame.QUIT:
                timeToQuit = True
    display.quit()
    

if __name__ == '__main__':
    remoteClient = RemoteClient(PLAYER_ID)
    try:
        remoteClient.mainLoop()
    finally:
        remoteClient.exit()

