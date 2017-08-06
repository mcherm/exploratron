from kindsofthing import Region, Thing, Wall, Door, Trap, Mobile

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

