#
# This contains the logic for a "brain" -- the AI component that decides how a
# mobile will behave.
#
# Most brains keep some state, so each brain instance is used by only a single
# mobile. However, the brain doesn't keep a reference to the mobile (to avoid
# ownership loops).
#

import random


class Brain:
    """The abstract parent class of all Brain implementations."""
    def takeOneAction(self, mobile, currentTime, world, screenChanges):
        """This is called when it is time for the mobile to take one action."""
        raise NotImplementedError()


class PlayerBrain(Brain):
    """The kind that players have. It isn't used."""
    pass


class RandomBrain(Brain):
    """A Brain that simply attempts to step in a random direction each turn."""
    def takeOneAction(self, mobile, currentTime, world, screenChanges):
        randomNumber = random.randrange(4)
        if randomNumber == 0:
            mobile.moveNorth(currentTime, world, screenChanges)
        elif randomNumber == 1:
            mobile.moveSouth(currentTime, world, screenChanges)
        elif randomNumber == 2:
            mobile.moveEast(currentTime, world, screenChanges)
        else:
            mobile.moveWest(currentTime, world, screenChanges)

