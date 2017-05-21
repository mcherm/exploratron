#
# This contains the game currently known as "Exploratron". 
#

import pygame
import kindsofthing
from kindsofthing import *
from objects import * 

# ========= Start Classes for Game =========

class Cell:
    """Contains a stack of things."""
    def __init__(self):
        self.things = []
    def addThing(self, thing):
        assert isinstance(thing, Thing)
        self.things.append(thing)
    def removeThing(self, thing):
        """This will remove the thing from this cell if it is in this
        cell. If it is not there then this raises ValueError."""
        self.things.remove(thing)
    def canEnter(self, mobile):
        """This returns True if the mobile is able to enter into this
        cell."""
        for thing in self.things:
            if not thing.canEnter(mobile):
                return False
        return True
    def doEnter(self, mobile):
        """This gets called when a mobile enters into this cell. It should
        make sure that all the things in the cell that do anything when you
        enter do whatever they are supposed to."""
        for thing in self.things:
            thing.doEnter(mobile)


class Grid:
    """A grid has rows and colums of cells."""
    def __init__(self, width, height):
        self.cells = [ [Cell() for x in range(width)] for y in range(height)]
        self.width = width
        self.height = height
    def cellAt(self, x, y):
        return self.cells[y][x]


class Location:
    """This is a way to specify a particular place."""
    def __init__(self, roomNumber, coordinates):
        self.roomNumber = roomNumber
        self.coordinates = coordinates


def makeRoom0():
    grid = Grid(7, 5)
    grid.cellAt(3,2).addThing(StairsDown())
    grid.cellAt(0,0).addThing(BrickWall())
    grid.cellAt(0,1).addThing(BrickWall())
    grid.cellAt(0,2).addThing(BrickWall())
    grid.cellAt(0,3).addThing(BrickWall())
    grid.cellAt(0,4).addThing(BrickWall())
    grid.cellAt(1,0).addThing(BrickWall())
    grid.cellAt(2,0).addThing(WoodenDoor(Location(1, (2,3))))
    grid.cellAt(3,0).addThing(BrickWall())
    grid.cellAt(4,0).addThing(BrickWall())
    grid.cellAt(5,0).addThing(BrickWall())
    grid.cellAt(6,0).addThing(BrickWall())
    grid.cellAt(6,1).addThing(BrickWall())
    grid.cellAt(6,2).addThing(BrickWall())
    grid.cellAt(6,3).addThing(BrickWall())
    grid.cellAt(6,4).addThing(BrickWall())
    grid.cellAt(1,4).addThing(BrickWall())
    grid.cellAt(2,4).addThing(BrickWall())
    grid.cellAt(3,4).addThing(BrickWall())
    grid.cellAt(4,4).addThing(BrickWall())
    grid.cellAt(5,4).addThing(BrickWall())
    grid.cellAt(1,1).addThing(Dirt())
    grid.cellAt(2,1).addThing(Dirt())
    grid.cellAt(3,1).addThing(Dirt())
    grid.cellAt(4,1).addThing(Dirt())
    grid.cellAt(5,1).addThing(Dirt())
    grid.cellAt(5,1).addThing(Mobile(12))
    grid.cellAt(1,2).addThing(Dirt())
    grid.cellAt(1,3).addThing(Dirt())
    grid.cellAt(2,2).addThing(Dirt())
    grid.cellAt(2,3).addThing(Dirt())
    grid.cellAt(3,3).addThing(Dirt())
    grid.cellAt(4,2).addThing(Dirt())
    grid.cellAt(4,3).addThing(Dirt())
    grid.cellAt(5,2).addThing(Dirt())
    grid.cellAt(5,3).addThing(Dirt())
    grid.cellAt(5,3).addThing(Chest())
    grid.cellAt(1,1).addThing(Chest())
    return grid

