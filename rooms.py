from objects import *
from gamecomponents import *



drt = Dirt()
bkw = BrickWall()
idr = InnerDoor()
st1 = StairsDown(Location(2, (2,3)))
st2 = StairsDown(Location(0, (3,2)))
dr1 = WoodenDoor(Location(1, (2,3)))
dr2 = WoodenDoor(Location(0, (2,0)))
dr3 = WoodenDoor(Location(3, (0,1)))
dr4 = WoodenDoor(Location(2, (11,1)))


room0 = Room(
    [
        [bkw, bkw, dr1, bkw, bkw, bkw, bkw],
        [bkw, drt, drt, drt, drt, drt, bkw],
        [bkw, drt, drt, st1, drt, drt, bkw],
        [bkw, drt, drt, drt, drt, drt, bkw],
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw],
    ],
    {
        (1,1): Chest(),
        (5,3): Chest(),
    },
    {
        (5,1): Mobile(12),
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


room2 = Room(
    [
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, dr3],
        [bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, bkw],
        [bkw, drt, st2, drt, drt, bkw, drt, drt, drt, drt, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, bkw],
        [bkw, drt, drt, drt, drt, idr, drt, drt, drt, drt, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, bkw],
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw],
    ],
    {
        (9,3): Chest(),
    },
    {
        (8,8): Mobile(12),
    }
)

room3 = Room(
    [
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw],
        [dr4, drt, drt, drt, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, drt, drt, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, bkw],
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw],
    ],

        
)



rooms = [room0, room1, room2, room3]
