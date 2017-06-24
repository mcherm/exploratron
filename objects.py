from kindsofthing import *


class BrickWall(Wall):
    def __init__(self):
        Wall.__init__(self, 7)

class Dirt(Thing):
    def __init__(self):
        Thing.__init__(self, 0)

class StairsDown(Door):
    def __init__(self, destination):
        Door.__init__(self, 5, destination)

class Chest(Thing):
    def __init__(self):
        Thing.__init__(self, 6)

class WoodenDoor(Door):
    def __init__(self, destination):
        Door.__init__(self, 8, destination)

class InnerDoor(Thing):
    def __init__(self):
        Thing.__init__(self, 8)

class GiantBee(Mobile):
    def __init__(self):
        super().__init__(12)
        
class MouseMan(Mobile):
    def __init__(self):
        super().__init__(13)