def makeRoom1():
    grid = Grid(5, 4)
    grid.cellAt(0,0).addThing(BrickWall())
    grid.cellAt(0,1).addThing(BrickWall())
    grid.cellAt(0,2).addThing(BrickWall())
    grid.cellAt(0,3).addThing(BrickWall())
    grid.cellAt(1,0).addThing(BrickWall())
    grid.cellAt(1,1).addThing(Dirt())
    grid.cellAt(1,2).addThing(Dirt())
    grid.cellAt(1,3).addThing(BrickWall())
    grid.cellAt(2,0).addThing(BrickWall())
    grid.cellAt(2,1).addThing(Dirt())
    grid.cellAt(2,2).addThing(Dirt())
    grid.cellAt(2,3).addThing(WoodenDoor(Location(0, (2,0)) ))
    grid.cellAt(3,0).addThing(BrickWall())
    grid.cellAt(3,1).addThing(Dirt())
    grid.cellAt(3,2).addThing(Dirt())
    grid.cellAt(3,3).addThing(BrickWall())
    grid.cellAt(4,0).addThing(BrickWall())
    grid.cellAt(4,1).addThing(BrickWall())
    grid.cellAt(4,2).addThing(BrickWall())
    grid.cellAt(4,3).addThing(BrickWall())
    return grid
    


class World:
    """Represents the entire world."""
    def __init__(self):
        self.gameOver = False
        room0 = makeRoom0()
        room1 = makeRoom1()
        self.rooms = [room0, room1]
        
        self.player = Player(11)
        self.player.setLocation( room1, (2,1) )
        room1.cellAt(2,1).addThing(self.player)

        
class PlayerInputs:
    def __init__(self, events):
        self.events = events

        
# ========= End Classes for Game =========


# ========= Start Drawing Stuff =========

TILE_SIZE = 64


class ImageLibrary:
    def __init__(self):
        rootDir = '/Users/rdg959/Documents/personal/Exploratron/img'
        names = [
            'drawntiles64/dirt-1',
            'drawntiles64/dirt-1',
            'drawntiles64/dirt-1',
            'drawntiles64/dirt-1',
            'drawntiles64/dirt-1',
            'drawntiles64/stairs-down',
            'drawntiles64/chest',
            'drawntiles64/wall-1',
            'drawntiles64/doorway-1',
            'drawntiles64/chest',
            'drawntiles64/chest',
            'drawntiles64/adventurer-1-boy',
            'foundassets/crawl-tiles Oct-5-2010/player/transform/dragon_form',            
          ]
        self.imageById = {}
        for imgnum, name in enumerate(names):
            self.imageById[imgnum] = pygame.image.load(
                f'{rootDir}/{name}.png')
    def lookup(self, imgnum):
        return self.imageById[imgnum]
    

class PygameGridDisplay:
    def __init__(self):
        self.screen = pygame.display.set_mode( (1024,768) )
    def show(self, grid, imageLibrary):
        self.screen.fill( (0,0,0) )
        for y in range(grid.height):
            for x in range(grid.width):
                cell = grid.cellAt(x,y)
                for thing in cell.things:
                    image = imageLibrary.lookup( thing.tileId )
                    self.screen.blit( image, (TILE_SIZE*x, TILE_SIZE*y) )
        pygame.display.flip()
    def quit(self):
        pygame.quit()


class PygameInput:
    def __init__(self):
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
    def getEvents(self):
        return pygame.event.get()


# ========= End Drawing Stuff ==========

# ========= Start Functions for Game =========

def getPlayerInputs(pygameInput):
    events = pygameInput.getEvents()
    return PlayerInputs(events)


def updateWorld(world, playerInputs):
    events = playerInputs.events
    if events:
        print(events)
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                world.player.moveSouth()
            if event.key == pygame.K_w:
                world.player.moveNorth()
            if event.key == pygame.K_d:
                world.player.moveEast()
            if event.key == pygame.K_a:
                world.player.moveWest()
        if event.type == pygame.QUIT:
            world.gameOver = True
            
    


def renderWorld(player, display, imageLibrary):
    display.show(player.grid, imageLibrary)



def mainLoop(world):
    display = PygameGridDisplay()
    imageLibrary = ImageLibrary()
    pygameInput = PygameInput()
    player = world.player
    while not world.gameOver:
        renderWorld(player, display, imageLibrary)
        playerInputs = getPlayerInputs(pygameInput)
        updateWorld(world, playerInputs)
    display.quit()

# ========= End Functions for Game =========

kindsofthing.world = World()
mainLoop(kindsofthing.world)
