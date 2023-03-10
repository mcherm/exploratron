
from images import Region
from spells import SingleTargetSpell
from infotext import InfoText



class Thing:
    """Represents any kind of thing in the world."""
    def __init__(self, region, tileName, displayName):
        assert isinstance(region, Region)
        assert isinstance(tileName, str)
        self.tileId = region.imageLibrary.idByName(tileName)
        self.displayName = displayName
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
    def __init__(self, region, tileName, displayName, destination, soundEffectName=None):
        super().__init__(region, tileName, displayName)
        self.destination = destination
        self.soundEffectId = None if soundEffectName is None else region.soundLibrary.idByName(soundEffectName)
    def doEnter(self, mobile, world, screenChanges):
        mobile.goToLocation(self.destination, world, screenChanges)
        if self.soundEffectId is not None:
            screenChanges.roomPlaySound(mobile.room, self.soundEffectId)

class Sign(Thing):
    """A thing that displays a message when you enter it."""
    def __init__(self, region, tileName, displayName, text):
        """Create a new sign with the string messageText."""
        super().__init__(region, tileName, displayName)
        self.infoText = InfoText(text)
    def doEnter(self, mobile, world, screenChanges):
        if mobile.isPlayer():
            screenChanges.showInfoText(mobile, self.infoText)

class Trap(Thing):
    """A thing that makes you take damage"""
    def doEnter(self, mobile, world, screenChanges):
        mobile.takeDamage(1, screenChanges)
        

class Item(Thing):
    """A parent class for any Thing that can be put in an inventory."""
    def uniqueId(self):
        """All Items have a unique ID used to identify them when managing inventory
        remotely on the client."""
        return id(self)
    def featureCode(self):
        """For describing items so they can be manipulated on the client, there are
        a few properties that need to be available clientside. Those are isWeapon (boolean),
        and isWand (boolean). Currently, no item can be both. This method returns a code
        string that indicates what features a weapon has. The current codes are: "N"
        (normal item), "W" (weapon), "S" (wand)."""
        return "N"


class Weapon(Item):
    def __init__(self, region, tileName, displayName, damage, hitSoundEffectName):
        super().__init__(region, tileName, displayName)
        self.damage = damage
        self.hitSoundEffectId = region.soundLibrary.idByName(hitSoundEffectName)
    def getHitSoundEffectId(self):
        """This returns the ID of the sound effect that should be played
        when this weapon is used to successfully attack someone."""
        return self.hitSoundEffectId
    def featureCode(self):
        return "W"


class Wand(Item):
    def __init__(self, region, displayName, manaCost, spell, tileName="wand"):
        super().__init__(region, tileName, displayName)
        self.manaCost = manaCost
        self.spell = spell
    def cast(self, caster, world, screenChanges):
        """Attempts to invoke the spell effect of the wand. Returns True if the cast
        was successful, and False if it fails."""
        if caster.stats.mana < self.manaCost:
            return False
        else:
            caster.stats.mana -= self.manaCost  # spend the mana even if the spell fails
            self.activateSpell(caster, world, screenChanges)
    def activateSpell(self, caster, world, screenChanges):
        raise NotImplementedError # intended to be overridden by subclasses
    def featureCode(self):
        return "S"


class SelfOnlyWand(Wand):
    """A wand with a spell that affects the caster. No aiming needed."""
    def __init__(self, region, displayName, manaCost, spell, tileName="wand"):
        assert isinstance(spell, SingleTargetSpell)
        super().__init__(region, displayName, manaCost, spell, tileName)

    def activateSpell(self, caster, world, screenChanges):
        """This is how you activate a SingleTarget spell that affects the caster."""
        self.spell.cast(caster, world, screenChanges)


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

