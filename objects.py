from kindsofthing import Region, Thing, Wall, Door, Trap, Item, Weapon, SelfOnlyWand, Sign
from mobile import Mobile
from brain import RandomBrain, AgressiveBrain
from spells import HealingSpell, TeleportSpell


defaultRegion = Region()

class BrickWall(Wall):
    def __init__(self):
        super().__init__(defaultRegion, 'wall-1', "brick wall")

class InnerSecretDoor(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'wall-1', "secret door")

class Dirt(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'grey_tile', "dirt")

class Grass(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'grassBlock', "grass")

class StairsDown(Door):
    def __init__(self, destination):
        super().__init__(defaultRegion, 'stairs-down', "stairs", destination)

class Chest(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'chest2', "chest")

class Tree(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'Tree', "tree")

class WoodenDoor(Door):
    def __init__(self, destination):
        super().__init__(defaultRegion, 'doorway-1', "wooden door", destination,
                         soundEffectName="364922__mattix__door-opened")

class InnerDoor(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'doorway-1', "door")
        self.soundEffectId = defaultRegion.soundLibrary.idByName(
            "364922__mattix__door-opened")
    def doEnter(self, mobile, world, screenChanges):
        super().doEnter(mobile, world, screenChanges)
        screenChanges.roomPlaySound(mobile.room, self.soundEffectId)

class PublicSign(Sign):
    def __init__(self, messageText):
        super().__init__(defaultRegion, "sign", "sign", messageText)

class GiantBee(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, 'angry-bee', "giant bee", 11, 1, RandomBrain, inventory=[Sting(), BluePotion()])
        
class MouseMan(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, 'mouseman', "mouse man",
                         maxHealth=3,
                         maxMana=5,
                         brainType=RandomBrain,
                         inventory=[Bite()])

class SnakeTrap(Trap):
    def __init__(self):
        super().__init__(defaultRegion, 'green-snake', "snake trap")

class BluePotion(Item):
    def __init__(self):
        super().__init__(defaultRegion, "potion-blue", "potion of ____")

class Sword(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "sword", "sword", 3,
                         "348112__mattix__crunch")

class Spear(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "spear", "spear", 2,
                         "348112__mattix__crunch")

class Bite(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "transparent", "teeth", 2,
                         "348112__mattix__crunch")

class ViciousHorns(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "transparent", "vicious horns", 1,
                         "348112__mattix__crunch")

class FuzzAttack(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "transparent", "fuzz ball fangs", .5,
                         "348112__mattix__crunch")

class Minotar(Mobile):
    def __init__(self, extraInventory=[]):
        super().__init__(defaultRegion, "minotaur", "fuming minotaur",
                         maxHealth=12,
                         maxMana=5,
                         brainType=AgressiveBrain,
                         inventory=[ViciousHorns()] + extraInventory)
        self.stats.speed = 3

class RedFuzzball(Mobile):
    def __init__(self, extraInventory=[]):
        super().__init__(defaultRegion, "redFuzzball", "Cherry Fuzz",
                         maxHealth=3,
                         maxMana=5,
                         brainType=AgressiveBrain,
                         inventory=[ViciousHorns()] )
        self.stats.speed = 1

class OrangeFuzzball(Mobile):
    def __init__(self, extraInventory=[]):
        super().__init__(defaultRegion, "orangeFuzzball","Orange Fuzz",
                            maxHealth=3,
                            maxMana=5,
                            brainType=AgressiveBrain,
                            inventory=[FuzzAttack()])
        self.stats.speed = 1


class GreenFuzzball(Mobile):
    def __init__(self, extraInventory=[]):
        super().__init__(defaultRegion, "greenFuzzball", "Mint Fuzz",
                            maxHealth=3,
                            maxMana=5,
                            brainType=AgressiveBrain,
                            inventory=[FuzzAttack()])
        self.stats.speed = 1

class BleuFuzzball(Mobile):
    def __init__(self, extraInventory=[]):
        super().__init__(defaultRegion, "bleuFuzzball", "Blueberry Fuzz",
                            maxHealth=3,
                            maxMana=5,
                            brainType=AgressiveBrain,
                            inventory=[FuzzAttack()])
        self.stats.speed = 1

class BlueFuzzball(Mobile):
    def __init__(self, extraInventory=[]):
        super().__init__(defaultRegion, "blueFuzzball", "Bluebear Fuzz",
                            maxHealth=3,
                            maxMana=5,
                            brainType=AgressiveBrain,
                            inventory=[FuzzAttack()])
        self.stats.speed = 1

class Sting(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "transparent", "bee stinger", 3,
                         "365658__mattix__bird-thrush-nightingale-01")

class Witch(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, "witch", "The Wicked Witch of the Feast", maxHealth=8, maxMana=19, brainType=RandomBrain)


class HealingWand(SelfOnlyWand):
    def __init__(self):
        super().__init__(defaultRegion, "Medicinal wand", manaCost=6,
                         spell=HealingSpell(defaultRegion, healthHealed=4))

class TeleportWand(SelfOnlyWand):
    def __init__(self, destination):
        super().__init__(defaultRegion, "Wand of teleportation", manaCost=8,
                         spell=TeleportSpell(defaultRegion, destination))


#people feel free to change the names and make them more interesting#