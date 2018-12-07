#
# This contains the logic for a "brain" -- the AI component that decides how a
# mobile will behave.
#
# Most brains keep some state, so each brain instance is used by only a single
# mobile. However, the brain doesn't keep a reference to the mobile (to avoid
# ownership loops).
#

import random
from enum import Enum
from mobile import Mobile
from kindsofthing import Wall



Alignment = Enum('Alignment', 'FRIENDLY NEUTRAL UNFRIENDLY')



class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

    def deltaX(self):
        return _DIR_DELTA_X(self)

    def deltaY(self):
        return _DIR_DELTA_Y(self)


_DIR_DELTA_X = {
    Direction.NORTH: 0,
    Direction.SOUTH: 0,
    Direction.EAST: 1,
    Direction.WEST: -1,
}
_DIR_DELTA_Y = {
    Direction.NORTH: -1,
    Direction.SOUTH: 1,
    Direction.EAST: 0,
    Direction.WEST: 0,
}


class _ImpassableClass:
    def __repr__(self):
        return "IMPASSABLE"

IMPASSABLE = _ImpassableClass()

class _UnreachableClass:
    def __repr__(self):
        return "UNREACHABLE"
UNREACHABLE = _UnreachableClass()


class DijkstraMap:
    """This contains a grid of integers for each cell in a room. The first
    version of it will be specific to finding a path to any allies, but
    later I will generalize it.

    Throughout, this uses values, which are EITHER a non-negative integer
    or None (meaning not yet initialized), or IMPASSIBLE or UNREACHABLE."""
    def __init__(self, room):
        self.width = room.width
        self.height = room.height
        self.data = [None] * (self.width * self.height)
        for y in range(self.height):
            for x in range(self.width):
                roomCell = room.cellAt(x, y)
                isImpassible = False
                hasFriendly = False
                for thing in roomCell.things:
                    if isinstance(thing, Wall):
                        isImpassible = True
                    if isinstance(thing, Mobile) and thing.brain.getAlignment() is Alignment.FRIENDLY:
                        hasFriendly = True
                if isImpassible:
                    self.setValueAt(x, y, IMPASSABLE)
                elif hasFriendly:
                    self.setValueAt(x, y, 0)
                else:
                    pass # leave the rest as None

    def valueAt(self, x, y):
        """Returns the integer value at that position."""
        assert 0 <= x < self.width
        assert 0 <= y < self.height
        return self.data[x + (y * self.width)]

    def setValueAt(self, x, y, val):
        assert 0 <= x < self.width
        assert 0 <= y < self.height
        assert val in (None, IMPASSABLE, UNREACHABLE) or (isinstance(val, int) and val >= 0)
        self.data[x + (y * self.width)] = val

    def dump(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.valueAt(x, y), end=" ")
            print()

    def neighborsOf(self, x, y):
        """Given an x,y location, returns an iterator of (x,y) pairs of locations adjacent to it.
        Would always return 4 pairs EXCEPT that it doesn't return entries that are outside of
        the bounds."""
        if y > 0:
            yield (x, y-1)
        if y + 2 < self.height:
            yield (x, y+1)
        if x > 0:
            yield (x-1, y)
        if x +2 < self.width:
            yield (x+1, y)

    def numericNeighborsOf(self, x, y):
        """Given an x,y location, this returns an iterator of values in neighboring locations
        which contain numbers. If no neighbors contain a number, this will return no values."""
        for neighborX, neighborY in self.neighborsOf(x, y):
            neighborVal = self.valueAt(neighborX, neighborY)
            if neighborVal not in (None, IMPASSABLE, UNREACHABLE):
                assert isinstance(neighborVal, int) and neighborVal >= 0
                yield neighborVal

    def singlePassPopulateValues(self):
        """Performs a single pass of populating values. Returns the number of cells updated."""
        numUpdates = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.valueAt(x, y) is None:
                    # Try to populate it!
                    lowestNeighbor = min(self.numericNeighborsOf(x, y), default=None)
                    if lowestNeighbor is not None:
                        self.setValueAt(x, y, lowestNeighbor + 1)
                        numUpdates += 1
        return numUpdates

    def setNoneToUnreachable(self):
        """Simply sets all values in the DijkstraMap that are None to UNREACHABLE."""
        for y in range(self.height):
            for x in range(self.width):
                if self.valueAt(x, y) is None:
                    self.setValueAt(x, y, UNREACHABLE)

    def populateValues(self):
        """When this is called, it will iterate over the map until it has managed to
        replace all None values with one of the other valid values."""
        numUpdates = 1 # start with a dummy non-zero value
        while numUpdates: # loop until there are no updates
            numUpdates = self.singlePassPopulateValues()
        self.setNoneToUnreachable()




class Brain:
    """The abstract parent class of all Brain implementations."""

    def getAlignment(self):
        raise NotImplementedError()

    def takeOneAction(self, mobile, currentTime, world, screenChanges):
        """This is called when it is time for the mobile to take one action."""
        raise NotImplementedError()

    def neighboringCells(self, room, position):
        """Returns a list of ((deltaX, deltaY), cell) adjacent to the given position (will not include
        any cells that are beyond the edges of the room)."""
        result = []
        x0,y0 = position
        for deltaX, deltaY in [(-1,0), (1,0), (0,-1), (0,1)]:
            x,y = x0+deltaX, y0+deltaY
            if 0 <= x < room.width and 0 <= y < room.height:
                result.append( ((deltaX, deltaY), room.cellAt(x,y)) )
        return result

    def randomMove(self, mobile, currentTime, world, screenChanges):
        """Move randomly in some direction. It's a useful default action."""
        randomNumber = random.randrange(4)
        if randomNumber == 0:
            mobile.moveNorth(currentTime, world, screenChanges)
        elif randomNumber == 1:
            mobile.moveSouth(currentTime, world, screenChanges)
        elif randomNumber == 2:
            mobile.moveEast(currentTime, world, screenChanges)
        else:
            mobile.moveWest(currentTime, world, screenChanges)



class PlayerBrain(Brain):
    """The kind that players have. It isn't used."""

    def getAlignment(self):
        return Alignment.FRIENDLY



class RandomBrain(Brain):
    """A Brain that simply attempts to step in a random direction each turn."""

    def getAlignment(self):
        return Alignment.NEUTRAL

    def takeOneAction(self, mobile, currentTime, world, screenChanges):
        self.randomMove(mobile, currentTime, world, screenChanges)



class AgressiveBrain(Brain):
    """A brain that attempts to attack any ally it detects, and wanders randomly
    otherwise."""

    def getAlignment(self):
        return Alignment.UNFRIENDLY

    def takeOneAction(self, mobile, currentTime, world, screenChanges):
        neighboringAllies = []
        for deltas, neighborCell in self.neighboringCells(mobile.room, mobile.position):
            for thing in neighborCell.things:
                if isinstance(thing, Mobile) and thing.brain.getAlignment() == Alignment.FRIENDLY:
                    neighboringAllies.append((deltas, thing))
        if neighboringAllies:
            (deltas, ally) = random.choice(neighboringAllies)
            if deltas == (-1,0):
                mobile.moveWest(currentTime, world, screenChanges)
            elif deltas == (1,0):
                mobile.moveEast(currentTime, world, screenChanges)
            elif deltas == (0,1):
                mobile.moveSouth(currentTime, world, screenChanges)
            elif deltas == (0,-1):
                mobile.moveNorth(currentTime, world, screenChanges)
            else:
                assert False # Invalid value for deltas
        else:
            self.randomMove(mobile, currentTime, world, screenChanges)



