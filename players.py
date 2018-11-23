#
# Contains the Player class, as well as the master
# PlayerCatalog.
#

from gamecomponents import Location
from mobile import Mobile



class Player(Mobile):
    def __init__(self, region, tileName, health, maxMana, playerId):
        super().__init__(region, tileName, health, maxMana)
        self.queuedEvent = None
        self.playerId = playerId
        self.clientConnections = []
        self.displayed = False
    def goToLocation(self, location, world, screenChanges):
        oldRoom = self.room
        super().goToLocation(location, world, screenChanges)
        if self.room != oldRoom:
            screenChanges.playerSwitchedRooms(self, oldRoom, self.room)
            newMobiles = self.room.playerEntersRoom()
            if newMobiles:
                world.addMobiles(newMobiles)
    def addClient(self, clientConnection):
        self.clientConnections.append(clientConnection)
    def removeClient(self, clientConnection):
        assert clientConnection in self.clientConnections
        self.clientConnections.remove(clientConnection)


class PlayerCatalogEntry:
    """Just contains information about one way a player can be
    created."""
    def __init__(self, tileName, health, maxMana, playerId, location):
        self.tileName = tileName
        self.health = health
        self.maxMana = maxMana
        self.playerId = playerId
        self.location = location
    def getPlayer(self, region):
        return Player(
            region=region,
            tileName=self.tileName,
            health=self.health,
            maxMana=self.maxMana,
            playerId=self.playerId)
    def getLocation(self):
        return self.location


class PlayerCatalog:
    """This is a class that manages information about what players
    can be instantiated in the game. It probably should get MUCH
    better someday, but for now it's just a hard-coded list of
    specific player settings."""
    def __init__(self):
        self.entries = []
    def addEntry(self, playerCatalogEntry):
        assert isinstance(playerCatalogEntry, PlayerCatalogEntry)
        self.entries.append(playerCatalogEntry)
    def getEntryById(self, playerId):
        """Returns a PlayerCatalogEntry for a player with that ID, or None if there is no
        catalog entry with that ID."""
        for entry in self.entries:
            if entry.playerId == playerId:
                return entry
        return None


thePlayerCatalog = PlayerCatalog()
thePlayerCatalog.addEntry(PlayerCatalogEntry('adventurer-1-boy', 9, 10, "0", Location( 1, (2,1) )))
thePlayerCatalog.addEntry(PlayerCatalogEntry('adventurer-2-girl', 9, 10, "1", Location( 1, (3,2) )))
thePlayerCatalog.addEntry(PlayerCatalogEntry('adventurer-3-girl', 9, 11, "2", Location( 1, (1,2) )))

    
