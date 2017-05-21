from objects import *
from gamecomponents import *


room0Layout = [
    [ [BrickWall()], [BrickWall()], [WoodenDoor(Location(1, (2,3)))], [BrickWall()], [BrickWall()], [BrickWall()], [BrickWall()] ], 
    [ [BrickWall()], [Dirt(), Chest()], [Dirt()], [Dirt()], [Dirt()], [Dirt(), Mobile(12)], [BrickWall()], ],
    [ [BrickWall()], [Dirt()], [Dirt()], [StairsDown()], [Dirt()], [Dirt()], [BrickWall()], ],
    [ [BrickWall()], [Dirt()], [Dirt()], [Dirt()], [Dirt()], [Dirt(), Chest()], [BrickWall()], ],
    [ [BrickWall()], [BrickWall()], [BrickWall()], [BrickWall()], [BrickWall()], [BrickWall()], [BrickWall()], ],
]

room1Layout = [
    [ [BrickWall()], [BrickWall()], [BrickWall()],                    [BrickWall()], [BrickWall()] ],
    [ [BrickWall()], [Dirt()],      [Dirt()],                         [Dirt()],      [BrickWall()] ],
    [ [BrickWall()], [Dirt()],      [Dirt()],                         [Dirt()],      [BrickWall()] ],
    [ [BrickWall()], [BrickWall()], [WoodenDoor(Location(0, (2,0)))], [BrickWall()], [BrickWall()] ],
]


def makeRoom(layout):
    grid = Grid(len(layout[0]), len(layout))
    print(f"Grid size: {grid.__dict__}") # FIXME: Remove
    for y, row in enumerate(layout):
        for x, cellContents in enumerate(row):
            for thing in cellContents:
                grid.cellAt(x,y).addThing(thing)
    return grid


rooms = [ makeRoom(room) for room in [room0Layout, room1Layout]]

