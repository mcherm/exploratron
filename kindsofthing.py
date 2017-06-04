
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
    def setLocation(self, grid, position):
        """This sets the location of a player to a specific grid and (x,y) coordinate."""
        self.grid = grid
        self.position = position
    def moveSouth(self):
        # -- find the new location --
        oldX, oldY = self.position
        newX = oldX
        newY = oldY + 1
        # -- check if it is on the map --
        if newX < 0 or newY < 0 or newX >= self.grid.width or newY >= self.grid.height:
            return
        # -- check if we can enter --
        oldCell = self.grid.cellAt(oldX, oldY)
        newCell = self.grid.cellAt(newX, newY)
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
        if newX < 0 or newY < 0 or newX >= self.grid.width or newY >= self.grid.height:
            return
        # -- check if we can enter --
        oldCell = self.grid.cellAt(oldX, oldY)
        newCell = self.grid.cellAt(newX, newY)
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
        if newX < 0 or newY < 0 or newX >= self.grid.width or newY >= self.grid.height:
            return
        # -- check if we can enter --
        oldCell = self.grid.cellAt(oldX, oldY)
        newCell = self.grid.cellAt(newX, newY)
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
        if newX < 0 or newY < 0 or newX >= self.grid.width or newY >= self.grid.height:
            return
        # -- check if we can enter --
        oldCell = self.grid.cellAt(oldX, oldY)
        newCell = self.grid.cellAt(newX, newY)
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
        oldCell = self.grid.cellAt(self.position[0], self.position[1])
        oldCell.removeThing(self)
        self.grid = world.rooms[ location.roomNumber ]
        self.position = location.coordinates
        newCell = self.grid.cellAt(location.coordinates[0], location.coordinates[1])
        newCell.addThing(self)
    def takeOneStep(self):
        randomNumber = random.randrange(4)
        if randomNumber == 0:
            self.moveNorth()
        elif randomNumber == 1:
            self.moveSouth()
        elif randomNumber == 2:
            self.moveEast()
        else:
            self.moveWest()

            
class Player(Mobile):
    pass

