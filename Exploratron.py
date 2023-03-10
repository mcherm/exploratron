#
# This contains the game currently known as "Exploratron". 
#

from pygame import init as pygame_init
pygame_init() # Need to run this before some of the code that runs during imports


import objects
from players import thePlayerCatalog, PlayerCatalogEntry
from images import Region
from display import PygameDisplay
from events import EventList, KeyPressedEvent, KeyCode, QuitGameEvent, NewPlayerAddedEvent, ItemDroppedEvent, EquipItemEvent
from exploranetworking import *
from screenchanges import ScreenChanges, SetOfEverything
from players import Player
from clientdata import CellData, InventoryData
from mobile import EquipmentTypeCode
import rooms
import time
import random
import itertools


# ========= Start of Classes for Game =========




class World:
    """Represents the entire world."""
    def __init__(self):
        self.gameOver = False
        self.rooms = rooms.rooms
        self.mobiles = [] # contains all active mobiles EXCEPT those of type Player
        self.players = []
        self.playerByPlayerId = {} # FIXME: Don't need map AND ALSO the list
        self.displayedPlayer = None
        self.playerCatalog = thePlayerCatalog
        self.timeOfNextRegen = 0
    def addMobiles(self, newMobiles):
        """Call this to add some new mobiles to the list of active
        mobiles."""
        self.mobiles.extend(newMobiles)
    def addPlayer(self, region, playerCatalogEntry):
        """Call this to add a new Player to the game at the specified location. The
        playerId of this new player must be unique. It returns the newly created Player."""
        assert isinstance(region, Region)
        assert isinstance(playerCatalogEntry, PlayerCatalogEntry)
        newPlayer = playerCatalogEntry.getPlayer(region)
        assert newPlayer.playerId not in [p.playerId for p in self.players]
        self.players.append(newPlayer)
        self.playerByPlayerId[newPlayer.playerId] = newPlayer
        location = playerCatalogEntry.getLocation()
        startingRoom = self.rooms[location.roomNumber]
        newPlayer.setLocation(startingRoom, location.coordinates)
        startingRoom.cellAt(*location.coordinates).addThing(newPlayer)
        return newPlayer
    def removePlayer(self, player):
        """Passed a player, removes it."""
        self.players.remove(player)
        del self.playerByPlayerId[player.playerId]
    def getPlayer(self, playerId):
        """Passed a playerId, this returns the given player, or raises an exception if it isn't
        in the list of players."""
        return self.playerByPlayerId[playerId]
    def setDisplayedPlayer(self, playerId):
        if self.displayedPlayer is not None:
            self.displayedPlayer.displayed = False
        self.displayedPlayer = self.getPlayer(playerId)
        self.displayedPlayer.displayed = True

        
        
# ========= End of Classes for Game =========




# ========= Start of Functions for Game =========


def regenMobiles(world, currentTime):
    """Calls doRegen() on each mobile (so it can do things like
    healing) but only call if it has been 10 seconds since the last
    time that we updated them."""
    if currentTime >= world.timeOfNextRegen:
        world.timeOfNextRegen = currentTime + 10000
        for mobile in world.mobiles + world.players:
            mobile.doRegen()


def moveMobiles(world, currentTime, screenChanges):
    """This function will cause all of the mobiles to move one step,
    updating the world accordingly."""
    for mobile in world.mobiles:
        if currentTime >= mobile.whenItCanAct:
            mobile.takeOneAction(currentTime, world, screenChanges)
    




