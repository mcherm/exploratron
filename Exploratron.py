#
# This contains the game currently known as "Exploratron". 
#

import kindsofthing
from kindsofthing import *
from objects import *
from images import ImageLibrary, TILE_SIZE, PygameGridDisplay
from events import *
from exploranetworking import *
from screenchanges import ScreenChanges, SetOfEverything
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
    


def renderWorld(world, display, imageLibrary, screenChanges, clients):
    # -- Local screen --
    display.show(world.player.room, imageLibrary)

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
    imageLibrary = ImageLibrary()
    clients = ServersideClientConnections()
    player = world.player
    while not world.gameOver:
        eventList.clear()
        screenChanges.clear()
        eventList.addPygameEvents(display.getEvents(), world.player.playerId)
        processClientMessages(world, clients, eventList)
        updateWorld(world, eventList, screenChanges)
        renderWorld(world, display, imageLibrary, screenChanges, clients)
    display.quit()
    clients.sendMessageToAll(ClientShouldExitMessage())
    


# ========= End Functions for Game =========

mainLoop(World())
