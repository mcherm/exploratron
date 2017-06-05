#
# This contains the game currently known as "Exploratron". 
#

import pygame
import kindsofthing
from kindsofthing import *
from objects import *
import rooms

# ========= Start Classes for Game =========

    


class World:
    """Represents the entire world."""
    def __init__(self):
        self.gameOver = False
        self.rooms = rooms.rooms
        self.mobiles = []
        # set up player
        self.player = Player(11)
        playerRoom = self.rooms[1]
        self.player.setLocation( playerRoom, (2,1) )
        playerRoom.cellAt(2,1).addThing(self.player)
    def addMobiles(self, newMobiles):
        """Call this to add some new mobiles to the list of active
        mobiles."""
        print(f"Adding mobiles!") # FIXME: Remove
        self.mobiles.extend(newMobiles)

        
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
    def show(self, room, imageLibrary):
        self.screen.fill( (0,0,0) )
        for y in range(room.height):
            for x in range(room.width):
                cell = room.cellAt(x,y)
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


def moveMobiles(world):
    """This function will cause all of the mobiles to move one step,
    updating the world accordingly."""
    for mobile in world.mobiles:
        mobile.takeOneStep()
    

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
    moveMobiles(world)
            
    


def renderWorld(player, display, imageLibrary):
    display.show(player.room, imageLibrary)



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
