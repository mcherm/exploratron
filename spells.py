#
# Spells are named effects that can take place. They can be tied to
# a wand to be cast or to other kinds of things.
#


class Spell():
    def __init__(self, region, spellSoundEffectName):
        self._spellSoundEffectId = region.soundLibrary.idByName(spellSoundEffectName)

    def hasBeenCast(self, room, screenChanges):
        """Contains common behavior of ALL spells when they are cast."""
        screenChanges.roomPlaySound(room, self.getSpellSoundEffectId())

    def getSpellSoundEffectId(self):
        """This is a method so subclasses can choose to have different sounds under
        different circumstances if they want to."""
        return self._spellSoundEffectId


class SingleTargetSpell(Spell):
    """A spell that affects a single Mobile."""
    def cast(self, targetMobile, world, screenChanges):
        """Attempts to apply the spell effect of the spell. If it succeeds, this
        returns True, if it cannot be cast in this circumstance it returns False."""
        raise NotImplementedError() # subclasses should override this


class HealingSpell(SingleTargetSpell):
    """Heals a specified number of health."""
    def __init__(self, region, healthHealed):
        """Create a healing spell that heals up to healthHealed points of damage."""
        super().__init__(region, spellSoundEffectName="365658__mattix__bird-thrush-nightingale-01")
        self.healthHealed = healthHealed

    def cast(self, targetMobile, world, screenChanges):
        targetMobile.stats.health = min(
            targetMobile.stats.health + self.healthHealed,
            targetMobile.stats.maxHealth)
        self.hasBeenCast(targetMobile.room, screenChanges)
        return True


class TeleportSpell(SingleTargetSpell):
    """A spell that teleports the target to a pre-specified location."""
    def __init__(self, region, destination):
        """destination is a Location which specifies where to teleport to."""
        super().__init__(region, spellSoundEffectName="368682__mattix__knock-knock-02")
        self.destination = destination

    def cast(self, targetMobile, world, screenChanges):
        startingRoom = targetMobile.room
        targetMobile.goToLocation(self.destination, world, screenChanges)
        endingRoom = targetMobile.room
        # Make the spell effects visible/audible in BOTH locations
        self.hasBeenCast(startingRoom, screenChanges)
        self.hasBeenCast(endingRoom, screenChanges)