def updateWorld(world, region, eventList, screenChanges, uiState):
    currentTime = int(time.perf_counter()*1000)
    # Non-Action Events
    for event in eventList.getNonActionEvents():
        if isinstance(event, QuitGameEvent):
            world.gameOver = True
        elif isinstance(event, NewPlayerAddedEvent):
            newPlayer = world.addPlayer(region, event.playerCatalogEntry)
            newPlayer.addClient(event.clientConnection)
            room = newPlayer.room
            print(f"WelcomeClientMessage to just 1 client")
            message = WelcomeClientMessage( room.gridData() )
            event.clientConnection.send(message)
            # FIXME: Should probably update screenChanges
        elif isinstance(event, KeyPressedEvent):
            if event.keyCode == KeyCode.MOVE_UI_UP:
                uiState.moveUINorth()
            elif event.keyCode == KeyCode.MOVE_UI_DOWN:
                uiState.moveUISouth()
            elif event.keyCode == KeyCode.MOVE_UI_LEFT:
                uiState.moveUIWest()
            elif event.keyCode == KeyCode.MOVE_UI_RIGHT:
                uiState.moveUIEast()
            elif event.keyCode == KeyCode.UI_ACTION:
                uiState.takeAction()
            elif event.keyCode == KeyCode.TOGGLE_INVENTORY:
                uiState.toggleInventoryLocal(world.displayedPlayer, screenChanges)
        elif isinstance(event, ItemDroppedEvent):
            world.getPlayer(event.playerId).dropItem(event.itemUniqueId, screenChanges)
        elif isinstance(event, EquipItemEvent):
            player = world.getPlayer(event.playerId)
            if event.itemUniqueId is None:
                item = None
            else:
                item = player.inventory.findItemById(event.itemUniqueId)
                # Note: if item they gave wasn't in the inventory we'll still
                #   unwield any existing wielded item. That is the desired behavior.
            if event.equipmentTypeCode == EquipmentTypeCode.WEAPON:
                player.inventory.wieldWeapon(item)
            elif event.equipmentTypeCode == EquipmentTypeCode.WAND:
                player.inventory.wieldWand(item)
            else:
                raise AssertionError(f"Unknown EquipmentTypeCode: '{event.equipmentTypeCode}'")
        else:
            raise Exception(f'Unexpected event: {event}')
    # Action Events
    for player in world.players:
        if not player.isDead:
            if currentTime < player.whenItCanAct:
                # Player cannot act yet
                if player.queuedEvent is None:
                    # Player does not have an event queued
                    player.queuedEvent = eventList.getFirstActionEvent(player.playerId)
            else:
                # Player can act now
                eventToActOn = player.queuedEvent
                # We used the value, so clear it
                player.queuedEvent = None
                if eventToActOn is None:
                    # Set eventToActOn to the FIRST action event
                    eventToActOn = eventList.getFirstActionEvent(player.playerId)
                # Now we have set eventToActOn
                if eventToActOn is not None:
                    if isinstance(eventToActOn, KeyPressedEvent):
                        if eventToActOn.keyCode == KeyCode.GO_DOWN:
                            player.moveSouth(currentTime, world, screenChanges)
                        elif eventToActOn.keyCode == KeyCode.GO_UP:
                            player.moveNorth(currentTime, world, screenChanges)
                        elif eventToActOn.keyCode == KeyCode.GO_RIGHT:
                            player.moveEast(currentTime, world, screenChanges)
                        elif eventToActOn.keyCode == KeyCode.GO_LEFT:
                            player.moveWest(currentTime, world, screenChanges)
                        elif eventToActOn.keyCode == KeyCode.CAST:
                            player.cast(currentTime, world, screenChanges)
                        elif eventToActOn.keyCode == KeyCode.PICK_UP:
                            player.pickUpItem(currentTime, world, screenChanges)
    # Move Mobiles
    regenMobiles(world, currentTime)
    moveMobiles(world, currentTime, screenChanges)
    # Check for Death
    handleDeath(world, screenChanges)
    # Check for GameOver
    handleGameOver(world)
            

def handleDeath(world, screenChanges):
    for mobile in itertools.chain(world.mobiles, world.players):
        if mobile.isDead:
            x, y = mobile.position
            cell = mobile.room.cellAt(x, y)
            for item in mobile.inventory:
                mobile.dropItem(item, screenChanges)
            cell.removeThing(mobile)
            if mobile.isPlayer():
                world.removePlayer(mobile)
            else:
                world.mobiles.remove(mobile)
            screenChanges.changeCell(mobile.room, x, y)


def handleGameOver(world):
    reasonToKeepPlaying = False
    for player in world.players:
        if len(player.clientConnections) > 0 or player.displayed:
            reasonToKeepPlaying = True
    if not reasonToKeepPlaying:
        world.gameOver = True

def processClientMessages(world, clients, eventList):
    """This function gets any messages waiting on the queue from clients.
    If this results in new events, they will be written to the eventList."""
    for message, clientConnection in clients.receiveMessages():
        if isinstance(message, JoinServerMessage):
            print(f"Got JoinServerMessage to join client {message.playerId}.")
            # FIXME: Can be made cleaner now that there is getPlayer()
            playersWithId = [x for x in world.players if x.playerId == message.playerId]
            assert len(playersWithId) <= 1
            playerCatalogEntry = world.playerCatalog.getEntryById(message.playerId)
            if playersWithId:
                # Such a player exists; we just add a viewer
                player = playersWithId[0]
                player.addClient(clientConnection)
                room = player.room
                print(f"WelcomeClientMessage to just 1 client")
                message = WelcomeClientMessage( room.gridData() )
                clientConnection.send(message)
            elif playerCatalogEntry is not None:
                # No such player now, but we could add one
                eventList.addEvent(NewPlayerAddedEvent(playerCatalogEntry, clientConnection))
            else:
                # No such ID. We cannot welcome this client.
                # FIXME: Should return an error message to the client!
                pass
        elif isinstance(message, KeyPressedMessage):
            eventList.addEvent(KeyPressedEvent(clientConnection.playerId, message.keyCode))
        elif isinstance(message, RequestInventoryMessage):
            inventory = world.getPlayer(clientConnection.playerId).inventory
            inventoryData = InventoryData.fromInventory(inventory)
            clientConnection.send(InventoryMessage(inventoryData))
        elif isinstance(message, DropItemMessage):
            eventList.addEvent(ItemDroppedEvent(clientConnection.playerId, message.itemUniqueId))
        elif isinstance(message, EquipMessage):
            eventList.addEvent(EquipItemEvent(clientConnection.playerId, message.equipmentTypeCode, message.itemUniqueId))
        elif isinstance(message, ClientDisconnectingMessage):
            player = world.getPlayer(clientConnection.playerId)
            player.removeClient(clientConnection)
        else:
            raise Exception(f"Message type not supported for message {message}.")


