#
# This contains the game currently known as "Exploratron". 
#

import kindsofthing
from gamecomponents import Location
import objects
from players import Player, thePlayerCatalog, PlayerCatalogEntry
from images import Region, TILE_SIZE, PygameGridDisplay
from events import EventList, KeyPressedEvent, KeyCode, QuitGameEvent
from exploranetworking import *
from screenchanges import ScreenChanges, SetOfEverything
import rooms
import time
import random


# ========= Start Classes for Game =========

    


class World:
    """Represents the entire world."""
    def __init__(self):
        self.gameOver = False
        self.rooms = rooms.rooms
        self.mobiles = [] # contains all active mobiles EXCEPT those of type Player
        self.players = []
        self.displayedPlayer = None
    def addMobiles(self, newMobiles):
        """Call this to add some new mobiles to the list of active
        mobiles."""
        self.mobiles.extend(newMobiles)
    def addPlayer(self, region, playerCatalogEntry):
        """Call this to add a new Player to the game at the specified location. The
        playerId of this new player must be unique."""
        assert isinstance(region, Region)
        assert isinstance(playerCatalogEntry, PlayerCatalogEntry)
        newPlayer = playerCatalogEntry.getPlayer(region)
        assert newPlayer.playerId not in [p.playerId for p in self.players]
        self.players.append(newPlayer)
        location = playerCatalogEntry.getLocation()
        startingRoom = self.rooms[location.roomNumber]
        newPlayer.setLocation(startingRoom, location.coordinates)
        startingRoom.cellAt(*location.coordinates).addThing(newPlayer)
    def setDisplayedPlayer(self, playerId):
        if self.displayedPlayer is not None:
            self.displayedPlayer.displayed = False
        foundThePlayer = False
        for player in self.players:
            if player.playerId == playerId:
                assert not foundThePlayer # should only find it once
                player.displayed = True
                self.displayedPlayer = player
                foundThePlayer = True
        assert foundThePlayer # should find it at least once

        
        
# ========= End Classes for Game =========




# ========= Start Functions for Game =========


def moveMobiles(world, currentTime, screenChanges):
    """This function will cause all of the mobiles to move one step,
    updating the world accordingly."""
    for mobile in world.mobiles:
        if currentTime >= mobile.whenItCanAct:
            mobile.takeOneStep(currentTime, world, screenChanges)
    




def updateWorld(world, eventList, screenChanges):
    currentTime = int(time.perf_counter()*1000)
    # Non-Action Events
    for event in eventList.nonActionEvents:
        if isinstance(event, QuitGameEvent):
            world.gameOver = True
    # Action Events
    for player in world.players:
        if not player.isDead:
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
                        if eventToActOn.keyCode == KeyCode.GO_DOWN:
                            player.moveSouth(world, screenChanges)
                            player.whenItCanAct = currentTime + 500
                        if eventToActOn.keyCode == KeyCode.GO_UP:
                            player.moveNorth(world, screenChanges)
                            player.whenItCanAct = currentTime + 500
                        if eventToActOn.keyCode == KeyCode.GO_RIGHT:
                            player.moveEast(world, screenChanges)
                            player.whenItCanAct = currentTime + 500
                        if eventToActOn.keyCode == KeyCode.GO_LEFT:
                            player.moveWest(world, screenChanges)
                            player.whenItCanAct = currentTime + 500
    # Move Mobiles
    moveMobiles(world, currentTime, screenChanges)
    # Check for Death
    handleDeath(world)
    # Check for GameOver
    handleGameOver(world)
            

def handleDeath(world):
    for mobile in world.mobiles:
        if mobile.isDead:
            x, y = mobile.position
            cell = mobile.room.cellAt(x, y)
            cell.removeThing(mobile)
            world.mobiles.remove(mobile)
    for player in world.players:
        if player.isDead:
            x, y = player.position
            cell = player.room.cellAt(x, y)
            cell.removeThing(player)
            world.players.remove(player)

def handleGameOver(world):
    reasonToKeepPlaying = False
    for player in world.players:
        if player.numClients > 0 or player.displayed:
            reasonToKeepPlaying = True
    if not reasonToKeepPlaying:
        world.gameOver = True

def processClientMessages(world, clients, eventList):
    """This function gets any messages waiting on the queue from clients.
    If this results in new events, they will be written to the eventList."""
    for message, replyFunc in clients.receiveMessages():
        if isinstance(message, JoinServerMessage):
            print(f"Got JoinServerMessage to join client {message.playerId}.")
            playersWithId = [x for x in world.players if x.playerId == message.playerId]
            # FIXME: Better error handling than assert!
            assert len(playersWithId) == 1
            player = playersWithId[0]
            player.addClient()
            room = player.room
            print(f"WelcomeClientMessage to just 1 client")
            message = WelcomeClientMessage( room.width, room.height, room.gridInMessageFormat() )
            replyFunc(message)
        elif isinstance(message, KeyPressedMessage):
            pass # FIXME: Need this to handle key presses in client (later)
        elif isinstance(message, ClientDisconnectingMessage):
            # FIXME: I **SHOULD** call player.removeClient(), but I don't know which player.
            pass
        else:
            raise Exception(f"Message type not supported for message {message}.")
    


def renderWorld(world, display, region, screenChanges, clients):
    # -- Local screen --
    display.show(world.displayedPlayer.room, region.imageLibrary)

    # -- Remote clients --
    for player in world.players:
        if player.numClients > 0:
            roomSwitch = screenChanges.getRoomSwitches(player)
            if roomSwitch is not None:
                oldRoom, newRoom = roomSwitch
                message = NewRoomMessage(newRoom.width, newRoom.height, newRoom.gridInMessageFormat())
            else:
                room = player.room
                roomChangeSet = screenChanges.getRoomChangeSet(room)
                if isinstance(roomChangeSet, SetOfEverything):
                    message = RefreshRoomMessage(room.gridInMessageFormat())
                elif len(roomChangeSet) > 0:
                    updates = [(x,y,room.cellAt(x,y).toMessageFormat()) for (x,y) in roomChangeSet]
                    message = UpdateRoomMessage(updates)
                else:
                    message = None
            if message is not None:
                clients.sendMessageToPlayer(player.playerId, message)



def mainLoop(world):
    screenChanges = ScreenChanges()
    eventList = EventList()
    display = PygameGridDisplay()
    region = objects.defaultRegion
    clients = ServersideClientConnections()

    world.setDisplayedPlayer(world.players[0].playerId)
    
    while not world.gameOver:
        eventList.clear()
        screenChanges.clear()
        eventList.addPygameEvents(display.getEvents(), world.displayedPlayer.playerId)
        processClientMessages(world, clients, eventList)
        updateWorld(world, eventList, screenChanges)
        renderWorld(world, display, region, screenChanges, clients)
    display.quit()
    clients.sendMessageToAll(ClientShouldExitMessage())
    


# ========= End Functions for Game =========

world = World()
playerCatalogEntry = random.choice(thePlayerCatalog.entries)
world.addPlayer(objects.defaultRegion, playerCatalogEntry)
mainLoop(world)
