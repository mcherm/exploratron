#
# This is a client that connects to a certain character.
#

from pygame import init as pygame_init
pygame_init() # Need to run this before some of the code that runs during imports


import pygame
from exploranetworking import ClientsideConnection, KeyPressedMessage, WelcomeClientMessage, NewRoomMessage, RefreshRoomMessage, UpdateRoomMessage, PlaySoundsMessage, UpdateVisibleDataMessage, ClientShouldExitMessage, ClientDisconnectingMessage
from events import pygameKeyToKeyCode, KeyCode
import images
from display import PygameDisplay



SERVER_ADDRESS = ("127.0.0.1", 12000)
PLAYER_ID = "0"

class RemoteClient():
    def __init__(self, playerId):
        print(f'Test Client')
        self.playerId = playerId
        self.clientsideConnection = ClientsideConnection(SERVER_ADDRESS, playerId)

    def mainLoop(self):
        display = None
        imageLibrary = None
        soundLibrary = None
        currentGridData = None
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
                                self.clientsideConnection.send(message)
                    else:
                        raise Exception(f"pygame event type {pygameEvent.type} not supported")

            # --- Read a message ---
            message = self.clientsideConnection.receiveOneMessage()
            if message:
                if isinstance(message, WelcomeClientMessage):
                    currentGridData = message.gridData
                    if display is None:
                        display = PygameDisplay()
                        defaultRegion = images.Region()
                        imageLibrary = defaultRegion.imageLibrary
                        soundLibrary = defaultRegion.soundLibrary
                    display.uiState.newRoom(currentGridData)
                    display.setDisplayedPlayerId(self.playerId)
                elif isinstance(message, NewRoomMessage):
                    currentGridData = message.gridData
                    display.uiState.newRoom(currentGridData)
                elif isinstance(message, RefreshRoomMessage):
                    currentGridData = message.gridData
                elif isinstance(message, UpdateRoomMessage):
                    message.gridDataChange.applyToGrid(currentGridData)
                elif isinstance(message, PlaySoundsMessage):
                    display.playSounds(message.soundIds, soundLibrary)
                elif isinstance(message, UpdateVisibleDataMessage):
                    display.setVisibleData(message.visibleData)
                elif isinstance(message, ClientShouldExitMessage):
                    shouldExit = True
                else:
                    raise Exception(f"Server sent message type '{message}' which is not supported.")
                
            # --- Display ---
            if currentGridData is not None:
                display.show(currentGridData, imageLibrary)

    def exit(self):
        """This should be called after the main loop exits. It will inform the server
        that we are exiting. Use a try-finally to try very hard to make sure it is
        called.""" # FIXME: Make it compatible with the new 'with' statement
        self.clientsideConnection.send(ClientDisconnectingMessage())




if __name__ == '__main__':
    remoteClient = RemoteClient(PLAYER_ID)
    try:
        remoteClient.mainLoop()
    finally:
        remoteClient.exit()

