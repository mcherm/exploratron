from kindsofthing import Thing
from mobile import Mobile
from clientdata import GridData, CellData


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
    def doEnter(self, mobile, world, screenChanges):
        """This gets called when a mobile enters into this cell. It should
        make sure that all the things in the cell that do anything when you
        enter do whatever they are supposed to."""
        for thing in self.things:
            thing.doEnter(mobile, world, screenChanges)
    def doBump(self, mobile, world, screenChanges):
        """This gets called when a mobile trys to enters the cell and falils. It should
        make sure that all the things in the cell that do anything when you
        enter do whatever they are supposed to."""
        for thing in self.things:
            thing.doBump(mobile, world, screenChanges)
    def toMessageFormat(self):
        """Returns a number (representing the single tileId in this cell)
        OR a list of numbers (representing the stack of tiles in this cell)."""
        if len(self.things) == 1:
            return self.things[0].tileId
        else:
            return [x.tileId for x in self.things]


class Grid:
    """A grid has rows and columns of cells."""
    def __init__(self, width, height):
        self.cells = [ [Cell() for x in range(width)] for y in range(height)]
        self.width = width
        self.height = height
    def cellAt(self, x, y):
        return self.cells[y][x]
    def toGridData(self):
        """This returns the information of what is in the grid in the form of
        a GridData."""
        allCells = []
        for row in self.cells:
            allCells.extend([CellData(tuple(x.tileId for x in cell.things)) for cell in row])
        return GridData(self.width, self.height, allCells)


class Room:
    """A room is a location that mobiles can move through."""
    def __init__(self, background, items=None, mobilesAtEntry=None):
        """The background should be a 2-D list of Things which lays out
        the stuff in the background in the room. This is used to determine
        the width and height of the room. items can be None (for
        no items in the room) or a map where the keys are a location
        (an (x,y) tuple) and the values are either a Thing or a list
        of things to be placed in that location. Finally, mobiles is None
        or a map where keys are a location and values are a mobile who
        should be added to the room atthat spot the first time the room
        is entered."""
        self.width = len(background[0])
        self.height = len(background)
        self.hasBeenEntered = False
        self.mobilesAtEntry = mobilesAtEntry
        self.grid = Grid(self.width, self.height)
        for y, row in enumerate(background):
            assert len(row) == self.width
            for x, thing in enumerate(row):
                self.cellAt(x,y).addThing(thing)
        if items:
            for location, thingOrThings in items.items():
                x,y = location
                if isinstance(thingOrThings, Thing):
                    self.cellAt(x,y).addThing(thingOrThings)
                else:
                    for thing in thingOrThings:
                        self.cellAt(x,y).addThing(thing)
    def cellAt(self, x, y):
        assert 0 <= x < self.width
        assert 0 <= y < self.height
        return self.grid.cellAt(x,y)
    def playerEntersRoom(self):
        """The Game will call this when a player enters the room. The first
        time it is entered, this will add the mobiles; all other times it
        will do nothing. It returns a list of the newly added mobiles."""
        if self.hasBeenEntered:
            return []
        else:
            self.hasBeenEntered = True
            result = []
            if self.mobilesAtEntry:
                for location, mobile in self.mobilesAtEntry.items():
                    x,y = location
                    assert isinstance(mobile, Mobile)
                    mobile.setLocation(self, location)
                    self.cellAt(x,y).addThing(mobile)
                    result.append(mobile)
            return result
    def gridData(self):
        """Returns an exploranetworking.GridData of the information in the
        room."""
        return self.grid.toGridData()

