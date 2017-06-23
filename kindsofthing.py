
import random


world = None




class Thing:
    """Represents any kind of thing in the world."""
    def __init__(self, tileId):
        self.tileId = tileId
    def canEnter(self, mobile):
        """Tests whether the mobile can enter a space containing
        this thing. Returns True if it can and False if not."""
        return True
    def doEnter(self, mobile):
        """This gets called when a mobile enters the same cell as
        this thing."""
        pass


class Wall(Thing):
    """A thing that the player cannot enter."""
    def canEnter(self, mobile):
        return False


class Door(Thing):
    """A thing that teleports you to a new location when you enter."""
    def __init__(self, tileId, destination):
        super().__init__(tileId)
        self.destination = destination
    def doEnter(self, mobile):
        mobile.goToLocation(self.destination)


"""
Kinds of things:
  * Stuff you can walk on.
      Ex: Dirt
  * Walls you cannot go past.
      Ex: BrickWall
  * Stuff you interact with by walking on
      Ex: Trap
  * Stuff that moves
      Ex: Monsters
"""

class Mobile(Thing):
    def __init__(self, tileId):
        super().__init__(tileId)
        self.whenItCanAct = 0
    def setLocation(self, room, position):
        """This sets the location of a player to a specific grid and (x,y) coordinate."""
        self.room = room
        self.position = position
    def moveSouth(self):
        # -- find the new location --
        oldX, oldY = self.position
        newX = oldX
        newY = oldY + 1
        # -- check if it is on the map --
        if newX < 0 or newY < 0 or newX >= self.room.width or newY >= self.room.height:
            return
        # -- check if we can enter --
        oldCell = self.room.cellAt(oldX, oldY)
        newCell = self.room.cellAt(newX, newY)
        if newCell.canEnter(self):
            # -- update my position and the cell --
            self.position = (newX, newY)
            oldCell.removeThing(self)
            newCell.addThing(self)
            # -- let things happen --
            newCell.doEnter(self)
    def moveEast(self):
        oldX, oldY = self.position
        newX = oldX + 1
        newY = oldY 
        # -- check if it is on the map --
        if newX < 0 or newY < 0 or newX >= self.room.width or newY >= self.room.height:
            return
        # -- check if we can enter --
        oldCell = self.room.cellAt(oldX, oldY)
        newCell = self.room.cellAt(newX, newY)
        if newCell.canEnter(self):
            # -- update my position and the cell --
            self.position = (newX, newY)
            oldCell.removeThing(self)
            newCell.addThing(self)
            # -- let things happen --
            newCell.doEnter(self)
    def moveWest(self):
        oldX, oldY = self.position
        newX = oldX - 1
        newY = oldY 
        # -- check if it is on the map --
        if newX < 0 or newY < 0 or newX >= self.room.width or newY >= self.room.height:
            return
        # -- check if we can enter --
        oldCell = self.room.cellAt(oldX, oldY)
        newCell = self.room.cellAt(newX, newY)
        if newCell.canEnter(self):
            # -- update my position and the cell --
            self.position = (newX, newY)
            oldCell.removeThing(self)
            newCell.addThing(self)
            # -- let things happen --
            newCell.doEnter(self)
    def moveNorth(self):
        oldX, oldY = self.position
        newX = oldX
        newY = oldY - 1
        # -- check if it is on the map --
        if newX < 0 or newY < 0 or newX >= self.room.width or newY >= self.room.height:
            return
        # -- check if we can enter --
        oldCell = self.room.cellAt(oldX, oldY)
        newCell = self.room.cellAt(newX, newY)
        if newCell.canEnter(self):
            # -- update my position and the cell --
            self.position = (newX, newY)
            oldCell.removeThing(self)
            newCell.addThing(self)
            # -- let things happen --
            newCell.doEnter(self)
    def goToLocation(self, location):
        """Calling this makes the player move from it's current location to
        the new location specified."""
        oldCell = self.room.cellAt(self.position[0], self.position[1])
        oldCell.removeThing(self)
        self.room = world.rooms[ location.roomNumber ]
        self.position = location.coordinates
        newCell = self.room.cellAt(location.coordinates[0], location.coordinates[1])
        newCell.addThing(self)
    def takeOneStep(self, currentTime):
        randomNumber = random.randrange(4)
        if randomNumber == 0:
            self.moveNorth()
        elif randomNumber == 1:
            self.moveSouth()
        elif randomNumber == 2:
            self.moveEast()
        else:
            self.moveWest()
        self.whenItCanAct = currentTime + 500

            
class Player(Mobile):
    def __init__(self, tileId):
        super().__init__(tileId)
        self.queuedEvent = None
    def goToLocation(self, location):
        oldRoom = self.room
        super().goToLocation(location)
        if self.room != oldRoom:
            newMobiles = self.room.playerEntersRoom()
            if newMobiles:
                world.addMobiles(newMobiles)

