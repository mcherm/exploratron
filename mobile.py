from kindsofthing import Thing, Item, Weapon
import random

class Stats:
    def __init__(self):
        """Create a new Stats, with all stats set to 0."""
        self.speed = 0
        self.maxHealth = 0
        self.health = 0
        self.mana = 0
        self.maxMana = 0

class Inventory:
    """An instance of this class is the stuff that a mobile carries around with
    them.

    It has a separate wielded weapon. If no weapon is wielded and a new weapon
    is put into the inventory, then it becomes the wielded weapon. Also the
    wieldWeapon() method can be used to change it."""

    def __init__(self, items=()):
        self.items = []
        self.wieldedWeapon = None
        assert all(isinstance(x, Item) for x in items)
        for x in items:
            self.addItem(x)

    def __iter__(self):
        return iter(self.items)

    def addItem(self, item):
        """Attempts to add an item. If it can be added, this returns True, if not
        then this returns False."""
        assert isinstance(item, Item)
        self.items.append(item)
        if self.wieldedWeapon is None and isinstance(item, Weapon):
            self.wieldedWeapon = item
        return True

    def removeItem(self, item):
        """Removes an item from the inventory. If the given item is not in the
        inventory then this raises a ValueError."""
        if item == self.wieldedWeapon:
            self.wieldedWeapon = None
        self.items.remove(item)

    def getWieldedWeapon(self):
        """Returns the currently wielded weapon, or None if no weapon is wielded."""
        return self.wieldedWeapon



class Mobile(Thing):
    def __init__(self, region, tileName, maxHealth, maxMana, inventory=()):
        super().__init__(region, tileName)
        self.whenItCanAct = 0
        self.isDead = False
        self.inventory = Inventory(inventory)
        self.stats = Stats()
        self.stats.maxHealth = maxHealth
        self.stats.health = maxHealth
        self.stats.maxMana = maxMana
        self.stats.mana = maxMana
        self.stats.speed = 5
    def canEnter(self, mobile):
        return False
    def doBump(self, mobile, world, screenChanges):
        """This gets called when a mobile bumps the cell with this thing."""
        wieldedWeapon = mobile.getWieldedWeapon()
        if wieldedWeapon == None:
            pass
        else:
            screenChanges.roomPlaySound(self.room, wieldedWeapon.getHitSoundEffectId())
            self.takeDamage(wieldedWeapon.damage)
    def timeToWait(self):
        timeToWait = (500 - (self.stats.speed) * 20)
        return timeToWait
    def getWieldedWeapon(self):
        """This returns the weapon that the mobile is wielding, or it
        returns None if the mobile is not wielding any weapon."""
        return self.inventory.getWieldedWeapon()
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
        self.room = world.rooms[location.roomNumber]
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
        self.whenItCanAct = currentTime + self.timeToWait()
    def takeDamage(self, amount):
        self.stats.health = self.stats.health-amount
        if self.stats.health < 1:
            self.isDead = True
            print (self.isDead)
    def receiveItem(self, item):
        """This is called to potentially give an item to a mobile.
        If the item is successfully put in the mobile's inventory
        this returns True, if not it returns False."""
        return self.inventory.addItem(item)
    def pickUpItem(self):
        """This makes the mobile attempt to pick up the top item
        in the space the mobile occupies. Picking it up might
        succeed or it might not."""
        cell = self.room.cellAt(self.position[0], self.position[1])
        itemsInCell = [x for x in cell.things if isinstance(x, Item)]
        if itemsInCell:
            topItem = itemsInCell[-1]
            iGotIt = self.receiveItem(topItem)
            if iGotIt:
                cell.removeThing(topItem)
    def placeItem(self, item):
        """This makes the mobile place an item in its current location."""
        cell = self.room.cellAt(self.position[0], self.position[1])
        cell.things.append(item)
    def doRegen(self):
        """This gets called once every 10 seconds. When it is called the
        mobile should perform regeneration updates such as healing damage."""
        if self.stats.health < self.stats.maxHealth:
            self.stats.health = self.stats.health + 1


