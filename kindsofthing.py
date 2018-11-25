
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
    def __init__(self, region, tileName, destination, soundEffectName=None):
        super().__init__(region, tileName)
        self.destination = destination
        self.soundEffectId = None if soundEffectName is None else region.soundLibrary.idByName(soundEffectName)
    def doEnter(self, mobile, world, screenChanges):
        mobile.goToLocation(self.destination, world, screenChanges)
        if self.soundEffectId is not None:
            screenChanges.roomPlaySound(mobile.room, self.soundEffectId)


class Trap(Thing):
    """a thing that maks you take damage"""
    def doEnter(self, mobile, world, screenChanges):
        mobile.takeDamage(1)
        

class Item(Thing):
    """A parent class for any Thing that can be put in an inventory."""
    pass


class Weapon(Item):
    def __init__(self, region, tileName, damage, hitSoundEffectName):
        super().__init__(region, tileName)
        self.damage = damage
        self.hitSoundEffectId = region.soundLibrary.idByName(hitSoundEffectName)
    def getHitSoundEffectId(self):
        """This returns the ID of the sound effect that should be played
        when this weapon is used to successfully attack someone."""
        return self.hitSoundEffectId


class Wand(Item):
    def __init__(self, region, manaCost, spellSoundEffectName, tileName="wand"):
        super().__init__(region, tileName)
        self.manaCost = manaCost
        self.spellSoundEffectId = region.soundLibrary.idByName(spellSoundEffectName)
    def getSpellSoundEffectId(self):
        """This returns the ID of the sound effect that should be played
        when this wand is used."""
        return self.spellSoundEffectId
    def cast(self, caster, world, screenChanges):
        """Common behavior of all wands when cast. Returns True if the cast
        was successful, and False if it fails."""
        if caster.stats.mana < self.manaCost:
            return False
        else:
            caster.stats.mana -= self.manaCost
            screenChanges.roomPlaySound(caster.room, self.getSpellSoundEffectId())
            self.takeEffect(caster, world, screenChanges)
    def takeEffect(self, caster, world, screenChanges):
        """Specific wands will override this to perform an action."""
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

