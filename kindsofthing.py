
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
    def doEnter(self, mobile, screenChanges):
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
    def doEnter(self, mobile, screenChanges):
        mobile.goToLocation(self.destination, screenChanges)

class Trap(Thing):
    """a thing that maks you take damage"""
    def doEnter(self, mobile, screenChanges):
        mobile.takeDamage(1)
        


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
    def __init__(self, tileId, hitPoints):
        super().__init__(tileId)
        self.whenItCanAct = 0
        self.hitPoints=hitPoints
        self.isDead=False
    def setLocation(self, room, position):
        """This sets the location of a player to a specific grid and (x,y) coordinate."""
        self.room = room
        self.position = position
    def moveSouth(self, screenChanges):
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
            newCell.doEnter(self, screenChanges)
    def moveEast(self, screenChanges):
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
            newCell.doEnter(self, screenChanges)
    def moveWest(self, screenChanges):
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
            newCell.doEnter(self, screenChanges)
    def moveNorth(self, screenChanges):
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
            newCell.doEnter(self, screenChanges)
    def goToLocation(self, location, screenChanges):
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
    def takeOneStep(self, currentTime, screenChanges):
        randomNumber = random.randrange(4)
        if randomNumber == 0:
            self.moveNorth(screenChanges)
        elif randomNumber == 1:
            self.moveSouth(screenChanges)
        elif randomNumber == 2:
            self.moveEast(screenChanges)
        else:
            self.moveWest(screenChanges)
        self.whenItCanAct = currentTime + 500
    def takeDamage (self,amount):
        self.hitPoints=self.hitPoints-amount
        print(self.hitPoints)
        if self.hitPoints < 1:
            self.isDead = True
            print (self.isDead) 
            
    
        
class Player(Mobile):
    def __init__(self, tileId, hitPoints, playerId):
        super().__init__(tileId, hitPoints)
        self.queuedEvent = None
        self.playerId = playerId
        self.numClients = 0
    def goToLocation(self, location, screenChanges):
        oldRoom = self.room
        super().goToLocation(location, screenChanges)
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

