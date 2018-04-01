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
        super().__init__(defaultRegion, 'drawntiles64/dirt-1')

class StairsDown(Door):
    def __init__(self, destination):
        super().__init__(defaultRegion, 'drawntiles64/stairs-down', destination)

class Chest(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/chest2')

class WoodenDoor(Door):
    def __init__(self, destination):
        super().__init__(defaultRegion, 'drawntiles64/doorway-1', destination)

class InnerDoor(Thing):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/doorway-1')

class GiantBee(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/angry-bee', 11)
        
class MouseMan(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/mouseman', 3)

class SnakeTrap(Trap):
    def __init__(self):
        super().__init__(defaultRegion, 'drawntiles64/green-snake')

class BluePotion(Item):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/potion-blue")

class Sword(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/sword", 2)

class Spear(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/spear", 3)

class Wand(Item):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/wand")

class ViciousHorns(Weapon):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/spear", 2) # Should be invisible tile

class Minotar(Mobile):
    def __init__(self):
        super().__init__(defaultRegion, "drawntiles64/mouseman",
                         health=12,
                         inventory=[ViciousHorns()])
