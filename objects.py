from kindsofthing import Region, Thing, Wall, Door, Trap, Item, Weapon
from mobile import Mobile

defaultRegion = Region()

class BrickWall(Wall):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/wall-1')

class InnerSecretDoor(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/wall-1')

class Dirt(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/grey_tile')

class StairsDown(Door):
    def __init__(self, destination):
        super().__init__(defaultRegion, 'drawntiles64/stairs-down', destination)

class Chest(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/chest2')

class WoodenDoor(Door):
    def __init__(self, destination):
        super().__init__(defaultRegion, 'drawntiles64/doorway-1', destination,
                         soundEffectName="foundassets/freesound.org/364922__mattix__door-opened")

class InnerDoor(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/doorway-1')
        self.soundEffectId = defaultRegion.soundLibrary.idByName(
            "foundassets/freesound.org/364922__mattix__door-opened")
    def doEnter(self, mobile, world, screenChanges):
        super().doEnter(mobile, world, screenChanges)
        screenChanges.roomPlaySound(mobile.room, self.soundEffectId)

class GiantBee(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/angry-bee', 11, inventory=[Sting()])
        
class MouseMan(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/mouseman',
                         maxHealth=3,
                         inventory=[Bite()])

class SnakeTrap(Trap):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/green-snake')

class BluePotion(Item):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/potion-blue")

class Sword(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/sword", 2,
                         "foundassets/freesound.org/348112__mattix__crunch")

class Spear(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/spear", 3,
                         "foundassets/freesound.org/348112__mattix__crunch")

class Wand(Item):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/wand")

class Bite(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/transparent", 2,
                         "foundassets/freesound.org/348112__mattix__crunch")

class ViciousHorns(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/transparent", 3,
                         "foundassets/freesound.org/348112__mattix__crunch")

class Minotar(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/mouseman",
                         maxHealth=12,
                         inventory=[ViciousHorns()])
class Sting(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/transparent", 3,
                         "foundassets/freesound.org/365658__mattix__bird-thrush-nightingale-01w")

class Witch(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/witch", maxHealth=8)