from kindsofthing import Region, Thing, Wall, Door, Trap, Item, Weapon, SelfOnlyWand, Sign
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

class Grass(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'grassBlock')

class StairsDown(Door):
    def __init__(self, destination):
        super().__init__(defaultRegion, 'stairs-down', destination)

class Chest(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'chest2')

class Tree(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'Tree')

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

class PublicSign(Sign):
    def __init__(self, messageText):
        super().__init__(defaultRegion, "sign", messageText)

class GiantBee(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, 'angry-bee', 11, 1, RandomBrain, inventory=[Sting(), BluePotion()])
        
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

class FuzzAttack(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "transparent", .5,
                         "348112__mattix__crunch")

class Minotar(Mobile):
    def __init__(self, extraInventory=[]):
        super().__init__(defaultRegion, "minotaur",
                         maxHealth=12,
                         maxMana=5,
                         brainType=AgressiveBrain,
                         inventory=[ViciousHorns()] + extraInventory)
                                    self.stats.speed = 3

class RedFuzzball(Mobile):
    def __init__(self, extraInventory=[]):
        super().__init__(defaultRegion, "redFuzzball",
                         maxHealth=3,
                         maxMana=5,
                         brainType=AgressiveBrain,
                         inventory=[ViciousHorns()])

class OrangeFuzzball(Mobile):
    def __init__(self, extraInventory=[]):
        super().__init__(defaultRegion, "orangeFuzzball",
                            maxHealth=3,
                            maxMana=5,
                            brainType=AgressiveBrain,
                            inventory=[FuzzAttack()])

class GreenFuzzball(Mobile):
    def __init__(self, extraInventory=[]):
        super().__init__(defaultRegion, "greenFuzzball",
                            maxHealth=3,
                            maxMana=5,
                            brainType=AgressiveBrain,
                            inventory=[FuzzAttack()])

class BleuFuzzball(Mobile):
    def __init__(self, extraInventory=[]):
        super().__init__(defaultRegion, "bleuFuzzball",
                            maxHealth=3,
                            maxMana=5,
                            brainType=AgressiveBrain,
                            inventory=[FuzzAttack()])

class BlueFuzzball(Mobile):
    def __init__(self, extraInventory=[]):
        super().__init__(defaultRegion, "blueFuzzball",
                            maxHealth=3,
                            maxMana=5,
                            brainType=AgressiveBrain,
                            inventory=[FuzzAttack()])

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
