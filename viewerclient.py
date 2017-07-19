#
# This is a client that simply views what is happening to the main
# character and never sends any input.
#

import pygame
import time
from socket import socket, AF_INET, SOCK_DGRAM
from exploranetworking import *
import select
import random
import images


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
    display = images.PygameGridDisplay()
    display.show(mockRoom, imageLibrary)
#-----------------------
    
SERVER_ADDRESS = ("127.0.0.1", 12000)
PLAYER_ID = "0"

class ViewerClient():
    def __init__(self):
        print(f'Test Client')
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.settimeout(1)

        self.clientSocket.sendto(JoinServerMessage(PLAYER_ID).toBytes(), SERVER_ADDRESS)
    def mainLoop(self):
        currentRoom = None
        display = None
        imageLibrary = None
        shouldExit = False
        while not shouldExit:
            # --- Look for local events ---

            # --- Read from socket ---
            readyToReadSockets, (), () = select.select([self.clientSocket], [], [], 0)
            if readyToReadSockets:
                byteStr, address = readyToReadSockets[0].recvfrom(UDP_MAX_SIZE)
                message = bytesToMessage(byteStr)
                if isinstance(message, WelcomeClientMessage):
                    print(f"Server sent WelcomeClientMessage.")
                    currentRoom = MockRoom(message)
                elif isinstance(message, NewRoomMessage):
                    print(f"Server sent NewRoomMessage.")
                    currentRoom = MockRoom(message)
                elif isinstance(message, RefreshRoomMessage):
                    print(f"Server sent RefreshRoomMessage.")
                    currentRoom.refreshRoom(message)
                elif isinstance(message, UpdateRoomMessage):
                    print(f"Server sent UpdateRoomMessage.")
                    currentRoom.updateRoom(message)
                elif isinstance(message, ClientShouldExitMessage):
                    print(f"Server sent ClientShouldExitMessage: {message}.")
                    shouldExit = True
                else:
                    raise Exception(f"Message type {message} not supported.")
            # --- Display ---
            if currentRoom is not None:
                if display is None:
                    display = images.PygameGridDisplay()
                    imageLibrary = images.ImageLibrary('drawntiles64')
                display.show(currentRoom, imageLibrary)
            if display is not None:
                events = display.getEvents()
                for event in events:
                    if event.type == pygame.QUIT:
                        shouldExit = True
    def exit(self):
        """This should be called after the main loop exits. It will inform the server
        that we are exiting. Use a try-finally to try very hard to make sure it is
        called.""" # FIXME: Make it compatible with the new 'with' statement
        self.clientSocket.sendto(ClientDisconnectingMessage().toBytes(), SERVER_ADDRESS)
        

def testDisplay():
    msg = NewRoomMessage( 4, 5, [[7,7,7,7],[7,0,0,7],[7,0,[0,12],7],[7,0,0,7],[7,7,8,7]] )
    room = MockRoom(msg)
    
    display = images.PygameGridDisplay()
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
    viewerClient = ViewerClient()
    try:
        viewerClient.mainLoop()
    finally:
        viewerClient.exit()



