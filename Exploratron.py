#
# This contains the game currently known as "Exploratron". 
#

import pygame
import kindsofthing
from kindsofthing import *
from objects import *
from images import ImageLibrary, TILE_SIZE, PygameGridDisplay
from events import *
import rooms
import time


# ========= Start Classes for Game =========

    


class World:
    """Represents the entire world."""
    def __init__(self):
        self.gameOver = False
        self.rooms = rooms.rooms
        self.mobiles = []
        self.players = []
        # set up player
        self.player = Player(tileId=11, hitPoints=9, playerId="0")
        self.players.append(self.player)
        playerRoom = self.rooms[1]
        self.player.setLocation( playerRoom, (2,1) )
        playerRoom.cellAt(2,1).addThing(self.player)
    def addMobiles(self, newMobiles):
        """Call this to add some new mobiles to the list of active
        mobiles."""
        self.mobiles.extend(newMobiles)

        
##class PlayerInputs:
##    """Maintains a list of events. The events are designed to be EITHER
##    created by PyGame (for local events) OR created ourselves (for
##    remote connections). The object will be assumed to have a "type"
##    property which will be a PyGame event type or else something we
##    define (our types will be numbers above 1000)."""
##    def __init__(self, events):
##        self.events = events

        
# ========= End Classes for Game =========



# ========= Start Functions for Game =========


def moveMobiles(world, currentTime):
    """This function will cause all of the mobiles to move one step,
    updating the world accordingly."""
    for mobile in world.mobiles:
        if currentTime >= mobile.whenItCanAct:
            mobile.takeOneStep(currentTime)
    




def updateWorld(world, eventList):
    currentTime = int(time.perf_counter()*1000)
    # Non-Action Events
    for event in eventList.nonActionEvents:
        if isinstance(event, QuitGameEvent):
            world.gameOver = True
    # Action Events
    for player in world.players:
        if currentTime < player.whenItCanAct:
            # Player cannot act yet
            if player.queuedEvent is None:
                # Player does not have an event queued
                for event in eventList.actionEvents:
                    player.queuedEvent = event
                    break
        else:
            # Player can act now
            eventToActOn = player.queuedEvent
            # We used the value, so clear it
            player.queuedEvent = None
            if eventToActOn is None:
                # Set eventToActOn to the FIRST action event
                for event in eventList.actionEvents:
                    eventToActOn = event
                    break
            # Now we have set eventToActOn
            if eventToActOn is not None:
                if isinstance(eventToActOn, KeyPressedEvent):
                    if eventToActOn.keyCode == pygame.K_s:
                        player.moveSouth()
                        player.whenItCanAct = currentTime + 500
                    if eventToActOn.keyCode == pygame.K_w:
                        player.moveNorth()
                        player.whenItCanAct = currentTime + 500
                    if eventToActOn.keyCode == pygame.K_d:
                        player.moveEast()
                        player.whenItCanAct = currentTime + 500
                    if eventToActOn.keyCode == pygame.K_a:
                        player.moveWest()
                        player.whenItCanAct = currentTime + 500
    # Move Mobiles
    moveMobiles(world, currentTime)
    # Check for Death
    handleDeath(world)
            

def handleDeath(world):
    for mobile in world.mobiles:
        if mobile.isDead:
            x, y = mobile.position
            cell = mobile.room.cellAt(x, y)
            cell.removeThing(mobile)
            world.mobiles.remove(mobile)
    if world.player.isDead:
        x, y = world.player.position
        cell = world.player.room.cellAt(x, y)
        cell.removeThing(world.player)
        world.gameOver = True

# FIXME: Add this soon
##def processClientMessages(clients):
##    """This function gets any messages waiting on the queue from clients
##    and returns XXXXXXXXX"""
##    for message, replyFunc in clients.receiveMessages():
##        if isinstance(message, JoinServerMessage):
##            print(f"Got JoinServerMessage to join client {message.playerId}.")
##            print(f"WelcomeClientMessage to just 1 client")
##            replyFunc( WelcomeClientMessage( 4, 5, makeRandomGrid() ) )
##        elif isinstance(message, KeyPressedMessage):
##            pass
##        elif isinstance(message, ClientDisconnectingMessage):
##            pass
##        else:
##            raise Exception(f"Message type not supported for message {message}.")
    


def renderWorld(player, display, imageLibrary):
    display.show(player.room, imageLibrary)



def mainLoop(world):
    eventList = EventList()
    display = PygameGridDisplay()
    imageLibrary = ImageLibrary()
# FIXME: Add this soon
#    clients = ServersideClientConnections()
    player = world.player
    while not world.gameOver:
        renderWorld(player, display, imageLibrary)
        eventList.clear()
        eventList.addPygameEvents(display.getEvents(), world.player.playerId)
        # FIXME: Add this soon
        #clientInputs = processClientMessages(clients)
        updateWorld(world, eventList)
    display.quit()



# ========= End Functions for Game =========

kindsofthing.world = World()
mainLoop(kindsofthing.world)
