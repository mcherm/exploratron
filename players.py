#
# Contains the Player class, as well as the master
# PlayerCatalog.
#

from kindsofthing import Mobile
from gamecomponents import Location



class Player(Mobile):
    def __init__(self, region, tileName, hitPoints, playerId):
        super().__init__(region, tileName, hitPoints)
        self.queuedEvent = None
        self.playerId = playerId
        self.numClients = 0
        self.displayed = False
    def goToLocation(self, location, world, screenChanges):
        oldRoom = self.room
        super().goToLocation(location, world, screenChanges)
        if self.room != oldRoom:
            screenChanges.playerSwitchedRooms(self, oldRoom, self.room)
            newMobiles = self.room.playerEntersRoom()
            if newMobiles:
                world.addMobiles(newMobiles)
    def addClient(self):
        self.numClients += 1
    def removeClient(self):
        assert self.numClients > 0
        self.numClients -= 1


class PlayerCatalogEntry:
    """Just contains information about one way a player can be
    created."""
    def __init__(self, tileName, hitPoints, playerId, location):
        self.tileName = tileName
        self.hitPoints = hitPoints
        self.playerId = playerId
        self.location = location
    def getPlayer(self, region):
        return Player(
            region=region,
            tileName=self.tileName,
            hitPoints=self.hitPoints,
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


thePlayerCatalog = PlayerCatalog()
thePlayerCatalog.addEntry(PlayerCatalogEntry('drawntiles64/adventurer-1-boy', 9, "0", Location( 1, (2,1) )))
thePlayerCatalog.addEntry(PlayerCatalogEntry('drawntiles64/adventurer-2-girl', 9, "1", Location( 1, (3,2) )))

    