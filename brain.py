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



Alignment = Enum('Alignment', 'FRIENDLY NEUTRAL UNFRIENDLY')


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



