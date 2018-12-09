from kindsofthing import Region, Thing, Wall, Door, Trap, Item, Weapon, SelfOnlyWand
from mobile import Mobile
from brain import RandomBrain, AgressiveBrain
from spells import HealingSpell, TeleportSpell


defaultRegion = Region()

class BrickWall(Wall):
    def __init__(self):
        super().__init__(defaultRegion, 'wall-1')

class InnerSecretDoor(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'wall-1')

class Dirt(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'grey_tile')

class StairsDown(Door):
    def __init__(self, destination):
        super().__init__(defaultRegion, 'stairs-down', destination)

class Chest(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'chest2')

class WoodenDoor(Door):
    def __init__(self, destination):
        super().__init__(defaultRegion, 'doorway-1', destination,
                         soundEffectName="364922__mattix__door-opened")

class InnerDoor(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'doorway-1')
        self.soundEffectId = defaultRegion.soundLibrary.idByName(
            "364922__mattix__door-opened")
    def doEnter(self, mobile, world, screenChanges):
        super().doEnter(mobile, world, screenChanges)
        screenChanges.roomPlaySound(mobile.room, self.soundEffectId)

class GiantBee(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, 'angry-bee', 11, 1, RandomBrain, inventory=[Sting()])
        
class MouseMan(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, 'mouseman',
                         maxHealth=3,
                         maxMana=5,
                         brainType=RandomBrain,
                         inventory=[Bite()])

class SnakeTrap(Trap):
    def __init__(self):
        super().__init__(defaultRegion, 'green-snake')

class BluePotion(Item):
    def __init__(self):
        super().__init__(defaultRegion, "potion-blue")

class Sword(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "sword", 3,
                         "348112__mattix__crunch")

class Spear(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "spear", 2,
                         "348112__mattix__crunch")

class Bite(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "transparent", 2,
                         "348112__mattix__crunch")

class ViciousHorns(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "transparent", 1,
                         "348112__mattix__crunch")

class Minotar(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, "mouseman",
                         maxHealth=12,
                         maxMana=5,
                         brainType=AgressiveBrain,
                         inventory=[ViciousHorns()])
class Sting(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "transparent", 3,
                         "365658__mattix__bird-thrush-nightingale-01")

class Witch(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, "witch", maxHealth=8, maxMana=19, brainType=RandomBrain)


class HealingWand(SelfOnlyWand):
    def __init__(self):
        super().__init__(defaultRegion, manaCost=6,
                         spell=HealingSpell(defaultRegion, healthHealed=4))

class TeleportWand(SelfOnlyWand):
    def __init__(self, destination):
        super().__init__(defaultRegion, manaCost=8,
                         spell=TeleportSpell(defaultRegion, destination))
