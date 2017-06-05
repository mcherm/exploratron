from objects import *
from gamecomponents import *



drt = Dirt()
bkw = BrickWall()
std = StairsDown()
dr1 = WoodenDoor(Location(1, (2,3)))
dr2 = WoodenDoor(Location(0, (2,0)))


room0 = Room(
    [
        [bkw, bkw, dr1, bkw, bkw, bkw, bkw],
        [bkw, drt, drt, drt, drt, drt, bkw],
        [bkw, drt, drt, std, drt, drt, bkw],
        [bkw, drt, drt, drt, drt, drt, bkw],
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw],
    ],
    {
        (1,1): Chest(),
        (5,3): Chest(),
    },
    {
        (5,1): Mobile(12)
    }
)



room1 = Room(
    [
        [bkw, bkw, bkw, bkw, bkw],
        [bkw, drt, drt, drt, bkw],
        [bkw, drt, drt, drt, bkw],
        [bkw, bkw, dr2, bkw, bkw],
    ]
)


rooms = [room0, room1]
