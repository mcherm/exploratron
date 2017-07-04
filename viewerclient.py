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
    def __init__(self, newRoomMessage):
        assert isinstance(newRoomMessage, NewRoomMessage)
        self.width = newRoomMessage.width
        self.height = newRoomMessage.height
        self.grid = [ [MockCell(tileData) for tileData in row] for row in newRoomMessage.grid]
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
    

class ViewerClient():
    def __init__(self):
        print(f'Test Client')
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.settimeout(1)
        serverAddr = ("127.0.0.1", 12000)

        byteStr = JoinServerMessage().toBytes()
        if len(byteStr) > UDP_MAX_SIZE:
            raise Exception("Message too long for our UDP buffers.")
        self.clientSocket.sendto(byteStr, serverAddr)
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
                    print(f"Server sent WelcomeClientMessage: {message}.")
                elif isinstance(message, NewRoomMessage):
                    print(f"Server sent NewRoomMessage: {message}.")
                    currentRoom = MockRoom(message)
                elif isinstance(message, ClientShouldExitMessage):
                    print(f"Server sent ClientShouldExitMessage: {message}.")
                    shouldExit = True
                else:
                    raise Exception(f"Message type {message} not supported.")
            # --- Display ---
            if currentRoom is not None:
                if display is None:
                    display = images.PygameGridDisplay()
                    imageLibrary = images.ImageLibrary()
                display.show(currentRoom, imageLibrary)
            if display is not None:
                events = display.getEvents()
                for event in events:
                    if event.type == pygame.QUIT:
                        shouldExit = True

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
    viewerClient.mainLoop()

