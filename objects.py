from kindsofthing import *


class BrickWall(Wall):
    def __init__(self):
        Wall.__init__(self, 7)

class Dirt(Thing):
    def __init__(self):
        Thing.__init__(self, 0)

class StairsDown(Thing):
    def __init__(self):
        Thing.__init__(self, 5)

class Chest(Thing):
    def __init__(self):
        Thing.__init__(self, 6)
