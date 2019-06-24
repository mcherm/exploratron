from objects import *
from gamecomponents import *



drt = Dirt()
bkw = BrickWall()
idr = InnerDoor()
grs = Grass()
st1 = StairsDown(Location(2, (2,3)))
st2 = StairsDown(Location(0, (3,2)))
dr1 = WoodenDoor(Location(1, (2,3)))
dr2 = WoodenDoor(Location(0, (2,0)))
dr3 = WoodenDoor(Location(3, (0,1)))
dr4 = WoodenDoor(Location(2, (11,1)))
dr5 = WoodenDoor(Location(4, (1,1)))
dr6 = WoodenDoor(Location(3, (6,6)))
dr7 = WoodenDoor(Location(5, (0,1)))
dr8 = WoodenDoor(Location(6, (0,1)))
dr9 = WoodenDoor(Location(5, (6,6)))
d10 = WoodenDoor(Location(4, (10,12)))
d11 = WoodenDoor(Location(7, (6,10)))
d12 = WoodenDoor(Location(8, (15,19)))
d14 = WoodenDoor(Location(2, (1,9)))
d13 = WoodenDoor(Location(9, (1,0)))
sdr = InnerSecretDoor()


room0 = Room(
    [
        [bkw, bkw, dr1, bkw, bkw, bkw, bkw],
        [bkw, drt, drt, drt, drt, drt, bkw],
        [bkw, drt, drt, st1, drt, drt, bkw],
        [bkw, drt, drt, drt, drt, drt, d12],
        [bkw, bkw, bkw, bkw, d11, bkw, bkw],
    ],
    {
        (1,1): Chest(),
        (5,3): Chest(),
        (1,2): BluePotion(),
        (1,2): [Spear(), BluePotion(), Sword(), HealingWand(), Spear()],
        (5,3): PublicSign("Go East for Minotaur\n\nBeware - the only escape is\nto defeat the beast."),
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
        [bkw, d13, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw],
    ],
    {
        (9,3): Chest(),
        (7,4): SnakeTrap(),
        (10,1): HealingWand(),
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
        [bkw,bkw,drt,bkw,drt,drt,drt,drt,drt,drt,dr7],
        [bkw,bkw,bkw,bkw,bkw,bkw,bkw,bkw,bkw,bkw,bkw],
    ],
    {
        (1,7): Sword(),
        (8,8): Spear(),
    },
    {
        (1, 1): Witch(),
    }
)


room5 = Room(
    [
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw],
        [d10, drt, drt, drt, drt, drt, bkw],
        [bkw, bkw, drt, bkw, bkw, drt, bkw],
        [bkw, bkw, drt, drt, drt, drt, bkw],
        [bkw, bkw, drt, bkw, bkw, drt, bkw],
        [bkw, bkw, drt, drt, drt, bkw, bkw],
        [bkw, drt, drt, bkw, drt, drt, dr8],
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw],
    ],
    {
        (4,5): HealingWand(),
    }
)


room6 = Room(
    [
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw],
        [dr9, drt, drt, drt, drt, drt, bkw],
        [bkw, drt, bkw, bkw, bkw, drt, bkw],
        [bkw, drt, drt, bkw, drt, drt, bkw],
        [bkw, bkw, drt, bkw, bkw, drt, bkw],
        [bkw, bkw, drt, bkw, drt, drt, bkw],
        [bkw, bkw, drt, drt, bkw, bkw, bkw],
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw],
    ],
    {
        (4,5): SnakeTrap(),
    }
)


# The "combat room"
room7 = Room(
    [
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw, bkw, idr, bkw, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, idr, drt, bkw, drt, bkw],
        [bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw],
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw],
    ],
    {
        (9,3): Sword(),
        (3,17): Sword(),
        (13,3): TeleportWand(Location(1, (1,1))),
    },
    {
        (10,19): Minotar()
    }
)

