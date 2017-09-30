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
dr5 = WoodenDoor(Location(4, (1,1)))
dr6 = WoodenDoor(Location(3,(6,6)))
#dr7 = WoodenDoor(Location(
sdr = InnerSecretDoor()


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
        (1,2): BluePotion(),
    },
    {
        (5,1): GiantBee(),
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
        (7,4): SnakeTrap(),
        (10,1): Wand(),
    },
    {
        (8,8): MouseMan(),
    }
)

room3 = Room(
    [
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw],
        [dr4, drt, drt, drt, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, drt, sdr, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, drt, bkw, drt, dr5],
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw],
    ],

        
)

room4 = Room(
    [
        [bkw,bkw,bkw,bkw,bkw,bkw,bkw,bkw,bkw,bkw,bkw],
        [dr6,drt,drt,drt,drt,drt,drt,drt,drt,drt,bkw],
        [bkw,bkw,drt,bkw,bkw,bkw,bkw,drt,bkw,bkw,bkw],
        [bkw,drt,drt,drt,drt,drt,bkw,drt,bkw,bkw,bkw],
        [bkw,drt,bkw,bkw,bkw,drt,bkw,drt,drt,bkw,bkw],
        [bkw,drt,bkw,drt,drt,drt,drt,bkw,drt,drt,bkw],
        [bkw,drt,bkw,drt,bkw,bkw,drt,bkw,bkw,drt,bkw],
        [bkw,drt,bkw,drt,bkw,bkw,drt,bkw,drt,drt,bkw],
        [bkw,bkw,bkw,bkw,bkw,drt,drt,bkw,drt,bkw,bkw],
        [bkw,drt,drt,drt,drt,drt,bkw,bkw,bkw,bkw,bkw],
        [bkw,drt,bkw,bkw,drt,bkw,drt,drt,drt,bkw,bkw],
        [bkw,drt,drt,bkw,drt,bkw,drt,bkw,bkw,bkw,bkw],
        [bkw,bkw,drt,bkw,drt,drt,drt,drt,drt,drt,bkw],
        [bkw,bkw,bkw,bkw,bkw,bkw,bkw,bkw,bkw,bkw,bkw],
    ],
    {
        (1,7): Sword(),
        (8,8): Spear(),
    }
)




rooms = [room0, room1, room2, room3, room4]
