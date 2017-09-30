
import random
from images import Region



class Thing:
    """Represents any kind of thing in the world."""
    def __init__(self, region, tileName):
        assert isinstance(region, Region)
        assert isinstance(tileName, str)
        self.tileId = region.imageLibrary.idByName(tileName)
    def canEnter(self, mobile):
        """Tests whether the mobile can enter a space containing
        this thing. Returns True if it can and False if not."""
        return True
    def doEnter(self, mobile, world, screenChanges):
        """This gets called when a mobile enters the same cell as
        this thing."""
        pass
    def doBump(self, mobile, world, screenChanges):
        """This gets called when a mobile bumps the cell with this thing."""
        pass


class Wall(Thing):
    """A thing that the player cannot enter."""
    def canEnter(self, mobile):
        return False


class Door(Thing):
    """A thing that teleports you to a new location when you enter."""
    def __init__(self, region, tileName, destination):
        super().__init__(region, tileName)
        self.destination = destination
    def doEnter(self, mobile, world, screenChanges):
        mobile.goToLocation(self.destination, world, screenChanges)

class Trap(Thing):
    """a thing that maks you take damage"""
    def doEnter(self, mobile, world, screenChanges):
        mobile.takeDamage(1)
        

class Item(Thing):
    """A parent class for any Thing that can be put in an inventory."""
    pass


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
    def __init__(self, region, tileName, hitPoints):
        super().__init__(region, tileName)
        self.whenItCanAct = 0
        self.hitPoints = hitPoints
        self.isDead = False
        self.inventory = []
    def canEnter(self, mobile):
        return False
    def doBump(self, mobile, world, screenChanges):
        """This gets called when a mobile bumps the cell with this thing."""
        self.takeDamage(1)
    def setLocation(self, room, position):
        """This sets the location of a player to a specific grid and (x,y) coordinate."""
        self.room = room
        self.position = position
    def moveSouth(self, world, screenChanges):
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
            screenChanges.changeTwoCells(self.room, oldX, oldY, newX, newY)
            # -- let things happen --
            newCell.doEnter(self, world, screenChanges)
        else:
            # -- let things happen --
            newCell.doBump(self, world, screenChanges)
    def moveEast(self, world, screenChanges):
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
            screenChanges.changeTwoCells(self.room, oldX, oldY, newX, newY)
            # -- let things happen --
            newCell.doEnter(self, world, screenChanges)
        else:
            # -- let things happen --
            newCell.doBump(self, world, screenChanges)
    def moveWest(self, world, screenChanges):
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
            screenChanges.changeTwoCells(self.room, oldX, oldY, newX, newY)
            # -- let things happen --
            newCell.doEnter(self, world, screenChanges)
        else:
            # -- let things happen --
            newCell.doBump(self, world, screenChanges)
    def moveNorth(self, world, screenChanges):
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
            screenChanges.changeTwoCells(self.room, oldX, oldY, newX, newY)
            # -- let things happen --
            newCell.doEnter(self, world, screenChanges)
        else:
            # -- let things happen --
            newCell.doBump(self, world, screenChanges)
    def goToLocation(self, location, world, screenChanges):
        """Calling this makes the player move from it's current location to
        the new location specified."""
        oldCell = self.room.cellAt(self.position[0], self.position[1])
        oldCell.removeThing(self)
        self.room = world.rooms[ location.roomNumber ]
        self.position = location.coordinates
        x,y = location.coordinates
        newCell = self.room.cellAt(x, y)
        newCell.addThing(self)
        screenChanges.changeCell(self.room, x, y)
    def takeOneStep(self, currentTime, world, screenChanges):
        randomNumber = random.randrange(4)
        if randomNumber == 0:
            self.moveNorth(world, screenChanges)
        elif randomNumber == 1:
            self.moveSouth(world, screenChanges)
        elif randomNumber == 2:
            self.moveEast(world, screenChanges)
        else:
            self.moveWest(world, screenChanges)
        self.whenItCanAct = currentTime + 500
    def takeDamage(self, amount):
        self.hitPoints=self.hitPoints-amount
        print(self.hitPoints)
        if self.hitPoints < 1:
            self.isDead = True
            print (self.isDead)
    def receiveItem(self, item):
        """This is called to potentially give an item to a mobile.
        If the item is successfully put in the mobile's inventory
        this returns True, if not it returns False."""
        assert isinstance(item, Item)
        self.inventory.append(item)
        return True
    def pickUpItem(self):
        """This makes the mobile attempt to pick up the top item
        in the space the mobile occupies. Picking it up might
        succeed or it might not."""
        cell = self.room.cellAt(self.position[0], self.position[1])
        itemsInCell = [x for x in cell.things if isinstance(x, Item)]
        if itemsInCell:
            topItem = itemsInCell[-1]
            if isinstance(topItem, Item):
                iGotIt = self.receiveItem(topItem)
                if iGotIt:
                    cell.removeThing(topItem)
            
            
    

