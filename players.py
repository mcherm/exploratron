#
# Contains the Player class, as well as the master
# PlayerCatalog.
#

from kindsofthing import Mobile


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