room8 = Room(
    [
        [bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw],
        [bkw, drt, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, drt, drt, drt, drt, bkw, bkw, bkw, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, drt, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, drt, idr, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, drt, bkw, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, drt, bkw, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, drt, bkw, drt, drt, bkw, drt, drt, drt, drt, bkw, idr, bkw, bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, drt, bkw, drt, drt, bkw, drt, drt, drt, drt, bkw, drt, drt, bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, drt, bkw, drt, drt, bkw, bkw, bkw, idr, bkw, bkw, drt, drt, bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, drt, idr, drt, drt, bkw, drt, drt, drt, drt, bkw, bkw, idr, bkw, bkw, bkw, bkw, bkw, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, drt, bkw, drt, drt, bkw, drt, drt, drt, drt, idr, drt, drt, drt, idr, drt, drt, drt, bkw, bkw, bkw, bkw, bkw, idr, bkw, idr, bkw, bkw, idr],
        [bkw, drt, bkw, drt, bkw, drt, drt, idr, drt, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, bkw, drt, bkw, idr, bkw, bkw, bkw, bkw, bkw, idr, bkw],
        [bkw, drt, bkw, drt, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, idr, bkw, bkw, bkw, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, drt, drt, idr, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, bkw, bkw, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, idr, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, drt, drt, idr, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt],
        [bkw, drt, bkw, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, bkw, bkw, bkw, idr, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, drt],
        [bkw, drt, bkw, drt, drt, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, idr, bkw, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, drt],
        [bkw, drt, bkw, drt, drt, drt, drt, drt, drt, drt, idr, drt, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, drt],
        [bkw, bkw, bkw, drt, drt, drt, drt, drt, drt, drt, bkw, drt, drt, idr, drt, bkw, drt, idr, drt, drt, drt, drt, drt, drt, drt, drt, bkw, drt, drt, bkw, drt],
        [bkw, drt, drt, drt, bkw, bkw, bkw, bkw, bkw, bkw, bkw, idr, bkw, bkw, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, drt],
        [bkw, drt, bkw, drt, bkw, drt, drt, drt, drt, drt, bkw, drt, bkw, bkw, bkw, idr, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, drt, drt, drt, drt, bkw, drt],
        [drt, bkw, drt, drt, bkw, drt, drt, drt, drt, drt, bkw, drt, bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, bkw, drt, drt, drt, drt, bkw, drt],
        [drt, bkw, idr, bkw, bkw, bkw, bkw, bkw, idr, bkw, bkw, drt, bkw, bkw, bkw, bkw, drt, bkw, drt, drt, drt, drt, drt, drt, bkw, drt, drt, drt, drt, bkw, drt],
        [bkw, bkw, drt, drt, idr, drt, bkw, drt, drt, drt, drt, drt, idr, drt, drt, bkw, drt, bkw, idr, bkw, bkw, bkw, bkw, idr, bkw, bkw, bkw, bkw, drt, bkw, drt],
        [bkw, drt, drt, drt, bkw, drt, bkw, drt, drt, drt, drt, drt, bkw, drt, drt, bkw, drt, idr, drt, drt, drt, drt, bkw, drt, drt, drt, drt, bkw, drt, bkw, drt],
        [bkw, bkw, bkw, bkw, bkw, drt, bkw, drt, drt, drt, drt, drt, bkw, bkw, idr, bkw, bkw, bkw, bkw, bkw, idr, bkw, bkw, drt, drt, drt, drt, bkw, drt, bkw, drt],
        [bkw, drt, bkw, drt, drt, drt, idr, drt, drt, drt, drt, drt, bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, bkw, idr, bkw, drt],
        [bkw, drt, bkw, drt, bkw, bkw, bkw, drt, drt, drt, drt, drt, bkw, drt, bkw, bkw, bkw, bkw, drt, drt, drt, drt, bkw, drt, drt, drt, drt, bkw, drt, bkw, drt],
        [bkw, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, drt, drt, bkw, drt, bkw, drt, drt, idr, drt, drt, drt, drt, idr, drt, drt, drt, drt, bkw, drt, bkw, drt],
        [bkw, drt, bkw, drt, drt, drt, bkw, drt, drt, drt, drt, drt, bkw, drt, bkw, drt, drt, bkw, bkw, idr, bkw, idr, bkw, idr, bkw ,bkw, idr, bkw, idr, bkw, drt],
        [bkw, drt, bkw, bkw, bkw, bkw, bkw, bkw, bkw, sdr, bkw, bkw, bkw, drt, bkw, drt, drt, idr, drt, drt, bkw, drt, bkw, drt, bkw, bkw, drt, bkw, drt, bkw, drt],
        [bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, drt, bkw, drt, drt, bkw, drt, drt, bkw, drt, bkw, drt, bkw, bkw, drt, bkw, drt, bkw, drt],
        [bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, drt, bkw, bkw, bkw, bkw, bkw, bkw, bkw, drt, bkw, drt, bkw, bkw, drt, bkw, drt, bkw, drt],
        [bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, drt, drt, drt, bkw, drt, drt, drt, drt, drt, drt, bkw, drt],
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, bkw, drt],
    ],
    {
        (14, 18): SnakeTrap(),
        (16, 18): SnakeTrap(),
        (14, 20): SnakeTrap(),
        (28, 29): SnakeTrap(),
        ( 9, 29): Sword(),
    },
    {
        (20, 1): Minotar(extraInventory=[TeleportWand(Location(0, (2,1)))])
    }
)

room9 = Room(
    [
        [bkw, d14, bkw, bkw, bkw, bkw, bkw],
        [bkw, grs, grs, grs, grs, grs, bkw],
        [bkw, grs, grs, grs, grs, grs, bkw],
        [bkw, grs, grs, grs, grs, grs, bkw],
        [bkw, grs, grs, grs, grs, grs, bkw],
        [bkw, grs, grs, grs, grs, grs, bkw],
        [bkw, grs, grs, grs, grs, grs, bkw],
        [bkw, bkw, bkw, bkw, bkw, bkw, bkw],
    ],
    {
        (4,5): SnakeTrap(),
        (3, 4): Tree(),
    },
    {
        (5, 6): BlueFuzzball(),
        (5, 1): BleuFuzzball(),
        (5, 2): GreenFuzzball(),
        (5, 3): RedFuzzball(),
        (5, 4): OrangeFuzzball(),

#if you put them on the same square to start only one, the last one of the list appears, even with random brains.
    }
)


rooms = [room0, room1, room2, room3, room4, room5, room6, room7, room8, room9]
