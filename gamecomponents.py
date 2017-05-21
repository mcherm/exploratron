from kindsofthing import *


class Location:
    """This is a way to specify a particular place."""
    def __init__(self, roomNumber, coordinates):
        self.roomNumber = roomNumber
        self.coordinates = coordinates

class Cell:
    """Contains a stack of things."""
    def __init__(self):
        self.things = []
    def addThing(self, thing):
        assert isinstance(thing, Thing)
        self.things.append(thing)
    def removeThing(self, thing):
        """This will remove the thing from this cell if it is in this
        cell. If it is not there then this raises ValueError."""
        self.things.remove(thing)
    def canEnter(self, mobile):
        """This returns True if the mobile is able to enter into this
        cell."""
        for thing in self.things:
            if not thing.canEnter(mobile):
                return False
        return True
    def doEnter(self, mobile):
        """This gets called when a mobile enters into this cell. It should
        make sure that all the things in the cell that do anything when you
        enter do whatever they are supposed to."""
        for thing in self.things:
            thing.doEnter(mobile)


class Grid:
    """A grid has rows and colums of cells."""
    def __init__(self, width, height):
        self.cells = [ [Cell() for x in range(width)] for y in range(height)]
        self.width = width
        self.height = height
    def cellAt(self, x, y):
        return self.cells[y][x]