def renderWorld(world, display, region, screenChanges, clients):
    renderWorldLocal(world, display, region, screenChanges)
    renderWorldRemote(world, screenChanges, clients)


def renderWorldLocal(world, display, region, screenChanges):
    # --- draw the tiles ---
    localRoomSwitches = screenChanges.getRoomSwitches(world.displayedPlayer)
    if localRoomSwitches is not None:
        oldRoom, newRoom = localRoomSwitches
        display.uiState.newRoom(newRoom.gridData())
    displayedRoom = world.displayedPlayer.room
    display.show(displayedRoom.gridData(), region.imageLibrary)
    # --- start any sounds ---
    display.playSounds(screenChanges.getRoomSounds(displayedRoom), region.soundLibrary)
    # --- possibly a message ---
    display.uiState.infoTexts.extend(screenChanges.getNewInfoTexts(world.displayedPlayer))
    # --- Add any new console messages ---
    newConsoleTexts  = screenChanges.getConsoleTextsForPlayer(world.displayedPlayer)
    for newConsoleText in newConsoleTexts:
        display.console.addMessage(newConsoleText)
    # --- update the visible data ---
    display.setVisibleData(VisibleData.fromEnvironment(world.displayedPlayer))


def renderWorldRemote(world, screenChanges, clients):
    for player in world.players:
        if len(player.clientConnections) > 0:
            # --- Send at most one message about drawing the tiles ---
            roomSwitch = screenChanges.getRoomSwitches(player)
            if roomSwitch is not None:
                oldRoom, newRoom = roomSwitch
                message = NewRoomMessage(newRoom.gridData())
                room = newRoom
            else:
                room = player.room
                roomChangeSet = screenChanges.getRoomChangeSet(room)
                if isinstance(roomChangeSet, SetOfEverything):
                    message = RefreshRoomMessage(room.gridData())
                elif len(roomChangeSet) > 0:
                    def cellDataFromCell(cell):
                        """Given a cell, returns a CellData for it."""
                        return CellData(tuple(thing.tileId for thing in cell.things))

                    updates = [(x, y, cellDataFromCell(room.cellAt(x, y))) for (x, y) in roomChangeSet]
                    message = UpdateRoomMessage(GridDataChange(updates))
                else:
                    message = None
            if message is not None:
                clients.sendMessageToPlayer(player.playerId, message)

            # --- Possibly a message about sounds ---
            soundIds = screenChanges.getRoomSounds(room)
            if soundIds:
                soundMessage = PlaySoundsMessage(soundIds)
                clients.sendMessageToPlayer(player.playerId, soundMessage)

            # --- Possibly some user messages ---
            newInfoTexts = screenChanges.getNewInfoTexts(player)
            if newInfoTexts:
                for infoText in newInfoTexts:
                    infoTextMessage = InfoTextMessage(infoText.getText())
                    clients.sendMessageToPlayer(player.playerId, infoTextMessage)

            # --- Possibly some console messages ---
            newConsoleTexts = screenChanges.getConsoleTextsForPlayer(player)
            if newConsoleTexts:
                for consoleText in newConsoleTexts:
                    consoleTextMessage = ConsoleTextMessage(consoleText)
                    clients.sendMessageToPlayer(player.playerId, consoleTextMessage)

            # --- Possibly a message about displayed properties ---
            visibleData = VisibleData.fromEnvironment(player)
            for serversideClientConnection in clients.connectionsByPlayer.get(player.playerId):
                if visibleData != serversideClientConnection.visibleData:
                    serversideClientConnection.send(UpdateVisibleDataMessage(visibleData))
                    serversideClientConnection.visibleData = visibleData


def mainLoop(world):
    screenChanges = ScreenChanges()
    eventList = EventList()
    display = PygameDisplay()
    region = objects.defaultRegion
    clients = ServersideClientConnections()
    world.setDisplayedPlayer(world.players[0].playerId)
    display.setDisplayedPlayerId(world.players[0])

    while not world.gameOver:
        eventList.clear()
        screenChanges.clear()
        eventList.addPygameEvents(display.getEvents(), world.displayedPlayer.playerId)
        processClientMessages(world, clients, eventList)
        updateWorld(world, region, eventList, screenChanges, display.uiState)        
        renderWorld(world, display, region, screenChanges, clients)
    display.quit()
    clients.sendMessageToAll(ClientShouldExitMessage())
    


# ========= End of Functions for Game =========

# ========= Start of Run It All ==========

world = World()
playerCatalogEntry = random.choice(world.playerCatalog.entries)
world.addPlayer(objects.defaultRegion, playerCatalogEntry)
mainLoop(world)


# ========= End of Run It All ==========
